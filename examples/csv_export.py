"""
Export table to CSV.

This shows how to use a record factory to get just the values and not
names of fields.

It doesn't escape anything in the data, so you should use the standard
library module "csv" instead.
"""

if True:
    from dbfread import DBF

    def get_values(items):
       return [str(value) for (name, value) in items]

    table = DBF('files/people.dbf', recfactory=get_values)
    print(';'.join(table.field_names))
    for record in table:
        print(';'.join(record))
