import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from peewee import Database

from src.db_models import Metadata as MetadataModel
from src.metadata import Fb2MetadataExtractor

mimetypes.add_type("application/fb2+xml", ".fb2")

DEBUG = True


def index_files(filenames: Sequence[tuple[str, str]]) -> None:
    for filename, virtual_filename in filenames:
        if os.path.isdir(filename):
            contents = [(Path(filename) / name, Path(virtual_filename) / name) for name in os.listdir(filename)]
            index_files(filenames=contents)
            continue

        filetype = mimetypes.guess_type(filename)[0]
        match filetype:
            case "application/fb2+xml":
                meta = Fb2MetadataExtractor.extract_metadata(str(filename))
            case _:
                print(f"Unknown filetype for file {virtual_filename}, skipping")
                continue

        _, created = MetadataModel.get_or_create(
            title=meta.title,
            author_list=meta.author_list,
            series=meta.series,
            lang=meta.lang,
            format=meta.format,
            virtual_filename=virtual_filename,
        )
        if DEBUG:
            if created:
                print(f"Saved book {virtual_filename} ({meta.author_list} - {meta.title})")
            else:
                print(f"Book {virtual_filename} ({meta.author_list} - {meta.title}) is already indexed, skipping")
