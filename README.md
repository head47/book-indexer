# Book Indexer

Indexes metadata of books into a database, allowing one to easily search them.

Currently supported book formats:
* fb2

Currently supported archive formats:
* zip

## Usage

1. Copy `config.example.json` to `config.json`, configure PostgreSQL there
2. Run `indexer.py` on your collection: `indexer.py <file | directory>`
3. Run `search.py` with your query: `search.py [-t <title>] [-a <author>] [--translator <translator>] [-s <series>] [-f <format>] [-l <lang>] [query]`
