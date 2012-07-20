# -*- coding: utf-8 -*-

__author__ = 'Ole Martin Bjørndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '0.1.0'

from .dbf import DBF as read

#
# Todo: this should have inherited from OrderedDict,
# but that doesn't seem to work.
#
class DictObject(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)

__all__ = ['DictObject', 'read']
