import sqlite3
import tempfile
import urllib.error
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from anki_skill.exporters import (
    _sanitize_tsv,
    export_ankiconnect,
    export_apkg,
    export_tsv,
)
from anki_skill.models import Card


# --- _sanitize_tsv ---


def test_sanitize_tsv_removes_tabs():
    assert _sanitize_tsv("hello\tworld") == "hello world"


def test_sanitize_tsv_converts_newlines_to_br():
    assert _sanitize_tsv("line1\nline2") == "line1<br>line2"


def test_sanitize_tsv_removes_carriage_return():
    assert _sanitize_tsv("line1\r\nline2") == "line1<br>line2"


def test_sanitize_tsv_handles_mixed():
    assert _sanitize_tsv("a\tb\nc\r\nd") == "a b<br>c<br>d"


def test_sanitize_tsv_passthrough_clean_string():
    assert _sanitize_tsv("<b>hello</b>") == "<b>hello</b>"


# --- Helpers ---


def _sample_cards() -> list[Card]:
    return [
        Card(
            question="<b>Q1</b>",
            answer="A1<br><br>nidd123",
            tags=["tag1::sub"],
        ),
        Card(
            question="Q2",
            answer="<ul><li>A2a</li><li>A2b</li></ul>",
            tags=["tag2", "tag3"],
        ),
    ]


# --- TSV export ---


def test_export_tsv_creates_file(tmp_path):
    cards = _sample_cards()
    path = tmp_path / "out.tsv"
    export_tsv(cards, path)
    assert path.exists()
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2


def test_export_tsv_tab_separated(tmp_path):
    cards = _sample_cards()
    path = tmp_path / "out.tsv"
    export_tsv(cards, path)
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    parts = first_line.split("\t")
    assert len(parts) == 3
    assert parts[0] == "<b>Q1</b>"
    assert parts[1] == "A1"  # nidd stripped from answer
    assert "tag1::sub" in parts[2]
    assert "nidd123" in parts[2]  # nidd moved to tags


def test_export_tsv_multiple_tags_space_joined(tmp_path):
    cards = _sample_cards()
    path = tmp_path / "out.tsv"
    export_tsv(cards, path)
    second_line = path.read_text(encoding="utf-8").splitlines()[1]
    parts = second_line.split("\t")
    assert parts[2] == "tag2 tag3"


def test_export_tsv_cloze_card(tmp_path):
    """Cloze cards should export with cloze syntax preserved."""
    cards = [
        Card(
            question="{{c1::Mitochondria}} is the powerhouse of the cell.",
            answer="",
            tags=["biology"],
        )
    ]
    path = tmp_path / "out.tsv"
    export_tsv(cards, path)
    content = path.read_text(encoding="utf-8")
    assert "{{c1::Mitochondria}}" in content


# --- APKG export ---


def test_export_apkg_creates_file(tmp_path):
    cards = _sample_cards()
    path = tmp_path / "out.apkg"
    export_apkg(cards, path, deck_name="Test Deck")
    assert path.exists()
    assert path.stat().st_size > 0


def test_export_apkg_default_deck_name(tmp_path):
    cards = _sample_cards()
    path = tmp_path / "out.apkg"
    export_apkg(cards, path)
    assert path.exists()


def test_export_apkg_preserves_html(tmp_path):
    cards = [Card(question="<b>Bold Q</b>", answer="<i>Italic A</i>", tags=[])]
    path = tmp_path / "out.apkg"
    export_apkg(cards, path, deck_name="HTML Test")
    assert path.stat().st_size > 0


def test_export_apkg_nidd_in_tags(tmp_path):
    """APKG export should move nidd from answer to tags."""
    cards = [
        Card(question="Q", answer="A<br><br>nidd999", tags=["tag1"])
    ]
    path = tmp_path / "out.apkg"
    export_apkg(cards, path, deck_name="nidd test")

    with zipfile.ZipFile(path, "r") as z:
        db_name = [n for n in z.namelist() if n.endswith(".anki2")][0]
        db_bytes = z.read(db_name)

    db_path = tmp_path / "temp.anki2"
    db_path.write_bytes(db_bytes)
    conn = sqlite3.connect(str(db_path))
    row = conn.execute("SELECT tags, flds FROM notes").fetchone()
    conn.close()

    tags_str = row[0]
    flds_str = row[1]
    assert "nidd999" in tags_str
    assert "tag1" in tags_str
    answer_field = flds_str.split("\x1f")[1]
    assert "nidd999" not in answer_field


def test_export_apkg_cloze_card(tmp_path):
    """APKG export should use Cloze model for cloze cards."""
    cards = [
        Card(
            question="{{c1::Mitochondria}} is the powerhouse of the cell.",
            answer="",
            tags=["biology"],
        )
    ]
    path = tmp_path / "out.apkg"
    export_apkg(cards, path, deck_name="Cloze Test")
    assert path.stat().st_size > 0


# --- AnkiConnect export ---


def test_export_ankiconnect_builds_correct_notes():
    """AnkiConnect export should build correct note structure."""
    cards = [
        Card(question="<b>Q1</b>", answer="A1<br><br>nidd123", tags=["tag1"]),
        Card(question="{{c1::Mitochondria}} is X.", answer="", tags=["bio"]),
    ]

    mock_response = MagicMock()
    mock_response.read.return_value = b'{"result": [1, 2], "error": null}'
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("anki_skill.exporters.urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        added = export_ankiconnect(cards, deck_name="Test Deck")

    assert added == 2
    assert mock_urlopen.call_count == 3  # version, createDeck, addNotes


def test_export_ankiconnect_connection_error():
    """Should raise ConnectionError when Anki is not running."""
    cards = [Card(question="Q", answer="A", tags=[])]

    with patch("anki_skill.exporters.urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
        with pytest.raises(ConnectionError, match="Cannot connect"):
            export_ankiconnect(cards)
