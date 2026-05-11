"""Search logic for inverted index queries."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Set

from .indexer import tokenize


@dataclass
class SearchResult:
    doc_id: str
    score: float
    matched_terms: int


class SearchEngine:
    """Search engine using AND matching + TF-IDF scoring."""

    def __init__(
        self,
        index: Dict[str, Dict[str, Dict[str, int | List[int]]]],
        doc_meta: Dict[str, Dict[str, int | str]],
    ) -> None:
        self.index = index
        self.doc_meta = doc_meta
        self.num_docs = max(len(doc_meta), 1)

    def print_word(self, word: str) -> Dict[str, Dict[str, int | List[int]]]:
        """Return posting list for a word (case-insensitive)."""
        token = word.lower().strip()
        return self.index.get(token, {})

    def find(self, query: str) -> List[SearchResult]:
        """Find docs containing all query words, ordered by TF-IDF score."""
        terms = tokenize(query)
        if not terms:
            return []
        unique_terms = list(dict.fromkeys(terms))

        posting_sets: List[Set[str]] = []
        for term in unique_terms:
            postings = self.index.get(term)
            if not postings:
                return []
            posting_sets.append(set(postings.keys()))

        matching_docs = set.intersection(*posting_sets) if posting_sets else set()
        if not matching_docs:
            return []

        results: List[SearchResult] = []
        for doc_id in matching_docs:
            score = 0.0
            for term in unique_terms:
                postings = self.index[term]
                entry = postings[doc_id]
                tf = 1.0 + math.log(float(entry["freq"]))
                df = len(postings)
                idf = math.log((self.num_docs + 1) / (df + 1)) + 1.0
                score += tf * idf
            results.append(SearchResult(doc_id=doc_id, score=score, matched_terms=len(unique_terms)))

        results.sort(key=lambda r: (-r.score, r.doc_id))
        return results

