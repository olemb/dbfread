"""
Add custom field parsing by subclassing FieldParser.
"""
import dbfread

class MyFieldParser(dbfread.FieldParser):
    def parseC(self, field, data):
        # Return strings reversed.
        return data.rstrip(' 0').decode()[::-1]

for record in dbfread.open('files/people.dbf', parserclass=MyFieldParser):
    print(record['NAME'])
