#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dbf2sqlite - convert dbf files into sqlite database

Ole Martin Bjørndalen
University of Tromsø

Todo:
- -v --verbose option
- handle existing table (-f option?)
- primary key option? (make first column primary key)
- create only option?
- insert only option?
- options to select columns to insert?
"""

import os
import sys
import argparse
import sqlite3
import traceback

from dbfread import DBF

typemap = {
    'F': 'FLOAT',
    'L': 'BOOLEAN',
    'I': 'INTEGER',
    'C': 'TEXT',
    'N': 'REAL',  # because it can be integer or float
    'M': 'TEXT',
    'D': 'DATE',
    'T': 'DATETIME',
    '0': 'INTEGER',
}


def add_table(cursor, table):
    """Add a dbase table to an open sqlite database."""

    cursor.execute('drop table if exists %s' % table.name)

    field_types = {}
    for f in table.fields:
        field_types[f.name] = typemap.get(f.type, 'TEXT')

    #
    # Create the table
    #
    defs = ', '.join(['"%s" %s' % (f, field_types[f])
                      for f in table.field_names])
    sql = 'create table "%s" (%s)' % (table.name, defs)
    cursor.execute(sql)

    # Create data rows
    refs = ', '.join([':' + f for f in table.field_names])
    sql = 'insert into "%s" values (%s)' % (table.name, refs)

    for rec in table:
        cursor.execute(sql, list(rec.values()))

def parse_args():
    parser = argparse.ArgumentParser(
        description='usage: %prog [OPTIONS] table1.dbf ... tableN.dbf')
    arg = parser.add_argument

    arg('-o', '--output-file',
        action='store',
        dest='output_file',
        default=None,
        help='sqlite database to write to '
        '(default is to print schema to stdout)')

    arg('-e', '--encoding',
        action='store',
        dest='encoding',
        default=None,
        help='character encoding in DBF file')

    arg('--char-decode-errors',
        action='store',
        dest='char_decode_errors',
        default='strict',
        help='how to handle decode errors (see pydoc bytes.decode)')

    arg('tables',
        metavar='TABLE',
        nargs='+',
        help='tables to add to sqlite database')

    return parser.parse_args()

def main():
    args = parse_args()

    conn = sqlite3.connect(args.output_file or ':memory:')
    cursor = conn.cursor()

    for table_file in args.tables:
        try:
            add_table(cursor, DBF(table_file,
                                  lowernames=True,
                                  encoding=args.encoding,
                                  char_decode_errors=args.char_decode_errors))
        except UnicodeDecodeError as err:
            traceback.print_exc()
            sys.exit('Please use --encoding or --char-decode-errors.')

    conn.commit()

    #
    # Dump SQL schema and data to stdout if no
    # database file was specified.
    #
    # This currently only works in Python 3,
    # since Python 2 somehow defaults to 'ascii'
    # encoding.
    #
    if not args.output_file:
        for line in conn.iterdump():
            print(line)

if __name__ == '__main__':
    main()
