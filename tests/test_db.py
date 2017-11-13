
from threedb import ThreeDB


def test_read_empty(tmpdir):
    db = ThreeDB(str(tmpdir))
    assert not db.search()
