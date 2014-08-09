"""
Reads data from FPT (memo) files.

FPT files are used to varying lenght text or binary data which is too
large to fit in a DBF field.
"""
from collections import namedtuple
from .ifiles import ifind
from .struct_parser import StructParser


Header = StructParser(
    'FPTHeader',
    '>LHH504s',
    ['nextblock',
     'reserved1',
     'blocksize',
     'reserved2'])

BlockHeader = StructParser(
    'FPTBlock',
    '>LL',
    ['type',
     'length'])

# Record type
RECORD_TYPES = {
    0x0: 'picture',
    0x1: 'memo',
    0x2: 'object',
}

Record = namedtuple('Record', ['is_text', 'data'])

class MemoFile(object):
    def __init__(self, filename):
        self.filename = filename
        self._open()
        self._init()

    def _init(self):
        pass

    def _open(self):
        self.file = open(self.filename, 'rb')
        # Shortcuts for speed.
        self._read = self.file.read
        self._seek = self.file.seek

    def _close(self):
        self.file.close()

    def __getitem__(self, index):
        raise NotImplemented

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._close()
        return False


class FakeMemoFile(MemoFile):
    def __getitem__(self, i):
        return Record(is_text=False, data=None)

    def _open(self):
        pass

    def _init(self):
        pass

    def _close(self):
        pass


class FPT(MemoFile):
    def _init(self):
        self.header = Header.read(self.file)

    def __getitem__(self, index):
        """Get a memo from the file."""
        if index <= 0:
            raise IndexError('memo file got index {}'.format(index))

        self._seek(index * self.header.blocksize)
        block_header = BlockHeader.read(self.file)

        data = self._read(block_header.length)
        if len(data) != block_header.length:
            raise IOError('EOF reached while reading memo')
        
        if block_header.type == 0x1:
            return Record(is_text=True, data=data)
        else:
            return Record(is_text=False, data=data)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()
        return False

class DBF(MemoFile):
    pass

def find_memofile(dbf_filename):
    for ext in ['.fpt', '.dbt']:
        name = ifind(dbf_filename, ext=ext)
        if name:
            return name
    else:
        return None

def open_memofile(filename):
    if filename.lower().endswith('.fpt'):
        return FPT(filename)
    else:
        return DBT(filename)
