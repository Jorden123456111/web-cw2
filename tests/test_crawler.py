from __future__ import annotations

from typing import Dict

import requests

from src.crawler import Crawler, is_quotes_listing_path, normalize_url


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, pages: Dict[str, str], fail_url: str | None = None) -> None:
        self.pages = pages
        self.fail_url = fail_url
        self.calls: list[str] = []

    def get(self, url: str, timeout: float, headers: Dict[str, str]) -> FakeResponse:
        self.calls.append(url)
        if self.fail_url and url == self.fail_url:
            raise requests.ConnectionError("network down")
        text = self.pages.get(url)
        if text is None:
            return FakeResponse("not found", status_code=404)
        return FakeResponse(text)


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def now(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


def test_normalize_url_and_scope_helper() -> None:
    assert normalize_url("HTTPS://quotes.toscrape.com/page/1/?a=1#x") == "https://quotes.toscrape.com/page/1"
    assert is_quotes_listing_path("/")
    assert is_quotes_listing_path("/page/2")
    assert not is_quotes_listing_path("/author/abc")


def test_crawler_quotes_scope_and_delay() -> None:
    base = "https://quotes.toscrape.com"
    pages = {
        f"{base}/": '<a href="/page/1/">Next</a><a href="/author/a/">Author</a><p>Hello World</p>',
        f"{base}/page/1": '<a href="/page/2/">Next</a><p>Second page text</p>',
        f"{base}/page/2": "<p>Final page</p>",
        f"{base}/author/a": "<p>Author profile should be excluded in quotes scope</p>",
    }
    session = FakeSession(pages)
    clock = FakeClock()

    crawler = Crawler(
        f"{base}/",
        delay_seconds=6.0,
        max_pages=10,
        scope="quotes",
        session=session,  # type: ignore[arg-type]
        sleeper=clock.sleep,
        clock=clock.now,
    )
    out = crawler.crawl()
    assert set(out.pages.keys()) == {f"{base}/", f"{base}/page/1", f"{base}/page/2"}
    assert f"{base}/author/a" not in out.pages
    assert clock.value >= 12.0


def test_crawler_records_errors() -> None:
    base = "https://quotes.toscrape.com"
    pages = {
        f"{base}/": '<a href="/page/1/">Next</a><p>Start</p>',
    }
    session = FakeSession(pages, fail_url=f"{base}/page/1")
    crawler = Crawler(
        f"{base}/",
        delay_seconds=0,
        max_pages=5,
        scope="quotes",
        session=session,  # type: ignore[arg-type]
    )
    out = crawler.crawl()
    assert f"{base}/" in out.pages
    assert f"{base}/page/1" in out.errors

