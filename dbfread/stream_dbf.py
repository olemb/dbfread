"""
Class to read DBF files from a file-like stream object.
"""
import datetime
import collections

from .struct_parser import StructParser
from .field_parser import FieldParser
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
        if self._table.loaded:
            return len(self._table._records)
        else:
            count = 0
            for _ in self._table._iter_records():
                count += 1
            return count

class StreamDBF(object):
    """DBF table."""
    def __init__(self, fileobj, encoding=None,
                 lowernames=True,
                 parserclass=FieldParser,
                 recfactory=collections.OrderedDict,
                 load=False, raw=False, deletedrecords=False):

        self.fileobj = fileobj
        self._finished = False
        self.encoding = encoding
        self.lowernames = lowernames
        self.parserclass = parserclass
        self.raw = raw
        self.deletedrecords = deletedrecords

        if recfactory is None:
            self.recfactory = lambda items: items
        else:
            self.recfactory = recfactory

        self._records = None
        self._deleted = None

        # Filled in by self._read_headers()
        self.header = None
        self.fields = []       # namedtuples
        self.field_names = []  # strings

        self._read_header()
        self._read_field_headers()
        self._check_headers()

        try:
            self.date = datetime.date(expand_year(self.header.year),
                                      self.header.month,
                                      self.header.day)
        except ValueError:
            # Invalid date or '\x00\x00\x00'.
            self.date = None

        if load:
            self.load()

    @property
    def dbversion(self):
        return get_dbversion_string(self.header.dbversion)

    @property
    def loaded(self):
        """``True`` if records are loaded into memory."""
        return self._records is not None

    def load(self):
        """Load records into memory.

        This loads records or deleted records depending on the contents of the
        ``deleted`` flag when the StreamDBF was created. The ``records`` or
        ``deleted`` attributes (as appropriate) will now be lists of records.
        """
        if not self.loaded:
            if self.deletedrecords:
                self._deleted = list(self._iter_records(b'*'))
            else:
                self._records = list(self._iter_records(b' '))

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

    def _read_header(self):
        # Todo: more checks?
        self.header = DBFHeader.read(self.fileobj)

        if self.encoding is None:
            try:
                self.encoding = guess_encoding(self.header.language_driver)
            except LookupError:
                self.encoding = 'ascii'

    def _read_field_headers(self):
        while True:
            sep = self.fileobj.read(1)
            if sep in (b'\r', b'\n', b''):
                # End of field headers
                break

            field = DBFField.unpack(sep + self.fileobj.read(DBFField.size - 1))

            field.type = chr(ord(field.type))

            # For character fields > 255 bytes the high byte
            # is stored in decimal_count.
            if field.type in 'C':
                field.length |= field.decimal_count << 8
                field.decimal_count = 0

            # Field name is b'\0' terminated.
            field.name = field.name.split(b'\0')[0].decode(self.encoding)
            if self.lowernames:
                field.name = field.name.lower()

            self.field_names.append(field.name)

            self.fields.append(field)

    def _check_headers(self):
        field_parser = self.parserclass(self)

        """Check headers for possible format errors."""
        for field in self.fields:

            if field.type == 'I' and field.length != 4:
                message = 'Field type I must have length 4 (was {})'
                raise ValueError(message.format(field.length))

            elif field.type == 'L' and field.length != 1:
                message = 'Field type L must have length 1 (was {})'
                raise ValueError(message.format(field.length))

            elif not field_parser.field_type_supported(field.type):
                # Todo: return as byte string?
                raise ValueError('Unknown field type: {!r}'.format(field.type))

    def _skip_record(self, infile):
        # -1 for the record separator which was already read.
        infile.read(self.header.recordlen - 1)

    def _iter_records(self, record_type=None):

        if self._finished:
            raise IOError('Cannot read from stream twice')

        if record_type is None:
            if self.deletedrecords:
                record_type = b'*'
            else:
                record_type = b' '

        if not self.raw:
            field_parser = self.parserclass(self)
            parse = field_parser.parse

        # Shortcuts for speed.
        skip_record = self._skip_record
        read = self.fileobj.read

        while True:
            sep = read(1)

            if sep == record_type:
                if self.raw:
                    items = [(field.name, read(field.length)) \
                             for field in self.fields]
                else:
                    items = [(field.name,
                              parse(field, read(field.length))) \
                             for field in self.fields]

                yield self.recfactory(items)

            elif sep in (b'\x1a', b''):
                # End of records.
                break
            else:
                skip_record(self.fileobj)

        self._finished = True

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
        return '<{} DBF table from stream>'.format(status)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.unload()
        return False
