#!/usr/bin/env python3

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tags", nargs="+")
parser.add_argument("-s", "--strict", action="store_true")
parser.add_argument("path")
args = parser.parse_args()

db = connect(args.path)
for item in db.search(args.strict, *tuple(args.tags or [])):
    print(item)
