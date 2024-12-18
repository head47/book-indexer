#!/usr/bin/env python3
import argparse
import json
import os
import tempfile
from pathlib import Path

from src import db_init, extractor
from src.config import Config
from src.db_models import Metadata as MetadataModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default=tempfile.gettempdir())
    parser.add_argument("-b", "--brief", action="store_true", help="only output names of extracted files")
    parser.add_argument("book_ids", nargs="+")
    args = parser.parse_args()

    config_file = Path(os.path.dirname(os.path.realpath(__file__))) / "config.json"
    with open(config_file) as cf:
        config = Config.from_dict(json.load(cf))
    database = db_init.from_config(config)

    for id in args.book_ids:
        book = MetadataModel.get(MetadataModel.id == id)
        output_prefix = f"{book.title}-{book.id}-"
        output_file = extractor.extract(book.virtual_filename, output_prefix, args.output)
        if args.brief:
            print(output_file)
        else:
            print(f"Extracted {book.title} to '{output_file}'")

    database.close()


if __name__ == "__main__":
    main()
