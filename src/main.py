"""CLI entry point for coursework search tool."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .crawler import Crawler
from .indexer import build_inverted_index
from .search import SearchEngine
from .storage import load_index, save_index

DEFAULT_START_URL = "https://quotes.toscrape.com/"
DEFAULT_INDEX_PATH = "data/index.json"


class SearchApp:
    """Stateful CLI app."""

    def __init__(self, index_path: str = DEFAULT_INDEX_PATH) -> None:
        self.index_path = index_path
        self.bundle: Dict[str, Any] | None = None

    def cmd_build(
        self,
        *,
        start_url: str,
        delay_seconds: float,
        max_pages: int,
        scope: str,
    ) -> None:
        crawler = Crawler(
            start_url,
            delay_seconds=delay_seconds,
            max_pages=max_pages,
            scope=scope,
        )
        crawl_output = crawler.crawl()
        index, doc_meta = build_inverted_index(crawl_output.pages)
        save_index(
            self.index_path,
            start_url=start_url,
            delay_seconds=delay_seconds,
            scope=scope,
            pages_visited=crawl_output.visited_order,
            crawl_errors=crawl_output.errors,
            index=index,
            doc_meta=doc_meta,
        )
        print(f"Build completed. Docs: {len(doc_meta)} Terms: {len(index)}")
        print(f"Index saved to {self.index_path}")
        if crawl_output.errors:
            print(f"Crawl completed with {len(crawl_output.errors)} errors.")

    def cmd_load(self) -> None:
        path = Path(self.index_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Index file not found: {self.index_path}. Run 'build' first."
            )
        self.bundle = load_index(self.index_path)
        md = self.bundle.get("metadata", {})
        print(
            "Loaded index:",
            f"docs={md.get('num_docs', 0)}",
            f"terms={md.get('num_terms', 0)}",
            f"created_at_utc={md.get('created_at_utc', 'unknown')}",
        )

    def _get_engine(self) -> SearchEngine:
        if self.bundle is None:
            self.cmd_load()
        assert self.bundle is not None
        return SearchEngine(
            index=self.bundle["index"],  # type: ignore[arg-type]
            doc_meta=self.bundle["doc_meta"],  # type: ignore[arg-type]
        )

    def cmd_print(self, word: str) -> None:
        engine = self._get_engine()
        postings = engine.print_word(word)
        if not postings:
            print(f"No postings found for '{word}'.")
            return
        print(json.dumps(postings, ensure_ascii=False, indent=2))

    def cmd_find(self, query: str) -> None:
        if not query.strip():
            print("Empty query is not allowed.")
            return
        engine = self._get_engine()
        results = engine.find(query)
        if not results:
            print(f"No documents found for query: '{query}'")
            return
        print(f"Found {len(results)} documents for query: '{query}'")
        for rank, item in enumerate(results, start=1):
            print(f"{rank}. {item.doc_id} score={item.score:.4f} matched_terms={item.matched_terms}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Coursework Search Tool CLI")
    parser.add_argument(
        "--index-path",
        default=DEFAULT_INDEX_PATH,
        help="Path to index file (default: data/index.json)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Crawl site and build index")
    p_build.add_argument(
        "--index-path",
        dest="sub_index_path",
        default=None,
        help="Path to index file (also accepted after subcommand)",
    )
    p_build.add_argument("--start-url", default=DEFAULT_START_URL)
    p_build.add_argument("--delay", type=float, default=6.0, help="Politeness delay seconds")
    p_build.add_argument("--max-pages", type=int, default=20)
    p_build.add_argument(
        "--scope",
        choices=["quotes", "all"],
        default="quotes",
        help="quotes: only / and /page/N; all: crawl any same-domain links",
    )

    p_load = sub.add_parser("load", help="Load index from disk")
    p_load.add_argument(
        "--index-path",
        dest="sub_index_path",
        default=None,
        help="Path to index file (also accepted after subcommand)",
    )

    p_print = sub.add_parser("print", help="Print postings for a word")
    p_print.add_argument(
        "--index-path",
        dest="sub_index_path",
        default=None,
        help="Path to index file (also accepted after subcommand)",
    )
    p_print.add_argument("word")

    p_find = sub.add_parser("find", help="Find pages for a query")
    p_find.add_argument(
        "--index-path",
        dest="sub_index_path",
        default=None,
        help="Path to index file (also accepted after subcommand)",
    )
    p_find.add_argument("query", nargs="+")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    effective_index_path = getattr(args, "sub_index_path", None) or args.index_path
    app = SearchApp(index_path=effective_index_path)

    if args.command == "build":
        app.cmd_build(
            start_url=args.start_url,
            delay_seconds=args.delay,
            max_pages=args.max_pages,
            scope=args.scope,
        )
    elif args.command == "load":
        app.cmd_load()
    elif args.command == "print":
        app.cmd_print(args.word)
    elif args.command == "find":
        app.cmd_find(" ".join(args.query))
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
