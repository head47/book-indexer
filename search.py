#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
from sys import argv

from prettytable import PrettyTable

from src import db_init, searcher
from src.config import Config


def print_usage() -> None:
    print(
        f"No filters specified. Usage: {argv[0]} [-t <title>] [-a <author>] [--translator <translator>] [-s <series>] [-f <format>] [-l <lang>] [query]"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title")
    parser.add_argument("-a", "--author")
    parser.add_argument("--translator")
    parser.add_argument("-s", "--series")
    parser.add_argument("-f", "--format"),
    parser.add_argument("-l", "--lang")
    parser.add_argument("query", nargs="?", default=None)

    args = parser.parse_args()

    config_file = Path(os.path.dirname(os.path.realpath(__file__))) / "config.json"
    with open(config_file) as cf:
        config = Config.from_dict(json.load(cf))
    database = db_init.from_config(config)

    print("Searching...")
    max_results = 100
    try:
        results = searcher.search(
            title=args.title,
            author=args.author,
            translator=args.translator,
            series=args.series,
            format=args.format,
            lang=args.lang,
            query=args.query,
            max_results=max_results,
        )
    except searcher.NoFiltersException:
        print_usage()
        database.close()
        raise SystemExit

    if len(results) == 100:
        print(f"Found {len(results)}+ results.")
    else:
        print(f"Found {len(results)} results.")

    table = PrettyTable()
    table.field_names = ["ID", "Title", "Authors", "Translators", "Series", "Lang", "Format", "Filename"]
    for book in results:
        table.add_row(
            [
                book.id,
                book.title,
                book.author_list,
                book.translator_list,
                book.series,
                book.lang,
                book.format,
                book.virtual_filename,
            ]
        )

    print(table)

    database.close()


if __name__ == "__main__":
    main()
