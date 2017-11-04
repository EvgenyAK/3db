
import itertools
import os


def filter_files(skip, seq):
    filtered = itertools.filterfalse(
        lambda x: x not in skip,
        seq
    )
    return filtered


def normalize_file_name(files):
    return map(lambda x: os.path.basename(x), files)
