# Book Indexer

Indexes metadata of books (that may be in archives) into a database, allowing one to easily search them.

Currently supported book formats:
* fb2

Currently supported archive formats:
* zip

## Setup

Copy `config.example.json` to `config.json`. Configure PostgreSQL credentials there.

## Usage

### Indexing

Run `indexer.py` on your collection: `indexer.py <file | directory>`

### Searching

Run `search.py` with your query: `search.py [-t <title>] [-a <author>] [--translator <translator>] [-s <series>] [-f <format>] [-l <lang>] [query]`

### Extraction

Run `extract.py` with book IDs you found with `search.py`: `extract.py <book IDs...>`
