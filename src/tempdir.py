import shutil
import sys
import tempfile
from contextlib import contextmanager


@contextmanager
def tempdir():
    path = tempfile.mkdtemp(prefix="book-indexer-")
    try:
        yield path
    finally:
        try:
            shutil.rmtree(path)
        except IOError:
            sys.stderr.write("Failed to clean up temp dir {}".format(path))
