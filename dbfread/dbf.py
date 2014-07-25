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

FieldValue = collections.namedtuple('Field', 'name value')


def expand_year(year):
    """Convert 2-digit year to 4-digit year."""
    
    if year < 80:
        return 2000 + year
    else:
        return 1900 + year


class RecordIterator(object):
    def __init__(self, table, deleted=False):
        self._deleted = deleted
        self._table = table

    def __iter__(self):
        for record in self._table._iter_records(deleted=self._deleted,
                                                read=True):
            yield record
 
    def __len__(self):
        num_records = 0
        for _ in self._table._iter_records(deleted=self._deleted,
                                           read=False):
            num_records += 1
        return num_records


class FakeMemoFile(object):
    def __getitem__(self, i):
        return ''

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False

_FAKE_MEMOFILE = FakeMemoFile()


class Table(list):
    """
    Class to read DBF files.
    """

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
        self.name = os.path.splitext(self.name)[0]
        self.name = self.name.lower()
        
        self.deleted = []
        self.loaded = False

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
            
        if load:
            self.load()
        else:
            self.unload()

    def _get_memofile(self):
        if self.memofilename and not self.raw:
            return FPT(self.memofilename)
        else:
            return _FAKE_MEMOFILE
 
    def load(self):
        if not self.loaded:
            del self[:]
            for record in RecordIterator(self):
                self.append(record)

            self.deleted = list(RecordIterator(self, deleted=True))

            self.loaded = True

    def unload(self):
        del self[:]
        self.deleted = RecordIterator(self, deleted=True)
        self.loaded = False

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
                self.encoding = 'latin1'

        #
        # Read field headers
        #
        while 1:
            sep = infile.read(1)
            if sep in (b'\x0d', '\n', ''):
                # End of field headers
                break

            fh = DBFField.read(infile, prepend=sep)
            # We need to fix the name and type

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
        for field in self.fields:
            value = infile.read(field.length)
            if self.raw:
                value = value  # Just return the byte string
            else:
                value = self._field_parser.parse(field, value)

                #
                # Decoding memo fields requires a little more
                # trickery.
                #
                if field.type == 'M':
                    if value is None:
                        value = ''
                    else:
                        memo = memofile[value]
                        if memo.type == 'memo' and not self.raw:
                            # Decode to unicode
                            value = parse_string(memo.data, self.encoding)
                        else:
                            # Byte array
                            value = memo.data

            items.append(FieldValue(name=field.name, value=value))

        return self.recfactory(items)
        
    def _skip_record(self, infile):
        # Seek ahead by size of record.
        infile.seek(sum(field.length for field in self.fields), 1)

    def _iter_records(self, deleted=False, read=False):
        with open(self.filename, 'rb') as infile, \
              self._get_memofile() as memofile:
            # Skip to first record.
            infile.seek(self.header.headerlen, 0)
            while True:
                sep = infile.read(1)

                if sep == b'' or sep == b'\x1a':
                    return  # End of file reached
                elif sep not in b' *':
                    raise IOError("invalid record separator '{}'".format(sep))

                if deleted and sep == b'*':
                    interesting_record = True
                elif not deleted and sep == b' ':
                    interesting_record = True
                else:
                    interesting_record = False

                if interesting_record:
                    if read:
                        yield self._read_record(infile, memofile)
                    else:
                        yield self._skip_record(infile)
                else:
                    self._skip_record(infile)

    def __iter__(self):
        if self.loaded:
            for record in list.__iter__(self):
                yield record
        else:
            for record in RecordIterator(self):
                yield record            

    def __len__(self):
        if self.loaded:
            return list.__len__(self)
        else:
            return len(RecordIterator(self))

    def __repr__(self):
        if self.loaded:
            return list.__repr__(self)
        else:
            return '<Unloaded DBF table {!r}>'.format(self.filename)

