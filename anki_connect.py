"""AnkiConnect client — talks to Anki desktop via the AnkiConnect addon (localhost:8765).

Requires: Anki desktop running + AnkiConnect addon installed (code: 2055492159).
No external dependencies — uses only urllib.request from stdlib.
"""

import json
import urllib.request

ANKI_CONNECT_URL = "http://localhost:8765"


def anki_request(action: str, **params) -> dict:
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    if body.get("error"):
        raise RuntimeError(f"AnkiConnect error: {body['error']}")
    return body["result"]


def create_basic_card(deck: str, front: str, back: str, tags: list[str] | None = None) -> int:
    note = {
        "deckName": deck,
        "modelName": "Basic",
        "fields": {"Front": front, "Back": back},
        "options": {"allowDuplicate": False},
        "tags": tags or [],
    }
    return anki_request("addNote", note=note)


def list_cards(query: str) -> list[dict]:
    note_ids = anki_request("findNotes", query=query)
    if not note_ids:
        return []
    notes = anki_request("notesInfo", notes=note_ids)
    return [
        {
            "noteId": n["noteId"],
            "modelName": n["modelName"],
            "tags": n["tags"],
            "fields": {name: val["value"] for name, val in n["fields"].items()},
        }
        for n in notes
    ]


def list_models() -> list[str]:
    return anki_request("modelNames")


def list_decks() -> list[str]:
    return anki_request("deckNames")


def check_connection() -> bool:
    try:
        anki_request("version")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if check_connection():
        print("Connected to AnkiConnect.")
        print("Decks:", list_decks())
    else:
        print("Could not reach AnkiConnect. Is Anki running with the addon installed?")
