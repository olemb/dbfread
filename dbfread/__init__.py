# -*- coding: utf-8 -*-

__author__ = 'Ole Martin Bjørndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '0.1.0x'

from .dbf import Table

read = Table  # Shortcut

class RecObject(object):
    def __init__(self, items):
        self.__dict__.update(items)
