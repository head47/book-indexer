import mimetypes
import os
import shutil
import tempfile
from contextvars import ContextVar
from pathlib import Path

from .archives import ZipArchiveExtractor

mimetypes.add_type("application/fb2+xml", ".fb2")

output_dir_cv = ContextVar("output_dir")


class UnsupportedArchiveFormat(Exception): ...


def extract(virtual_filename: str, prefix: str, output_dir: str) -> str:
    output_dir_cv.set(output_dir)
    cur_real_path = Path()
    path_parts = Path(virtual_filename).parts

    return _extract_iteration(path_parts, cur_real_path, 0, prefix)


def _extract_iteration(path_parts: tuple[str], cur_real_path: str, i: int, prefix: str) -> str:
    if i == len(path_parts) - 1:
        cur_real_path /= path_parts[-1]
        filetype = mimetypes.guess_type(cur_real_path)[0]
        match filetype:
            case "application/fb2+xml":
                suffix = ".fb2"
            case _:
                suffix = None
        output = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=output_dir_cv.get())[1]
        shutil.copyfile(cur_real_path, output)
        return output

    poss_real_path = cur_real_path / path_parts[i]
    if os.path.isdir(poss_real_path):
        cur_real_path = poss_real_path
        return _extract_iteration(path_parts, cur_real_path, i + 1, prefix)

    filetype = mimetypes.guess_type(poss_real_path)[0]
    match filetype:
        case "application/zip":
            with tempfile.TemporaryDirectory() as dir:
                cur_real_path = Path(dir)
                Path(ZipArchiveExtractor.extract_archive_member(poss_real_path, path_parts[i + 1], dir))
                return _extract_iteration(path_parts, cur_real_path, i + 1, prefix)
        case _:
            raise UnsupportedArchiveFormat(f"cannot extract {poss_real_path}")
