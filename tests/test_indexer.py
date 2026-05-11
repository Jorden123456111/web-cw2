from src.indexer import build_inverted_index, tokenize


def test_tokenize_case_insensitive() -> None:
    text = "Good, good! FRIENDS aren't bad."
    assert tokenize(text) == ["good", "good", "friends", "aren't", "bad"]


def test_build_inverted_index_stores_freq_and_positions() -> None:
    pages = {
        "doc1": "good friends and good books",
        "doc2": "good habits",
    }
    index, meta = build_inverted_index(pages)

    assert meta["doc1"]["length"] == 5
    assert index["good"]["doc1"]["freq"] == 2
    assert index["good"]["doc1"]["positions"] == [0, 3]
    assert index["good"]["doc2"]["freq"] == 1
    assert index["friends"]["doc1"]["positions"] == [1]

