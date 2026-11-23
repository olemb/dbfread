import shutil
import struct
from pytest import raises, mark
from dbfread import DBF
from dbfread import MissingMemoFile

def test_missing_memofile():
    with raises(MissingMemoFile):
        DBF('tests/cases/no_memofile.dbf')

    # This should succeed.
    table = DBF('tests/cases/no_memofile.dbf', ignore_missing_memofile=True)

    # Memo fields should be returned as None.
    record = next(iter(table))
    assert record['MEMO'] is None


@mark.parametrize('dbversion', [0x30, 0x31, 0x32])
@mark.parametrize('load', [False, True])
@mark.parametrize('raw', [False, True])
def test_vfp_double_without_memofile(tmpdir, dbversion, load, raw):
    filename = str(tmpdir.join('double.dbf'))
    shutil.copyfile('tests/cases/vfp_double.dbf', filename)
    with open(filename, 'r+b') as outfile:
        outfile.write(struct.pack('B', dbversion))

    table = DBF(filename, load=load, raw=raw)
    assert table.memofilename is None
    expected = [1.25, -2.5, 0.0]
    if raw:
        expected = [struct.pack('<d', value) for value in expected]
    assert [record['VALUE'] for record in table] == expected


@mark.parametrize('load', [False, True])
def test_vfp_double_with_memo(load):
    table = DBF('tests/cases/vfp_double_memo.dbf', load=load)
    assert list(table) == [{'VALUE': 1.25, 'MEMO': u'memo text'}]


def test_vfp_double_with_missing_memo(tmpdir):
    filename = str(tmpdir.join('double_memo.dbf'))
    shutil.copyfile('tests/cases/vfp_double_memo.dbf', filename)
    with raises(MissingMemoFile):
        DBF(filename)

    table = DBF(filename, ignore_missing_memofile=True)
    assert list(table) == [{'VALUE': 1.25, 'MEMO': None}]


@mark.parametrize('load', [False, True])
def test_dbase_binary_requires_memofile(tmpdir, load):
    filename = str(tmpdir.join('binary.dbf'))
    # A dBASE IV B field contains a ten-byte ASCII memo block index.
    header = struct.pack('<BBBBIHH20x', 0x8b, 120, 1, 1, 1, 65, 11)
    field = struct.pack('<11sc4xBB14x', b'BINARY', b'B', 10, 0)
    with open(filename, 'wb') as outfile:
        outfile.write(header + field + b'\r' + b'          1\x1a')

    with raises(MissingMemoFile):
        DBF(filename, load=load)
    table = DBF(filename, load=load, ignore_missing_memofile=True)
    assert list(table) == [{'BINARY': None}]

    with open(str(tmpdir.join('binary.dbt')), 'wb') as outfile:
        data = b'binary memo\x1f'
        memo = struct.pack('<II', 0x0008ffff, len(data) + 8) + data
        outfile.write(b'\0' * 512 + memo.ljust(512, b'\0'))
    table = DBF(filename, load=load)
    assert list(table) == [{'BINARY': b'binary memo'}]
