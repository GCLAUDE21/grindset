from fastapi import APIRouter
from backend.agents.gto_agent import analyze_hand_gto
from backend.database.database import get_connection
import json

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/hand/{hand_id}")
def analyze_hand(hand_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hands WHERE hand_id = ?", (hand_id,))
    hand = cursor.fetchone()
    conn.close()

    if not hand:
        return {"error": "Main non trouvée"}

    hand = dict(hand)
    result = analyze_hand_gto(hand)
    return {
        "hand_id": hand_id,
        "score": result["score"],
        "is_correct": result["is_correct"],
        "analysis": result["analysis"]
    }