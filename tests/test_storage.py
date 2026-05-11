from pathlib import Path

from src.storage import load_index, save_index


def test_save_and_load_index_roundtrip(tmp_path: Path) -> None:
    output = tmp_path / "index.json"
    save_index(
        str(output),
        start_url="https://quotes.toscrape.com/",
        delay_seconds=6.0,
        scope="quotes",
        pages_visited=["https://quotes.toscrape.com/"],
        crawl_errors={},
        index={"good": {"doc1": {"freq": 1, "positions": [0]}}},
        doc_meta={"doc1": {"length": 1, "title": "doc1"}},
    )
    bundle = load_index(str(output))
    assert bundle["metadata"]["num_docs"] == 1
    assert bundle["metadata"]["num_terms"] == 1
    assert bundle["index"]["good"]["doc1"]["freq"] == 1

