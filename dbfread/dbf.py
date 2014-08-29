"""
Class to read DBF files.
"""
import os
import sys
import datetime
import collections

from .ifiles import ifind
from .struct_parser import StructParser
from .field_parser import FieldParser
from .memo import find_memofile, open_memofile, FakeMemoFile, BinaryMemo
from .codepages import guess_encoding
from .dbversions import get_dbversion_string
from .exceptions import *

PY2 = sys.version_info[0] == 2

if PY2:
    decode_text = unicode
else:
    decode_text = str

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


class DBF(object):
    """DBF table."""
    def __init__(self, filename, encoding=None, ignorecase=True,
                 lowernames=False,
                 parserclass=FieldParser,
                 recfactory=collections.OrderedDict,
                 load=False,
                 raw=False,
                 ignore_missing_memofile=False):

        self.encoding = encoding
        self.ignorecase = ignorecase
        self.lowernames = lowernames
        self.parserclass = parserclass
        self._field_parser = None
        self.raw = raw
        self.ignore_missing_memofile = ignore_missing_memofile

        if recfactory is None:
            self.recfactory = lambda items: items
        else:
            self.recfactory = recfactory

        # Name part before .dbf is the table name
        self.name = os.path.basename(filename)
        self.name = os.path.splitext(self.name)[0].lower()
        self._records = None
        self._deleted = None

        if ignorecase:
            self.filename = ifind(filename)
            if not self.filename:
                raise DBFNotFound(repr(filename))
        else:
            self.filename = filename

        # Filled in by self._read_headers()
        self.memofilename = None
        self.header = None
        self.fields = []       # namedtuples
        self.field_names = []  # strings

        with open(self.filename, mode='rb') as infile:
            self._read_headers(infile, ignore_missing_memofile)
            self._check_headers()
            
            self.date = datetime.date(expand_year(self.header.year),
                                      self.header.month,
                                      self.header.day)
    
        self.memofilename = self._get_memofilename()

        if load:
            self.load()

    @property
    def dbversion(self):
        return get_dbversion_string(self.header.dbversion)

    def _get_memofilename(self):
        # Does the table have a memo field?
        field_types = [field.type for field in self.fields]
        if not set(field_types) & set('MGPB'):
            # No memo fields.
            return None

        path = find_memofile(self.filename)
        if path is None:
            if self.ignore_missing_memofile:
                return None
            raise MissingMemoFile('missing memo file for {}'.format(
                self.filename))
        else:
            return path

    @property
    def loaded(self):
        """``True`` if records are loaded into memory."""
        return self._records is not None

    def load(self):
        """Load records into memory.

        This loads both records and deleted records. The ``records``
        and ``deleted`` attributes will now be lists of records.

        """
        if not self.loaded:
            self._records = list(self._iter_records(b' '))
            self._deleted = list(self._iter_records(b'*'))

    def unload(self):
        """Unload records from memory.

        The records and deleted attributes will now be instances of
        ``RecordIterator``, which streams records from disk.
        """
        self._records = None
        self._deleted = None

    @property
    def records(self):
        """Records (not included deleted ones). When loaded a list of records,
        when not loaded a new ``RecordIterator`` object.
        """
        if self.loaded:
            return self._records
        else:
            return RecordIterator(self, b' ')

    @property
    def deleted(self):
        """Deleted records. When loaded a list of records, when not loaded a
        new ``RecordIterator`` object.
        """
        if self.loaded:
            return self._deleted
        else:
            return RecordIterator(self, b'*')

    def _read_headers(self, infile, ignore_missing_memofile):
        # Todo: more checks?
        self.header = DBFHeader.read(infile)

        if self.encoding is None:
            try:
                self.encoding = guess_encoding(self.header.language_driver)
            except LookupError as err:
                self.encoding = 'ascii'

        self._field_parser = self.parserclass(self)

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

            fieldname = decode_text(fh.name[:fh.name.index(b'\0')],
                                    self.encoding)
            if self.lowernames:
                fieldname = fieldname.lower()
            fieldtype = decode_text(fh.type, self.encoding)

            fh = fh._replace(name=fieldname,
                             type=fieldtype)

            self.field_names.append(fh.name)

            self.fields.append(fh)

    def _get_memofile(self):
        if self.memofilename and not self.raw:
            return open_memofile(self.memofilename, self.header.dbversion)
        else:
            return FakeMemoFile(self.memofilename)

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
                # Todo: field.type in.
                if value is not None:
                    if field.type == 'M':
                        value = memofile[value]
                        # Visual FoxPro allows binary data in memo fields.
                        # These should not be decoded as string.
                        if not isinstance(value, BinaryMemo):
                            if value is not None:
                                value = decode_text(value, self.encoding)

                    elif field.type in 'GPB':
                        # G == OLE object
                        # B == binary data
                        # P == picture
                        value = memofile[value]

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
