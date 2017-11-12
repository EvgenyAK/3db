#!/usr/bin/env python3

from threedb import connect, load_config
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tags", nargs="+")
parser.add_argument("-c", "--config")
parser.add_argument("-s", "--strict", action="store_true")
parser.add_argument("path")
args = parser.parse_args()

config = load_config(args.config)
db = connect(args.path, config=config)
for item in db.search(args.strict, *tuple(args.tags or [])):
    print(item)
