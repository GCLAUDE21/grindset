from fastapi import FastAPI
from backend.database.database import init_db, save_hands, get_all_hands
from backend.parser.hand_parser import parse_file

app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "Grindset API is running"}

@app.get("/status")
def status():
    return {"status": "ok", "version": "1.0"}

@app.post("/import")
def import_hands(filepath: str):
    hands = parse_file(filepath)
    save_hands(hands)
    return {
        "message": f"{len(hands)} mains importées",
        "hands": hands
    }

@app.get("/hands")
def get_hands():
    hands = get_all_hands()
    return {
        "total": len(hands),
        "hands": hands
    }