from typing import Optional

from peewee import ModelSelect

from src.db_models import Metadata as MetadataModel


class PlaceholderOperator:
    def __and__(self, other):
        return other


class NoFiltersException(Exception): ...


def search(
    title: Optional[str],
    author: Optional[str],
    translator: Optional[str],
    series: Optional[str],
    format: Optional[str],
    lang: Optional[str],
    query: Optional[str],
    max_results: Optional[int],
) -> ModelSelect:
    operators = PlaceholderOperator()
    if title is not None:
        operators &= MetadataModel.title_search.match(title, plain=True)
    if author is not None:
        operators &= MetadataModel.author_list_search.match(author, plain=True)
    if translator is not None:
        operators &= MetadataModel.translator_list_search.match(translator, plain=True)
    if series is not None:
        operators &= MetadataModel.series_search.match(series, plain=True)
    if format is not None:
        operators &= MetadataModel.format == format
    if lang is not None:
        operators &= MetadataModel.lang == lang
    if query is not None:
        operators &= (
            (MetadataModel.title_search.match(query, plain=True))
            | (MetadataModel.author_list_search.match(query, plain=True))
            | (MetadataModel.translator_list_search.match(query, plain=True))
            | (MetadataModel.series_search.match(query, plain=True))
        )
    if isinstance(operators, PlaceholderOperator):
        raise NoFiltersException
    results = MetadataModel.select().where(operators)
    if max_results is not None:
        results = results.limit(max_results)
    return results
