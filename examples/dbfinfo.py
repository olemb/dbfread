#!/usr/bin/env python
from __future__ import print_function
import sys
import dbfread

def show(*words):
    print('  ' + ' '.join(str(word) for word in words))

def show_field(field):
    print('    {} ({} {})'.format(field.name, field.type, field.length))

def main():
    for filename in sys.argv[1:]:
        print(filename + ':')
        table = dbfread.open(filename)
        show('Name:', table.name)
        show('Memo File:', table.memofilename or '')
        show('DB Version:', table.dbversion)
        show('Records:', len(table))
        show('Deleted Records:', len(table.deleted))
        show('Last Updated:', table.date)
        show('Character Encoding:', table.encoding)
        show('Fields:')
        for field in table.fields:
            show_field(field)

main()
