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
    """
    Convert 2-digit year to 4-digit year.
    """
    
    if year < 80:
        return 2000 + year
    else:
        return 1900 + year

class DBF(list):
    """
    Class to read DBF files.
    """

    def __init__(self, filename,
                 encoding='latin1',  # Todo: is this a good default?
                 raw=False,
                 ignorecase=True,
                 lowernames=False,
                 parserclass=FieldParser,
                 recfactory=dict,
                 peek=False):

        self.encoding = encoding
        self.recfactory = recfactory
        self.raw = raw
        self.ignorecase = ignorecase
        self.lowernames = lowernames
        self.parserclass = parserclass

        self._field_parser = self.parserclass(self.encoding)

        # Name part before .dbf is the table name
        self.name = os.path.basename(filename)
        self.name = os.path.splitext(self.name)[0]
        self.name = self.name.lower()

        if ignorecase:
            self.filename = ifind(filename)
        else:
            self.filename = filename

        # Filled in by self._read_headers()
        self.memofilename = None
        self.header = None
        self.fields = []       # namedtuples
        self.field_names = []  # strings

        with open(self.filename, mode='rb') as self.file:
            self._read_headers()
            self._check_headers()
            
            self.date = datetime.date(expand_year(self.header.year),
                                      self.header.month,
                                      self.header.day)
            
            self.deleted = []
            
            if not peek:
                self._load()

        del self.file

    def _read_headers(self):
        #
        # Todo: more checks
        # http://www.clicketyclick.dk/databases/xbase/format/dbf_check.html#CHECK_DBF
        #
        self.header = DBFHeader.read(self.file)

        #
        # Read field headers
        #
        while 1:
            sep = self.file.read(1)
            if sep in (b'\x0d', '\n', ''):
                # End of field headers
                break

            fh = DBFField.read(self.file, prepend=sep)
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
            raise ValueError('dbf file must have at least one field: %s' % self.filename)


        # Check for memo file
        field_types = set([f.type for f in self.fields])
        if 'M' in field_types:
            fn = os.path.splitext(self.filename)[0] + '.fpt'
            match = ifind(self.filename, ext='.fpt')
            if match:
                self.memofilename = match
            else:
                # Todo: warn and return field as byte string?
                raise IOError('Missing memo file: %r' % fn)

    def _check_headers(self):
        """Check headers for possible format errors."""

        for field in self.fields:

            if field.type == '0' and field.length != 1:
                    ValueError('Field of type 0 must have length 1 (was %s)' % field.length)

            elif field.type == 'I' and field.length != 4:
                    ValueError('Field type I must have length 4 (was %s)' % field.length)

            elif field.type == 'L' and field.length != 1:
                    ValueError('Field type L must have length 1 (was %s)' % field.length)

            elif not self._field_parser.field_type_supported(field.type):
                # Todo: return as byte string?
                ValueError('Unknown field type: %r' % (field.type))

    def _read_record(self, fpt=None):
        items = []  # List of Field
        for field in self.fields:
            value = self.file.read(field.length)
            if self.raw:
                value = value  # Just return the byte string
            else:
                value = self._field_parser.parse(field, value)

                #
                # Decoding memo fields requires a little more
                # trickery.
                #
                if field.type == 'M':
                    if value == None:
                        value = ''
                    else:
                        fptrecord = fpt[value]
                        if ftprecord.type == 'memo':
                            # Decode to unicode
                            value = parse_string(fptrecord.data, self.encoding)
                        else:
                            # Byte array
                            value = fptrecord.data

            items.append(FieldValue(name=field.name, value=value))

        row = self.recfactory(items)
        
        return row

    def _load(self):

        #
        # Get memo file
        #
        if self.memofilename and not self.raw:
            fpt = FPT(self.memofilename)
        else:
            fpt = None

        #
        # Skip header
        #
        self.file.seek(self.header.headerlen, 0)

        #
        # Read records
        #
        while 1:
            sep = self.file.read(1)

            if sep == b'':
                break  # End of file reached
            elif sep == b' ':
                row = self._read_record(fpt)
                self.append(row)
            elif sep == b'*':
                row = self._read_record(fpt)
                self.deleted.append(row)

    def __repr__(self):
        return '%s(%r, encoding=%r)' % (
            self.__class__.__name__,
            self.filename,
            self.encoding)

    #
    # Context manager
    # Todo: why is this a context manager?
    #
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
