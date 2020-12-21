from pytest import raises
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
