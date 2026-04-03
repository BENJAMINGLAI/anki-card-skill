"""CLI entry point for anki-export."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from anki_skill.exporters import export_apkg, export_tsv
from anki_skill.parser import parse_cards


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="anki-export",
        description="Parse pipe-delimited flashcards and export to Anki formats.",
    )
    parser.add_argument(
        "input",
        help="Input file with pipe-delimited cards, or '-' for stdin.",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["tsv", "apkg"],
        default="tsv",
        help="Output format (default: tsv).",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (required for tsv/apkg export).",
    )
    parser.add_argument(
        "-d", "--deck-name",
        default="AnkiSkill Export",
        help="Deck name for APKG or AnkiConnect export (default: 'AnkiSkill Export').",
    )
    parser.add_argument(
        "--ankiconnect",
        action="store_true",
        help="Push cards directly to Anki via AnkiConnect (requires Anki running).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show skipped lines and additional details.",
    )

    args = parser.parse_args(argv)

    # Validate: --output is required unless --ankiconnect is used
    if not args.ankiconnect and not args.output:
        parser.error("--output is required when not using --ankiconnect")

    if args.input == "-":
        text = sys.stdin.read()
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        text = input_path.read_text(encoding="utf-8-sig")

    cards = parse_cards(text, verbose=args.verbose)

    if not cards:
        print("Error: no cards parsed from input.", file=sys.stderr)
        sys.exit(2)

    if args.ankiconnect:
        from anki_skill.exporters import export_ankiconnect

        try:
            added = export_ankiconnect(cards, deck_name=args.deck_name)
        except ConnectionError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(4)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(4)
        print(f"Pushed {added}/{len(cards)} cards to Anki deck '{args.deck_name}'", file=sys.stderr)
    else:
        output_path = Path(args.output)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error: cannot create output directory: {e}", file=sys.stderr)
            sys.exit(3)

        try:
            if args.format == "tsv":
                export_tsv(cards, output_path)
            else:
                export_apkg(cards, output_path, deck_name=args.deck_name)
        except OSError as e:
            print(f"Error: cannot write output file: {e}", file=sys.stderr)
            sys.exit(3)

        print(f"Exported {len(cards)} cards to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
