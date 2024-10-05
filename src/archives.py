from abc import ABC, abstractmethod
from zipfile import ZipFile


class ArchiveExtractor(ABC):
    @staticmethod
    @abstractmethod
    def extract_archive(filename: str, output_folder: str): ...


class ZipArchiveExtractor(ArchiveExtractor):
    @staticmethod
    def extract_archive(filename: str, output_folder: str) -> None:
        with ZipFile(filename) as archive:
            archive.extractall(path=output_folder)
