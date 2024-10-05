from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import ebookmeta


@dataclass
class Metadata:
    title: str
    author_list: str
    series: Optional[str]
    lang: str
    format: str


class MetadataExtractor(ABC):
    @classmethod
    @abstractmethod
    def extract_metadata(filename: str) -> Metadata: ...


class Fb2MetadataExtractor(MetadataExtractor):
    def extract_metadata(filename: str) -> Metadata:
        ebook_meta = ebookmeta.get_metadata(filename)
        meta = Metadata(
            title=ebook_meta.title,
            author_list=", ".join(ebook_meta.author_list),
            series=ebook_meta.series if ebook_meta.series != "" else None,
            lang=ebook_meta.lang,
            format=ebook_meta.format,
        )
        return meta
