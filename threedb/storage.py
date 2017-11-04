
from os.path import join, exists, basename
from .utils import *
import itertools
import glob
import yaml
import os


METADATA = "metadata.yaml"


def _read_tags(metadata):
    if exists(metadata):
        with open(metadata, "r") as fd:
            metadata = yaml.load(fd)
            tags = metadata["tags"]
            return tags


def _filter_rows(rows, *tags):
    if not tags:
        return rows

    filtered = []
    tags = set(tags)
    for row in rows:
        index = [row[0]]
        path = row[2] or []
        data_tags = set(index) | set(path)

        if (data_tags & tags):
            filtered.append(row)
    return filtered


class _BaseStorage:

    def __init__(self, storage):
        self.storage = storage


class SimpleStorage(_BaseStorage):

    def __init__(self, *args, **kwargs):
        _BaseStorage.__init__(self, *args, **kwargs)

    def read(self):
        res = []
        for root, _, files in os.walk(self.storage):
            files = filter_files([METADATA], files)
            row = (basename(root),
                   root,
                   _read_tags(join(root, METADATA)),
                   files)
            res.append(row)
        return res

    def load(self, row):
        pass


simple_storage = SimpleStorage


class ThreeDB:

    def __init__(self, path, storage_type=simple_storage):
        self._path = path
        self._storage = storage_type(self._path)

    def search(self, *tags):
        rows = self._storage.read()
        if not tags:
            return rows
        return _filter_rows(rows, *tags)

    def load(self, *tags):
        pass

connect = ThreeDB

if __name__ == '__main__':
    path = "test"

    db = ThreeDB(path)
    for item in db.search():
        print(item, [i for i in item[-1]])
