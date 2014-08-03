class DBFError(IOError):
    pass

class DataFileNotFound(DBFError):
    pass

class MemoFileNotFound(DBFError):
    pass
