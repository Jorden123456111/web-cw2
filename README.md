# Coursework 2: Search Engine Tool

Python command-line search tool for `COMP/XJCO3011` coursework.

## Project Overview
This project crawls pages from `https://quotes.toscrape.com/`, builds an inverted index with term statistics, stores the index to disk, and supports searching via CLI commands.

The tool supports:
- `build`: crawl + index + persist
- `load`: load stored index from file
- `print`: print postings for one word
- `find`: search single or multi-word queries (case-insensitive)

## Repository Structure
```text
src/
  crawler.py
  indexer.py
  search.py
  storage.py
  main.py
tests/
  test_crawler.py
  test_indexer.py
  test_search.py
  test_storage.py
  test_main_cli.py
data/
requirements.txt
README.md
```

## Setup
```powershell
python -m pip install -r requirements.txt
```

## Usage
Run from repository root:

```powershell
python -m src.main build
python -m src.main load
python -m src.main print nonsense
python -m src.main find good friends
```

Offline demo fallback (if network/proxy blocks crawling):
```powershell
python -m src.main --index-path data/sample_index.json load
python -m src.main --index-path data/sample_index.json print good
python -m src.main --index-path data/sample_index.json find good friends
```

Optional build controls:
```powershell
python -m src.main build --delay 6 --max-pages 20 --scope quotes --index-path data/index.json
```

Arguments:
- `--delay`: politeness window in seconds (default `6`)
- `--max-pages`: maximum number of pages to crawl
- `--scope quotes|all`:
  - `quotes`: only `/` and `/page/N` pages on the same domain
  - `all`: all same-domain pages
- `--index-path`: output JSON path for compiled index

## Testing
```powershell
pytest -q
```

If `pytest-cov` is available:
```powershell
pytest --cov=src --cov-report=term-missing
```

## Index Format
The saved `data/index.json` includes:
- `metadata` (build time, start URL, politeness delay, scope, term/doc counts)
- `pages_visited`
- `crawl_errors`
- `doc_meta`
- `index`

Inverted index format:
```json
{
  "word": {
    "doc_id": {
      "freq": 3,
      "positions": [5, 18, 90]
    }
  }
}
```

## Design Decisions
- **Crawler strategy**: BFS traversal with same-domain filtering and strict inter-request delay.
- **Tokenization**: lower-cased regex tokens for case-insensitive matching.
- **Search semantics**: multi-word `find` uses AND semantics and TF-IDF ranking.
- **Defensive behavior**: network errors recorded and reported; empty query handling.

## Notes for Assessment Video
- Demonstrate all 4 commands.
- Show edge cases: non-existent word, empty query.
- Show tests running.
- Show Git commit history with incremental development.
- Include GenAI critical reflection with concrete examples.

