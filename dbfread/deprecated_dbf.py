from warnings import warn
from .dbf import DBF

class DeprecatedDBF(DBF, list):
    """This is the old version of the table which is a subclass of list.

    It is included for backwards compatability with 1.0 and older."""
    def __init__(self, filename, load=True, **kwargs):
        warn("read() is deprecated."
             " Please use dbfread.open(filename, load=True).")
        DBF.__init__(self, filename, load=load, **kwargs)

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
