import hashlib
import mimetypes
import os
import tempfile
from pathlib import Path
from typing import Sequence

from peewee import IntegrityError

from src.archives import ZipArchiveExtractor
from src.db_models import Metadata as MetadataModel
from src.metadata import Fb2MetadataExtractor

mimetypes.add_type("application/fb2+xml", ".fb2")


def index_files(filenames: Sequence[tuple[str, str]]) -> None:
    for filename, virtual_filename in filenames:
        if os.path.isdir(filename):
            contents = [(Path(filename) / name, Path(virtual_filename) / name) for name in os.listdir(filename)]
            index_files(contents)
            continue

        filetype = mimetypes.guess_type(filename)[0]
        match filetype:
            case "application/fb2+xml":
                try:
                    meta = Fb2MetadataExtractor.extract_metadata(str(filename))
                except Exception as exc:
                    print(f"Unable to extract metadata from {virtual_filename}, skipping")
                    continue
            case "application/zip":
                with tempfile.TemporaryDirectory() as dir:
                    print(f"Processing archive {filename}...")
                    ZipArchiveExtractor.extract_archive(filename, dir)
                    contents = [(Path(dir) / name, Path(virtual_filename) / name) for name in os.listdir(dir)]
                    index_files(contents)
                continue
            case _:
                print(f"Unknown filetype for file {virtual_filename}, skipping")
                continue

        hash = hashlib.sha256()
        hash.update(
            f"{meta.title}:{meta.author_list}:{meta.translator_list}:{meta.series}:{meta.lang}:{meta.format}".encode()
        )
        try:
            MetadataModel.create(
                title=meta.title,
                author_list=meta.author_list,
                translator_list=meta.translator_list,
                series=meta.series,
                lang=meta.lang,
                format=meta.format,
                hash=hash.hexdigest(),
                virtual_filename=os.path.abspath(virtual_filename),
            )
            print(f"Indexed book {virtual_filename} ({meta.author_list} - {meta.title})")
        except IntegrityError:
            print(f"Book {virtual_filename} ({meta.author_list} - {meta.title}) is already indexed, skipping")
