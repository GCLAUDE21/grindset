from fastapi import APIRouter
from backend.database.database import get_all_hands

router = APIRouter(prefix="/hands", tags=["hands"])

@router.get("/")
def get_hands():
    hands = get_all_hands()
    return {
        "total": len(hands),
        "hands": hands
    }