# -*- coding: utf-8 -*-

__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '1.0.1'

from .dbf import Table

open = Table

def read(*args, **kwargs):
    if not 'load' in kwargs:
        kwargs['load'] = True
    return open(*args, **kwargs)
