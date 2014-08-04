"""
Convert table to CSV.

Passing ordered=True returns records as ordered dictionaries.
This is useful for exporting to formats where field order is important.
"""
import sys
import csv
import dbfread

with dbfread.open('files/people.dbf', ordered=True, lowernames=True) as people:
    writer = csv.writer(sys.stdout, delimiter=';',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(people.field_names)
    for record in people:
        writer.writerow(record.values())
