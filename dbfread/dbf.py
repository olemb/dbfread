"""
Class to read DBF files.
"""
import os
import collections
from contextlib import closing

from .stream_dbf import StreamDBF
from .ifiles import ifind
from .memo import find_memofile, open_memofile, FakeMemoFile
from .field_parser import FieldParser
from .exceptions import *

class DBF(StreamDBF):
    """DBF table."""
    def __init__(self, filename, encoding=None, ignorecase=True,
                 lowernames=False,
                 parserclass=FieldParser,
                 recfactory=collections.OrderedDict,
                 load=False,
                 raw=False,
                 ignore_missing_memofile=False):

        self.ignorecase = ignorecase
        self.ignore_missing_memofile = ignore_missing_memofile

        # Name part before .dbf is the table name
        self.name = os.path.basename(filename)
        self.name = os.path.splitext(self.name)[0].lower()

        if ignorecase:
            self.filename = ifind(filename)
            if not self.filename:
                raise DBFNotFound('could not find file {!r}'.format(filename))
        else:
            self.filename = filename

        with open(self.filename, mode='rb') as infile:
            StreamDBF.__init__(self, fileobj=infile, encoding=encoding,
                               lowernames=lowernames, parserclass=parserclass,
                               recfactory=recfactory, load=load, raw=raw)

        self.memofilename = self._get_memofilename()

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

    def load(self):
        """Load records into memory.

        This loads both records and deleted records. The ``records``
        and ``deleted`` attributes will now be lists of records.

        """
        if not self.loaded:
            self._records = list(self._iter_records(b' '))
            self._deleted = list(self._iter_records(b'*'))

    def _open_memofile(self):
        if self.memofilename and not self.raw:
            return open_memofile(self.memofilename, self.header.dbversion)
        else:
            return FakeMemoFile(self.memofilename)

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

        if self.fileobj.closed:
            self.fileobj = open(self.filename, 'rb')

        with closing(self.fileobj) as infile, \
             self._open_memofile() as memofile:

            # Skip to first record.
            infile.seek(self.header.headerlen, 0)
            self._finished = False

            # Could use 'yield from' in Python 3
            for r in StreamDBF._iter_records(self, record_type):
                yield r

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
        if not self.fileobj.closed:
            self.fileobj.close()
        return False
