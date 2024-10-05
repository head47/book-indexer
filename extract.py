#!/usr/bin/env python3
import json
import os
from pathlib import Path
from sys import argv

from src import db_init, extractor
from src.db_models import Metadata as MetadataModel


def print_usage() -> None:
    print(f"Usage: {argv[0]} <book IDs...>")


def main():
    if len(argv) <= 1:
        print_usage()
        raise SystemExit

    book_ids = [int(arg) for arg in argv[1:]]
    config_file = Path(os.path.dirname(os.path.realpath(__file__))) / "config.json"
    with open(config_file) as cf:
        config = json.load(cf)
    database = db_init.from_config(config)

    for id in book_ids:
        book = MetadataModel.get(MetadataModel.id == id)
        output_prefix = f"{book.title}-{book.id}-"
        output_file = extractor.extract(book.virtual_filename, output_prefix)
        print(f"Extracted {book.title} to '{output_file}'")

    database.close()


if __name__ == "__main__":
    main()
