"""Export Card objects to Anki-importable formats."""

from __future__ import annotations

from pathlib import Path

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
