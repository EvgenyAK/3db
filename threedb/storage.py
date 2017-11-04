
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


def _filter_rows(rows, *tags):
    if not tags:
        return rows

    tags = set(tags)

    filtered = []
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
        for folder in os.listdir(self.storage):
            dir = join(self.storage, folder)
            res.append((
                folder,
                dir,
                None,
                glob.iglob(join(dir, "*")))
            )
        return res


simple_storage = SimpleStorage


def TreeStorage(_BaseStorage):
    pass


class ThreeDB:

    def __init__(self, path, storage_type=simple_storage):
        self._path = path
        self._storage = storage_type(self._path)

    def search(self, *tags):
        rows = self._storage.read()
        if not tags:
            return rows
        return _filter_rows(rows, *tags)

    def load(self, tags):
        pass

connect = ThreeDB
