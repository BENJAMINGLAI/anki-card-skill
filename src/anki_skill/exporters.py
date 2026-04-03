"""Export Card objects to Anki-importable formats."""

from __future__ import annotations

from pathlib import Path

import genanki

from anki_skill.models import Card


def export_tsv(cards: list[Card], output_path: Path) -> None:
    """Export cards to TSV format for Anki import.

    Format: question<TAB>answer<TAB>tags (space-separated)
    No header row — Anki's TSV import doesn't use one.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for card in cards:
            line = f"{card.question}\t{card.answer}\t{card.tags_string}\n"
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


def export_apkg(
    cards: list[Card],
    output_path: Path,
    deck_name: str = "AnkiSkill Export",
) -> None:
    """Export cards to .apkg format using genanki."""
    deck_id = abs(hash(deck_name)) % (2**31)
    deck = genanki.Deck(deck_id, deck_name)

    for card in cards:
        note = genanki.Note(
            model=_MODEL,
            fields=[card.question, card.answer],
            tags=card.tags,
        )
        deck.add_note(note)

    genanki.Package(deck).write_to_file(str(output_path))
