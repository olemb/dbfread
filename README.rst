dbfget - Python library for getting data out of DBF files
=========================================================

Requires Python 3.2 or 2.7 (works without changes in both)g

Project page: http://nerdly.info/ole/dbf/

License: MIT

(Latest version of the source code: https://github.com/olemb/dbfget)
(Not out yet.)

Simple example::

    >>> import dbfget
    >>> people = dbfget.read('people.dbf')
    
    >>> for p in people:
    ...     print(p['NAME'], p['BIRTHDAY'], p['BEARDED'])
    George 1982-12-16 True
    Wendy 1984-02-10 False
    
    >>> george = people['George']
    >>> george['BIRTHDAY']
    1982-12-16


Features
--------

  - supports all data types and convert to native Python types
  - reads memo fields (.fpt) and returns them as unicode strings
    (binary memo fields are not yet supported)
  - returns records as dictionary (or alternative format, such as OrderedDict)
  - explicit code page conversion to unicode
  - option to lowercase field names
  - file name case agnostic (KabReg.dbf will match KABREG.FPT)


Possible future features
------------------------

  - transparent code page conversion to unicode where possible
    (this is tricky)
  - method to read deleted records
  - easy export to SQL / CSV
  - raw mode (to get values as byte strings)
    

Contact
--------

Ole Martin Bjørndalen - ombdalen@gmail.com - http://nerdly.info/ole/
