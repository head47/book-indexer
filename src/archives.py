from abc import ABC, abstractmethod
from zipfile import ZipFile


class ArchiveExtractor(ABC):
    @staticmethod
    @abstractmethod
    def extract_archive(filename: str, output_folder: str): ...

    @staticmethod
    @abstractmethod
    def extract_archive_member(filename: str, member_name: str, output_folder: str) -> str: ...


class ZipArchiveExtractor(ArchiveExtractor):
    @staticmethod
    def extract_archive(filename: str, output_folder: str) -> None:
        with ZipFile(filename) as archive:
            archive.extractall(path=output_folder)

    @staticmethod
    def extract_archive_member(filename: str, member_name: str, output_folder: str) -> str:
        with ZipFile(filename) as archive:
            return archive.extract(member=member_name, path=output_folder)
