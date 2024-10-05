#!/usr/bin/env python3
import json
import os
from pathlib import Path
from sys import argv

from src import indexer
from src.db_models import Metadata as MetadataModel
from src.db_models import database


def print_usage() -> None:
    print(f"Usage: {argv[0]} <file | directory>")


def main():
    match len(argv):
        case 0 | 1:
            print_usage()
            raise SystemExit

    config_file = Path(os.path.dirname(os.path.realpath(__file__))) / "config.json"
    with open(config_file) as cf:
        config = json.load(cf)

    print("Starting processing...")
    filenames = argv[1:]
    database.init(
        config["database"]["db"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        host=config["database"]["host"],
    )
    database.connect()
    database.create_tables((MetadataModel,))

    indexer.index_files([(fn, fn) for fn in filenames])

    print("Finished processing.")
    database.close()


if __name__ == "__main__":
    main()
