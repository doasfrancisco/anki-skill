"""CLI for listing/filtering Anki cards via AnkiConnect.

Usage:
    python anki-connect/list_cards.py --deck "1. personal"
    python anki-connect/list_cards.py --deck "7. computer science" --added 30
    python anki-connect/list_cards.py --deck "7. computer science" --tag "python"
    python anki-connect/list_cards.py --due
    python anki-connect/list_cards.py --query "tag:python added:7"
"""

import argparse
import io
import sys

from anki_connect import check_connection, list_cards


# If we ever need to strip HTML for cleaner terminal output, remember to
# handle <img> tags first — extract src attributes and replace with
# [image: filename] before stripping, otherwise image-only fields appear empty.


def build_query(args) -> str:
    if args.query:
        return args.query

    parts = []
    if args.deck:
        parts.append(f'deck:"{args.deck}"')
    if args.tag:
        parts.append(f"tag:{args.tag}")
    if args.added:
        parts.append(f"added:{args.added}")
    if args.rated:
        parts.append(f"rated:{args.rated}")
    if args.due:
        parts.append("is:due")
    if args.new:
        parts.append("is:new")

    return " ".join(parts) if parts else "*"


def display_card(card: dict, index: int):
    print(f"--- Card {index} [{card['modelName']}] ---")
    for name, value in card["fields"].items():
        if value.strip():
            print(f"  {name}: {value}")
    if card["tags"]:
        print(f"  Tags: {', '.join(card['tags'])}")
    print()


def main():
    parser = argparse.ArgumentParser(description="List Anki cards via AnkiConnect")
    parser.add_argument("--deck", help="Filter by deck name")
    parser.add_argument("--tag", help="Filter by tag")
    parser.add_argument("--added", type=int, help="Cards added in last N days")
    parser.add_argument("--rated", type=int, help="Cards reviewed in last N days")
    parser.add_argument("--due", action="store_true", help="Only due cards")
    parser.add_argument("--new", action="store_true", help="Only new/unseen cards")
    parser.add_argument("--query", help="Raw Anki search query (overrides other filters)")
    parser.add_argument("--limit", type=int, default=20, help="Max cards to display (default: 20)")
    args = parser.parse_args()

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if not check_connection():
        print("Could not reach AnkiConnect. Is Anki running with the addon installed?")
        sys.exit(1)

    query = build_query(args)
    print(f"Query: {query}\n")

    cards = list_cards(query)
    total = len(cards)

    for i, card in enumerate(cards[: args.limit], 1):
        display_card(card, i)

    print(f"Showing {min(args.limit, total)} of {total} cards.")


if __name__ == "__main__":
    main()
