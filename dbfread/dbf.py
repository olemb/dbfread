"""
Class to read DBF files.
"""

import os
import datetime
import collections

from .struct_parser import StructParser
from .field_parser import FieldParser
from .common import parse_string
from .ifiles import ifind
from .fpt import FPT
from .codepages import guess_encoding
from .dbversions import get_dbversion_string

DBFHeader = StructParser(
    'DBFHeader',
    '<BBBBLHHHBBLLLBBH',
    ['dbversion',
     'year',
     'month',
     'day',
     'numrecords',
     'headerlen',
     'recordlen',
     'reserved1',
     'incomplete_transaction',
     'encryption_flag',
     'free_record_thread',
     'reserved2',
     'reserved3',
     'mdx_flag',
     'language_driver',
     'reserved4',
     ])

DBFField = StructParser(
    'DBFField',
    '<11scLBBHBBBB7sB',
    ['name',
     'type',
     'address',
     'length',
     'decimal_count',
     'reserved1',
     'workarea_id',
     'reserved2',
     'reserved3',
     'set_fields_flag',
     'reserved4',
     'index_field_flag',
     ])


def expand_year(year):
    """Convert 2-digit year to 4-digit year."""
    
    if year < 80:
        return 2000 + year
    else:
        return 1900 + year


class RecordIterator(object):
    def __init__(self, table, record_type):
        self._record_type = record_type
        self._table = table

    def __iter__(self):
        return self._table._iter_records(self._record_type)
 
    def __len__(self):
        return self._table._count_records(self._record_type)


class FakeMemoFile(object):
    def __getitem__(self, i):
        return ''

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False

_FAKE_MEMOFILE = FakeMemoFile()


class DBF(object):
    """DBF table."""
    def __init__(self, filename,
                 encoding=None,
                 ignorecase=True,
                 lowernames=False,
                 parserclass=FieldParser,
                 recfactory=dict,
                 load=False,
                 raw=False):

        self.encoding = encoding
        self.ignorecase = ignorecase
        self.lowernames = lowernames
        self.parserclass = parserclass
        self.recfactory = recfactory
        self.raw = raw

        # Name part before .dbf is the table name
        self.name = os.path.basename(filename)
        self.name = os.path.splitext(self.name)[0].lower()
        self._records = None
        self._deleted = None

        if ignorecase:
            self.filename = ifind(filename)
            if not self.filename:
                raise IOError('No such file: {!r}'.format(filename))
        else:
            self.filename = filename

        # Filled in by self._read_headers()
        self.memofilename = None
        self.header = None
        self.fields = []       # namedtuples
        self.field_names = []  # strings

        with open(self.filename, mode='rb') as infile:
            self._read_headers(infile)
            self._field_parser = self.parserclass(self.encoding)

            self._check_headers()
            
            self.date = datetime.date(expand_year(self.header.year),
                                      self.header.month,
                                      self.header.day)
            
        self.dbversion = get_dbversion_string(self.header.dbversion)

        if load:
            self.load()

    @property
    def loaded(self):
        return self._records is not None

    def load(self):
        if not self.loaded:
            self._records = list(self._iter_records(b' '))
            self._deleted = list(self._iter_records(b'*'))

    def unload(self):
        self._records = None
        self._deleted = None

    @property
    def records(self):
        if self.loaded:
            return self._records
        else:
            return RecordIterator(self, b' ')

    @property
    def deleted(self):
        if self.loaded:
            return self._deleted
        else:
            return RecordIterator(self, b'*')

    def _get_memofile(self):
        if self.memofilename and not self.raw:
            return FPT(self.memofilename)
        else:
            return _FAKE_MEMOFILE

    def _read_headers(self, infile):
        #
        # Todo: more checks
        # http://www.clicketyclick.dk/databases/xbase/format/dbf_check.html#CHECK_DBF
        #
        self.header = DBFHeader.read(infile)

        if self.encoding is None:
            try:
                self.encoding = guess_encoding(self.header.language_driver)
            except LookupError as err:
                self.encoding = 'ascii'

        #
        # Read field headers
        #
        while 1:
            sep = infile.read(1)
            if sep in (b'\r', b'\n', b''):
                # End of field headers
                break

            # sep is the first byte of the field name.
            # Go back one byte and read field header.
            infile.seek(-1, 1)
            fh = DBFField.read(infile)

            fieldname = parse_string(fh.name, self.encoding)
            if self.lowernames:
                fieldname = fieldname.lower()
            fieldtype = parse_string(fh.type, self.encoding)

            fh = fh._replace(name=fieldname,
                             type=fieldtype)

            self.field_names.append(fh.name)

            self.fields.append(fh)

        if len(self.fields) < 1:
            message = 'dbf file must have at least one field: {!r}'
            raise ValueError(message.format(self.filename))


        # Check for memo file
        field_types = set([field.type for field in self.fields])
        if 'M' in field_types:
            fn = os.path.splitext(self.filename)[0] + '.fpt'
            match = ifind(self.filename, ext='.fpt')
            if match:
                self.memofilename = match
            else:
                # Todo: warn and return field as byte string?
                raise IOError('Missing memo file: {!r}'.format(fn))

    def _check_headers(self):
        """Check headers for possible format errors."""
        for field in self.fields:

            if field.type == '0' and field.length != 1:
                message = 'Field of type 0 must have length 1 (was {})'
                raise ValueError(message.format(field.length))

            elif field.type == 'I' and field.length != 4:
                message = 'Field type I must have length 4 (was {})'
                raise ValueError(message.format(field.length))

            elif field.type == 'L' and field.length != 1:
                message = 'Field type L must have length 1 (was {})'
                raise ValueError(message.format(field.length))

            elif not self._field_parser.field_type_supported(field.type):
                # Todo: return as byte string?
                raise ValueError('Unknown field type: {!r}'.format(field.type))

    def _read_record(self, infile, memofile):
        items = []  # List of Field

        # Shortcuts for speed.
        parse = self._field_parser.parse
        append = items.append
        read = infile.read
        
        if self.raw:
            items = [(field.name, read(field.length)) for field in self.fields]
        else:
            for field in self.fields:
                value = parse(field, read(field.length))

                #
                # Decoding memo fields requires a little more
                # trickery.
                #
                if field.type == 'M' and value is not None:
                    memo = memofile[value]
                    if memo.type == 'memo':
                        # Decode to unicode
                        value = parse_string(memo.data, self.encoding)
                    else:
                        # Byte string
                        value = memo.data

                append((field.name, value))

        return self.recfactory(items)
        
    def _skip_record(self, infile):
        # -1 for the record separator which was already read.
        infile.seek(self.header.recordlen - 1, 1)

    def _count_records(self, record_type=b' '):
        count = 0

        with open(self.filename, 'rb') as infile:
            # Skip to first record.
            infile.seek(self.header.headerlen, 0)

            while True:
                sep = infile.read(1)
                if sep == record_type:
                    count += 1
                    self._skip_record(infile)
                elif sep in (b'\x1a', b''):
                    # End of records.
                    break
                else:
                    self._skip_record(infile)

        return count

    def _iter_records(self, record_type=b' '):
        with open(self.filename, 'rb') as infile, \
             self._get_memofile() as memofile:
            # Skip to first record.
            infile.seek(self.header.headerlen, 0)

            # Shortcuts for speed.
            read_record = self._read_record
            skip_record = self._skip_record
            read = infile.read

            while True:
                sep = read(1)

                if sep == record_type:
                    yield read_record(infile, memofile)
                elif sep in (b'\x1a', b''):
                    # End of records.
                    break
                else:
                    skip_record(infile)

    def __iter__(self):
        if self.loaded:
            return list.__iter__(self._records)
        else:
            return self._iter_records()

    def __len__(self):
        return len(self.records)

    def __repr__(self):
        if self.loaded:
            status = 'loaded'
        else:
            status = 'unloaded'
        return '<{} DBF table {!r}>'.format(status, self.filename)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.unload()
        return False

class DeprecatedDBF(DBF, list):
    """This is the old version of the table which is a subclass of list.

    It is included for backwards compatability with 1.0 and older."""
    @property
    def loaded(self):
        # Since records are loaded into the table object
        # we have to check the deleted attribute here.
        return isinstance(self._deleted, list)

    def load(self):
        if not self.loaded:
            self[:] = self._iter_records(b' ')
            self._deleted = list(self._iter_records(b'*'))

    def unload(self):
        # self.loaded is not checked here because this
        # is called by __init__() where self.loaded=False.
        # Also, unloading twice has no consequences.
        del self[:]
        self._deleted = None
        
    def __iter__(self):
        if self.loaded:
            return list.__iter__(self)
        else:
            return self._iter_records()

    def __len__(self):
        if self.loaded:
            return list.__len__(self)
        else:
            return self._count_records()

    def __repr__(self):
        if self.loaded:
            return list.__repr__(self)
        else:
            return '<unloaded DBF table {!r}>'.format(self.filename)
