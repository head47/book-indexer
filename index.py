#!/usr/bin/env python3
import json
import os
from pathlib import Path
from sys import argv

from src import db_init, indexer
from src.config import Config


def print_usage() -> None:
    print(f"Usage: {argv[0]} <file | directory>")


def main():
    if len(argv) <= 1:
        print_usage()
        raise SystemExit

    config_file = Path(os.path.dirname(os.path.realpath(__file__))) / "config.json"
    with open(config_file) as cf:
        config = Config.from_dict(json.load(cf))
    database = db_init.from_config(config)

    print("Starting processing...")
    filenames = argv[1:]

    indexer.index_files([(fn, fn) for fn in filenames])

    print("Finished processing.")
    database.close()


if __name__ == "__main__":
    main()
