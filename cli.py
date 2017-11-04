#!/usr/bin/env python3

from threedb import connect
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tags", nargs="+")
parser.add_argument("path")
args = parser.parse_args()

db = connect(args.path)
for item in db.search(*tuple(args.tags or [])):
    print(item)
