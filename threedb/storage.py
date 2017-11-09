
from os.path import join, exists, basename
from .filter import Filter
from .config import Config
from .utils import *
import itertools
import yaml
import os
import re


METADATA = "metadata.yaml"


def _read_tags(metadata):
    if exists(metadata):
        with open(metadata, "r") as fd:
            metadata = yaml.load(fd)
            tags = metadata["tags"]
            return tags


def _filter_rows(rows, strict=False, *tags):
    if not tags:
        return rows

    filtered = []
    tags = set(tags)
    for row in rows:
        index = [row["doc_id"]]
        path = row["tags"] or []
        data_tags = set(index) | set(path)

        if strict:
            if not bool(tags - data_tags):
                filtered.append(row)
                continue
            continue

        if (data_tags & tags):
            filtered.append(row)

    return filtered


class _BaseStorage:

    def __init__(self, storage_path, schema=None):
        self._storage_path = storage_path
        self._schema = schema


class Document(dict):

    def __init__(self, **kwargs):
        super(Document, self).__init__(self)
        self.update(**kwargs)


Element = Document


def _match_files_by_pattern(files, pattern):
    for file in files:
        if re.findall(pattern, file):
            yield file


def _loader(root, files):
    print(files)
    for file in files:
        print(file)
        fp = join(root, file)
        with open(fp) as fd:
            yield fd.read()


class SimpleStorage(_BaseStorage):

    def __init__(self, *args, **kwargs):
        _BaseStorage.__init__(self, *args, **kwargs)

    def _impose_scheme(self, schema, root, files):
        res = {}
        schema = self._schema
        for field in schema:
            match = Filter().regxp_filter(files, schema[field]["match"])
            print(match)
            if match:
                res[field] = _loader(root, match)
        return res

    def read(self):
        res = []
        for root, _, files in os.walk(self._storage_path):
            if files:
                fields = self._impose_scheme(self._schema, root, files)
                elem = Element(
                    index=basename(root),
                    rex=root,
                    tags=_read_tags(join(root, METADATA)),
                    **fields
                )

                res.append(elem)
        return res

simple_storage = SimpleStorage


class StorageProxy:

    def __init__(self, config, storage):
        self._config = config or Config()
        self._storage = storage

    def read(self):
        return self._storage.read()


class ThreeDB:

    def __init__(self, path, config=None, schema=None,
                 storage_type=simple_storage):
        self._config = config or Config()
        self._path = path
        self._storage = StorageProxy(
            self._config,
            storage_type(self._path, schema=schema))
        self._filter = filter or Filter()

    def search(self, strict=False, *tags):
        rows = self._storage.read()
        if not tags:
            return rows
        return _filter_rows(rows, strict, *tags)


connect = ThreeDB


if __name__ == '__main__':
    from pprint import pprint

    path = "test"
    config = {
        'ignore': ['^[0-9]'],
        'schema': {
            'data': {
                'load': False, 'match': ['data.[0-9]']},
            'etalon': {
                'load': True,
                'match': ['etalon.[0-9]'],
                'type': 'text'}}}

    db = ThreeDB(path, schema=config["schema"])
    rows = db.search()
    for row in rows:
        print(row)
        print([item for item in row["data"]])  # read data
