"""Export Card objects to Anki-importable formats."""

from __future__ import annotations

import hashlib
from pathlib import Path

import genanki

from anki_skill.models import Card


def _sanitize_tsv(value: str) -> str:
    """Remove characters that would corrupt TSV structure."""
    return value.replace("\t", " ").replace("\n", "<br>").replace("\r", "")


def export_tsv(cards: list[Card], output_path: Path) -> None:
    """Export cards to TSV format for Anki import.

    Format: question<TAB>answer<TAB>tags (space-separated)
    No header row — Anki's TSV import doesn't use one.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for card in cards:
            tags = card.tags_string
            if card.nidd:
                tags = f"{tags} {card.nidd}".strip()
            q = _sanitize_tsv(card.question)
            a = _sanitize_tsv(card.answer_clean)
            line = f"{q}\t{a}\t{tags}\n"
            f.write(line)


# Stable model ID — must not change between runs
_MODEL_ID = 1607392319
_MODEL = genanki.Model(
    _MODEL_ID,
    "AnkiSkill Basic",
    fields=[
        {"name": "Front"},
        {"name": "Back"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
    css=".card { font-family: arial; font-size: 20px; text-align: left; }"
)

_CLOZE_MODEL_ID = 1607392320
_CLOZE_MODEL = genanki.Model(
    _CLOZE_MODEL_ID,
    "AnkiSkill Cloze",
    model_type=genanki.Model.CLOZE,
    fields=[
        {"name": "Text"},
        {"name": "Extra"},
    ],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "{{cloze:Text}}",
            "afmt": "{{cloze:Text}}<br>{{Extra}}",
        },
    ],
    css=".card { font-family: arial; font-size: 20px; text-align: left; } .cloze { font-weight: bold; color: blue; }",
)


def export_apkg(
    cards: list[Card],
    output_path: Path,
    deck_name: str = "AnkiSkill Export",
) -> None:
    """Export cards to .apkg format using genanki."""
    deck_id = int(hashlib.sha256(deck_name.encode()).hexdigest(), 16) % (2**31)
    deck = genanki.Deck(deck_id, deck_name)

    for card in cards:
        tags = list(card.tags)
        if card.nidd:
            tags.append(card.nidd)
        if card.is_cloze:
            note = genanki.Note(
                model=_CLOZE_MODEL,
                fields=[card.question, card.answer_clean],
                tags=tags,
            )
        else:
            note = genanki.Note(
                model=_MODEL,
                fields=[card.question, card.answer_clean],
                tags=tags,
            )
        deck.add_note(note)

    genanki.Package(deck).write_to_file(str(output_path))
