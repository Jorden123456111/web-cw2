from src.search import SearchEngine


def build_engine() -> SearchEngine:
    index = {
        "good": {
            "doc1": {"freq": 2, "positions": [0, 3]},
            "doc2": {"freq": 1, "positions": [1]},
        },
        "friends": {
            "doc1": {"freq": 1, "positions": [2]},
            "doc3": {"freq": 1, "positions": [0]},
        },
    }
    meta = {"doc1": {"length": 5}, "doc2": {"length": 3}, "doc3": {"length": 2}}
    return SearchEngine(index=index, doc_meta=meta)


def test_print_word_case_insensitive() -> None:
    engine = build_engine()
    postings = engine.print_word("GOOD")
    assert set(postings.keys()) == {"doc1", "doc2"}


def test_find_single_term_returns_ranked_results() -> None:
    engine = build_engine()
    results = engine.find("good")
    assert [r.doc_id for r in results] == ["doc1", "doc2"]


def test_find_multi_term_uses_and_logic() -> None:
    engine = build_engine()
    results = engine.find("good friends")
    assert len(results) == 1
    assert results[0].doc_id == "doc1"


def test_find_empty_or_missing_returns_empty() -> None:
    engine = build_engine()
    assert engine.find("   ") == []
    assert engine.find("missing") == []

