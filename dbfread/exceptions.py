class DBFNotFound(IOError):
    pass

class MissingMemoFile(IOError):
    pass

__all__ = ['DBFNotFound', 'MissingMemoFile']

