from fastapi import APIRouter
from backend.database.database import get_connection

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM hands")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(hero_chips_won) as total_chips FROM hands")
    total_chips = cursor.fetchone()["total_chips"] or 0

    cursor.execute("SELECT COUNT(*) as wins FROM hands WHERE hero_won = 1")
    wins = cursor.fetchone()["wins"]

    cursor.execute("""
        SELECT hero_preflop_action, COUNT(*) as count
        FROM hands
        GROUP BY hero_preflop_action
        ORDER BY count DESC
        LIMIT 1
    """)
    top_action = cursor.fetchone()

    cursor.execute("""
        SELECT hero_position, COUNT(*) as count
        FROM hands
        GROUP BY hero_position
        ORDER BY count DESC
    """)
    positions = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT hero_preflop_action, COUNT(*) as count
        FROM hands
        GROUP BY hero_preflop_action
        ORDER BY count DESC
    """)
    actions = [dict(row) for row in cursor.fetchall()]

    conn.close()

    winrate = round((wins / total * 100), 1) if total > 0 else 0

    return {
        "total_hands": total,
        "total_chips": total_chips,
        "wins": wins,
        "winrate": winrate,
        "top_action": dict(top_action) if top_action else None,
        "positions": positions,
        "actions": actions
    }