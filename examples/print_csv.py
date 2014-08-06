"""Export to CSV."""
import sys
import csv
from dbfread import DBF

writer = csv.writer(sys.stdout)

table = DBF('files/people.dbf')
writer.writerow(table.field_names)
for record in table:
    writer.writerow(record.values())
