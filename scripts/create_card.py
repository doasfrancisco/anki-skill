"""CLI entry point for creating Anki cards via AnkiConnect.

Usage:
    python anki-skill/client/create_card.py --deck "CS" --front "What is X?" --back "X is..." --tags "python,basics"
"""

import argparse
import sys

from anki_connect import check_connection, create_basic_card


def main():
    parser = argparse.ArgumentParser(description="Create an Anki card via AnkiConnect")
    parser.add_argument("--deck", required=True, help="Target deck name")
    parser.add_argument("--front", required=True, help="Front of the card")
    parser.add_argument("--back", required=True, help="Back of the card")
    parser.add_argument("--tags", default="", help="Comma-separated tags (e.g. 'python,basics')")
    args = parser.parse_args()

    if not check_connection():
        print("Could not reach AnkiConnect. Is Anki running with the addon installed?")
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    note_id = create_basic_card(deck=args.deck, front=args.front, back=args.back, tags=tags)
    print(f"Card created (note ID: {note_id})")


if __name__ == "__main__":
    main()
