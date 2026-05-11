"""Crawler module for the coursework search tool."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from time import monotonic, sleep
from typing import Callable, Deque, Dict, List, Optional, Set
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests

USER_AGENT = "COMP3011-SearchTool/1.0"


def normalize_url(url: str) -> str:
    """Normalize URL by removing query/fragment and normalizing trailing slash."""
    parts = urlsplit(url)
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))


def is_quotes_listing_path(path: str) -> bool:
    """Return True for quote listing pages: / or /page/<number>."""
    if path == "/":
        return True
    pieces = path.strip("/").split("/")
    return len(pieces) == 2 and pieces[0] == "page" and pieces[1].isdigit()


class _LinkTextParser(HTMLParser):
    """Lightweight parser collecting links and visible text."""

    def __init__(self) -> None:
        super().__init__()
        self.links: List[str] = []
        self.text_chunks: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
            return
        if tag == "a":
            attr_map = dict(attrs)
            href = attr_map.get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        cleaned = " ".join(data.split())
        if cleaned:
            self.text_chunks.append(cleaned)


@dataclass
class CrawlOutput:
    """Crawler output."""

    pages: Dict[str, str] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)
    visited_order: List[str] = field(default_factory=list)


class Crawler:
    """Breadth-first crawler with politeness window."""

    def __init__(
        self,
        start_url: str,
        *,
        delay_seconds: float = 6.0,
        timeout_seconds: float = 10.0,
        max_pages: int = 20,
        scope: str = "quotes",
        session: Optional[requests.Session] = None,
        sleeper: Optional[Callable[[float], None]] = None,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        if scope not in {"quotes", "all"}:
            raise ValueError("scope must be 'quotes' or 'all'")
        self.start_url = normalize_url(start_url)
        self.delay_seconds = float(delay_seconds)
        self.timeout_seconds = float(timeout_seconds)
        self.max_pages = int(max_pages)
        self.scope = scope
        self.session = session or requests.Session()
        if hasattr(self.session, "trust_env"):
            self.session.trust_env = False
        self.sleeper = sleeper or sleep
        self.clock = clock or monotonic
        self.start_domain = urlsplit(self.start_url).netloc

    def _is_allowed(self, url: str) -> bool:
        parts = urlsplit(url)
        if parts.scheme not in {"http", "https"}:
            return False
        if parts.netloc != self.start_domain:
            return False
        if self.scope == "all":
            return True
        return is_quotes_listing_path(parts.path or "/")

    def crawl(self) -> CrawlOutput:
        """Crawl pages and return page text + errors."""
        output = CrawlOutput()
        queue: Deque[str] = deque([self.start_url])
        visited: Set[str] = set()
        enqueued: Set[str] = {self.start_url}
        last_request_at: Optional[float] = None

        while queue and len(output.pages) < self.max_pages:
            url = queue.popleft()
            if url in visited:
                continue
            visited.add(url)

            if last_request_at is not None:
                elapsed = self.clock() - last_request_at
                remaining = self.delay_seconds - elapsed
                if remaining > 0:
                    self.sleeper(remaining)

            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout_seconds,
                    headers={"User-Agent": USER_AGENT},
                )
                last_request_at = self.clock()
                response.raise_for_status()
            except requests.RequestException as exc:
                output.errors[url] = str(exc)
                continue

            parser = _LinkTextParser()
            parser.feed(response.text)
            parser.close()

            output.pages[url] = " ".join(parser.text_chunks)
            output.visited_order.append(url)

            for href in parser.links:
                absolute = normalize_url(urljoin(url, href))
                if absolute in enqueued or absolute in visited:
                    continue
                if self._is_allowed(absolute):
                    queue.append(absolute)
                    enqueued.add(absolute)

        return output
