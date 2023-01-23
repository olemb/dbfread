from dbfread import DBF

def test_scx() -> None:
    ''' Assert that an SCX file can be loaded properly'''

    # Associated SCT file should automatically be detected.
    dbf = DBF('tests/cases/form.scx', load=True)

    # First record has a special memo field that should survive.
    assert dbf.records[0]['RESERVED1'] == 'VERSION =   3.00'

    # Other records store information in memo fields.
    assert dbf.records[1]['PROPERTIES'] == (
        'Top = 0\r\nLeft = 0\r\nWidth = 0\r\nHeight = 0\r\n'
        'DataSource = .NULL.\r\nName = "Dataenvironment"\r\n'
    )