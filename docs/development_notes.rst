Development Notes
=================

Official Git Repository
-----------------------

dbfread uses Git and GitHub for version control.

All development happens in the develop branch:
http://github.com/olemb/dbfread/tree/develop


Unit Tests
----------

Unit tests can be run with::

    ./run_tests.py

This will run tests both in Python 2 and 3. If you want to test in a
specific version you can run ``tests.py`` directly.

Test are written with the standard library module ``unittest``, but
borrows the lighter syntax from ``pytest``. One drawback of this is
that the ``assert`` statements won't show the values that were
compared, so you will have to insert ``print()`` lines to find
these. I may switch to ``pytest``, which has a solution for this.


Automatic Unit Testing on Commit
--------------------------------

It's a good idea to run tests automatically before a commit. That way
code can't be commited unless it `passes all the tests
<http://www.youtube.com/watch?v=YHy06FMsezI>`_.

To install the pre-commit hook::

    ln -s ../../run_tests.py .git/hooks/pre-commit
