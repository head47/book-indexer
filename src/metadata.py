from abc import ABC, abstractmethod
from dataclasses import dataclass

import ebookmeta


@dataclass
class Metadata:
    title: str
    author_list: str
    translator_list: str
    series: str
    lang: str
    format: str


class MetadataExtractor(ABC):
    @staticmethod
    @abstractmethod
    def extract_metadata(filename: str) -> Metadata: ...


class Fb2MetadataExtractor(MetadataExtractor):
    @staticmethod
    def extract_metadata(filename: str) -> Metadata:
        ebook_meta = ebookmeta.get_metadata(filename)
        meta = Metadata(
            title=ebook_meta.title,
            author_list=", ".join(ebook_meta.author_list),
            translator_list=", ".join(ebook_meta.translator_list),
            series=ebook_meta.series,
            lang=ebook_meta.lang,
            format=ebook_meta.format,
        )
        return meta
