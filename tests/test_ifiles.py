from dbfread.ifiles import ipat, ifnmatch

assert ipat('mixed') == '[Mm][Ii][Xx][Ee][Dd]'
assert ifnmatch('test', 'test') == True
assert ifnmatch('miXEdCaSe', 'mixedcase') == True
assert ifnmatch('CAMELCASE/CamelCase', 'CamelCase/UPPERCASE') == False

# Pattern with
# assert ipat('[A]') == '[[Aa]]'


def test_ifind_literal_filename(tmpdir):
    from dbfread.ifiles import ifind

    directory = tmpdir.mkdir('data[1]')
    filename = directory.join('Report[1].DBF')
    filename.write_binary(b'')
    assert ifind(str(directory.join('report[1].dbf'))) == str(filename)


def test_dbf_with_brackets_in_filename(tmpdir):
    import os
    import shutil
    from dbfread import DBF

    source = os.path.join(os.path.dirname(__file__), 'cases', 'memotest.dbf')
    memo = os.path.join(os.path.dirname(__file__), 'cases', 'memotest.FPT')
    directory = tmpdir.mkdir('data[1]')
    filename = str(directory.join('Report[1].DBF'))
    shutil.copyfile(source, filename)
    shutil.copyfile(memo, str(directory.join('Report[1].FPT')))
    expected = list(DBF(source))
    assert list(DBF(str(directory.join('report[1].dbf')))) == expected


def test_ifind_keeps_pattern_lookup(tmpdir):
    from dbfread.ifiles import ifind

    filename = tmpdir.join('Report.DBF')
    filename.write_binary(b'')
    assert ifind(str(tmpdir.join('report*.dbf'))) == str(filename)
    assert ifind(str(tmpdir.join('missing.dbf'))) is None
