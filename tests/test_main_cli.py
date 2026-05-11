import json
import subprocess
import sys
from pathlib import Path

from src.main import SearchApp


def write_sample_index(path: Path) -> None:
    bundle = {
        "metadata": {"num_docs": 2, "num_terms": 2, "created_at_utc": "now"},
        "pages_visited": [],
        "crawl_errors": {},
        "doc_meta": {"doc1": {"length": 3}, "doc2": {"length": 2}},
        "index": {
            "good": {"doc1": {"freq": 1, "positions": [0]}, "doc2": {"freq": 1, "positions": [1]}},
            "friends": {"doc1": {"freq": 1, "positions": [2]}},
        },
    }
    path.write_text(json.dumps(bundle), encoding="utf-8")


def test_load_missing_file_raises(tmp_path: Path) -> None:
    app = SearchApp(index_path=str(tmp_path / "missing.json"))
    try:
        app.cmd_load()
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError")


def test_print_and_find_commands(capsys, tmp_path: Path) -> None:
    index_path = tmp_path / "index.json"
    write_sample_index(index_path)
    app = SearchApp(index_path=str(index_path))

    app.cmd_print("good")
    out = capsys.readouterr().out
    assert "doc1" in out and "doc2" in out

    app.cmd_find("good friends")
    out2 = capsys.readouterr().out
    assert "Found 1 documents" in out2
    assert "doc1" in out2

    app.cmd_find("   ")
    out3 = capsys.readouterr().out
    assert "Empty query is not allowed." in out3


def test_cli_accepts_index_path_after_subcommand(tmp_path: Path) -> None:
    index_path = tmp_path / "index.json"
    write_sample_index(index_path)
    cmd = [
        sys.executable,
        "-m",
        "src.main",
        "load",
        "--index-path",
        str(index_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "Loaded index:" in result.stdout
