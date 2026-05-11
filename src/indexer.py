"""Indexer module for building inverted index structures."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")


def tokenize(text: str) -> List[str]:
    """Tokenize text into lower-cased words."""
    return [match.group(0).lower() for match in WORD_PATTERN.finditer(text)]


def build_inverted_index(
    pages: Dict[str, str],
) -> Tuple[Dict[str, Dict[str, Dict[str, List[int] | int]]], Dict[str, Dict[str, int | str]]]:
    """
    Build inverted index:
    word -> doc -> {"freq": int, "positions": [int, ...]}
    Also returns doc metadata.
    """
    inverted: DefaultDict[str, Dict[str, Dict[str, List[int] | int]]] = defaultdict(dict)
    doc_meta: Dict[str, Dict[str, int | str]] = {}

    for doc_id, content in pages.items():
        tokens = tokenize(content)
        doc_meta[doc_id] = {"length": len(tokens), "title": doc_id}
        for pos, token in enumerate(tokens):
            posting = inverted[token].setdefault(doc_id, {"freq": 0, "positions": []})
            posting["freq"] = int(posting["freq"]) + 1
            positions = posting["positions"]
            if isinstance(positions, list):
                positions.append(pos)

    return dict(inverted), doc_meta

