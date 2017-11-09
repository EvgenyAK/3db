
from os.path import join, exists, basename
from .utils import *
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

    def __init__(self, storage_path):
        self._storage_path = storage_path


class Document(dict):

    def __init__(self, **kwargs):
        super(Document, self).__init__(self)
        self.update(**kwargs)


Element = Document


class SimpleStorage(_BaseStorage):

    def __init__(self, *args, **kwargs):
        _BaseStorage.__init__(self, *args, **kwargs)

    def read(self):
        res = []
        for root, _, files in os.walk(self._storage_path):
            if files:
                row = (basename(root),
                       root,
                       _read_tags(join(root, METADATA)),
                       files)
                res.append(row)
        return res


class Config:
    load_data = True
    alias = {
        "etalon": [
            "etalon.*"
        ],
        "data": [
            "data.*"
        ]
    }

    ignore = [
        "^[0-9]"
    ]


simple_storage = SimpleStorage


class StorageProxy:

    def __init__(self, config, storage):
        self._config = config or Config()
        self._storage = storage

    def read(self):
        res = []
        for each in self._storage.read():
            ignore_pattern = "|".join(self._config.ignore)
            ref = each[1]
            single_doc = Document(doc_id=each[0],
                                  ref=ref,
                                  tags=each[2])

            for file in each[3]:
                if re.findall(ignore_pattern, file):
                    continue

                name = basename(file).replace(".", "_")

                alias = self._config.alias
                for key in alias:
                    pattern = "|".join(alias[key])

                    if re.findall(pattern, file):
                        name = key

                single_doc[name] = read_txt(ref, file)

            res.append(single_doc)
        return res


# class Filter:
#     def filter_by_tags(data_tags, query): pass
#     def ignore(file, ignored): pass


class ThreeDB:

    def __init__(self, path, config=None, storage_type=simple_storage):
        self._config = config or Config()
        self._path = path
        self._storage = StorageProxy(self._config, storage_type(self._path))
        self._filter = filter or Filter()

    def search(self, strict=False, *tags):
        rows = self._storage.read()
        if not tags:
            return rows
        return _filter_rows(rows, strict, *tags)


connect = ThreeDB
