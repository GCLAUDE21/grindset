from fastapi import APIRouter
from backend.database.database import save_hands, save_hand_actions
from backend.parser.hand_parser import parse_file
import os
import json

router = APIRouter(prefix="/import", tags=["import"])

WINAMAX_HISTORY_PATH = "/Users/guillaumeclaude/Library/Application Support/winamax/documents/accounts/piiicka/history"

@router.post("/")
def import_hands(filepath: str):
    hands = parse_file(filepath)
    save_hands(hands)
    for hand in hands:
        if hand.get("streets"):
            save_hand_actions(hand["hand_id"], hand["streets"])
    return {
        "message": f"{len(hands)} mains importées",
        "hands": hands
    }

@router.post("/all")
def import_all_hands():
    total = 0
    files_processed = 0
    errors = []

    for filename in os.listdir(WINAMAX_HISTORY_PATH):
        if filename.endswith('.txt') and '_summary' not in filename:
            filepath = os.path.join(WINAMAX_HISTORY_PATH, filename)
            try:
                hands = parse_file(filepath)
                save_hands(hands)
                for hand in hands:
                    if hand.get("streets"):
                        save_hand_actions(hand["hand_id"], hand["streets"])
                total += len(hands)
                files_processed += 1
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")

    return {
        "message": f"{total} mains importées depuis {files_processed} fichiers",
        "errors": errors
    }