# Anki Skill

A Claude Code skill that creates and browses Anki flashcards during coding sessions. When you're learning something new — a concept, gotcha, or mental model — Claude proposes a card, you approve it, and it's in your deck.

## Demo

https://www.loom.com/share/0248912742334161936f4aabba55105b

## Why

I have 500+ Anki cards and 226 leeches. Bad cards are the problem. This skill enforces quality rules so every card Claude creates is atomic, minimal, and worth remembering long-term.

## How it works

1. You're coding with Claude Code and learn something new
2. Claude notices and proposes a flashcard (or you invoke `/anki`)
3. You review the front, back, deck, and tags
4. On approval, the card is created in Anki via AnkiConnect

No external dependencies — just Python's stdlib (`urllib.request`).

## Prerequisites

- **Anki desktop** running on your machine
- **AnkiConnect addon** installed — open Anki, go to Tools > Add-ons > Get Add-ons, paste code `2055492159`, restart Anki. This exposes a local API on port 8765 that the skill talks to.

## Setup

1. Copy this folder to `~/.claude/skills/anki/`
2. (Optional) Add a SessionStart hook to remind Claude about card creation:

```json
{
  "type": "command",
  "command": "echo \"Reminder: You can create Anki flashcards with /anki. If you notice the user learning something new, proactively suggest a card.\""
}
```

## Usage

### Create a card

```bash
python ./scripts/create_card.py \
  --deck "7. computer science" \
  --front "What does __slots__ do in Python?" \
  --back "Restricts instance attributes to a fixed set, saving memory by skipping __dict__." \
  --tags "python,memory"
```

### List cards

```bash
python ./scripts/list_cards.py --query "tag:python added:7"
python ./scripts/list_cards.py --deck "7. computer science" --added 30
```

### List decks

```bash
python -c "import sys; sys.path.insert(0, './scripts'); from anki_connect import list_decks; print(list_decks())"
```

## Card quality rules

1. **Atomic** — one fact per card
2. **Short, specific front** — few words, one unambiguous answer
3. **Minimal back** — no unnecessary text
4. **Visual over prose** — file trees and code blocks over sentences
5. **No trivia** — only things worth remembering long-term
6. **Tag consistently** — lowercase, comma-separated

## Project structure

```
anki-skill/
├── SKILL.md          # Claude Code skill definition
├── README.md
└── scripts/
    ├── anki_connect.py   # AnkiConnect client (stdlib only)
    ├── create_card.py    # CLI: create a card
    └── list_cards.py     # CLI: list/filter cards
```
