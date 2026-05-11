"""Persistence for index artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def save_index(
    path: str,
    *,
    start_url: str,
    delay_seconds: float,
    scope: str,
    pages_visited: List[str],
    crawl_errors: Dict[str, str],
    index: Dict[str, Dict[str, Dict[str, int | List[int]]]],
    doc_meta: Dict[str, Dict[str, int | str]],
) -> None:
    """Save full index bundle to JSON."""
    bundle = {
        "metadata": {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "start_url": start_url,
            "delay_seconds": delay_seconds,
            "scope": scope,
            "num_docs": len(doc_meta),
            "num_terms": len(index),
        },
        "pages_visited": pages_visited,
        "crawl_errors": crawl_errors,
        "doc_meta": doc_meta,
        "index": index,
    }
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")


def load_index(path: str) -> Dict[str, object]:
    """Load index bundle JSON."""
    content = Path(path).read_text(encoding="utf-8")
    return json.loads(content)

