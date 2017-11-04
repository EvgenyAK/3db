
from os.path import join, exists
import itertools
import glob
import yaml
import os


def _read_tags(self, path, metadata_file):
    """
    cat metadata.yaml
    tags:
        - ci
    """
    meta_path = join(path, metadata_file)
    if exists(meta_path):
        with open(meta_path, "r") as fd:
            metadata = yaml.load(fd)
            tags = metadata["tags"]
            return tags


def _filter_rows(self, rows, tags=None):
    if None:
        yield rows

    tags = set([tags] if type(tags) == str else tags)

    for row in rows:
        index = [row[0]]
        path = row[2] or []
        data_tags = set(index) + set(path)

        if not (data_tags - tags):
            yield row


class _BaseStorage:

    def __init__(self, storage):
        self.storage = storage


class SimpleStorage(_BaseStorage):

    def __init__(self, *args, **kwargs):
        _BaseStorage.__init__(self, *args, **kwargs)

    def read(self):
        """
        [(dirname, data_path, tags or None, data_iterator), ...]
        """
        res = []
        for folder in os.listdir(self.storage):
            dir = join(self.storage, folder)
            res.append((
                folder,
                dir,
                glob.iglob(join(dir, "*")))
            )
        return res

    def load(self, tags):
        pass


simple_storage = SimpleStorage


def TreeStorage(_BaseStorage):
    pass


class ThreeDB:

    def __init__(self, storage, storage_type=simple_storage):
        self._storage = storage
        self._storage_type = storage_type(self._storage)

    def search(self, tags=None):
        return _filter_rows()

    def load(self, tags):
        pass

connect = ThreeDB

if __name__ == '__main__':
    path = "test"
    stor = SimpleStorage(path)

    for row in stor.read():
        print(row)
