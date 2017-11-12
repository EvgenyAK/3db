
from threedb import SimpleStorage


def test_init_storage_without_schema():
    stor = SimpleStorage(".", schema=None)
    assert not stor._schema


def test_init_storage_with_schema():
    schema = {
        'schema': {
            'data': {
                'load': 'file_path',
                'match': ['data.*']},
            'etalon': {
                'load': 'file_path',
                'match': ['etalon.*'],
                'type': 'text'}
        }
    }
    stor = SimpleStorage(".", schema=schema)
    assert stor._schema == schema


def test_read_empty(tmpdir):
    stor = SimpleStorage(str(tmpdir))
    assert not stor.read()


def test_read_single_file(tmpdir):
    f = tmpdir.mkdir("0001_TestData").join("0001_data.txt")
    text = "lala"
    f.write("lala")
    stor = SimpleStorage(str(tmpdir))
    assert stor.read()[0]["0001_data_txt"].text == text
