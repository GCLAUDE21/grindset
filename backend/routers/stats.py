from fastapi import APIRouter
from backend.database.database import get_connection

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # Total mains
    cursor.execute("SELECT COUNT(*) as total FROM hands")
    total = cursor.fetchone()["total"]

    # Chips gagnés
    cursor.execute("SELECT SUM(hero_chips_won) as total_chips FROM hands")
    total_chips = cursor.fetchone()["total_chips"] or 0

    # Victoires
    cursor.execute("SELECT COUNT(*) as wins FROM hands WHERE hero_won = 1")
    wins = cursor.fetchone()["wins"]

    # Action principale
    cursor.execute("""
        SELECT hero_preflop_action, COUNT(*) as count
        FROM hands GROUP BY hero_preflop_action
        ORDER BY count DESC LIMIT 1
    """)
    top_action = cursor.fetchone()

    # Positions
    cursor.execute("""
        SELECT hero_position, COUNT(*) as count
        FROM hands GROUP BY hero_position
        ORDER BY count DESC
    """)
    positions = [dict(row) for row in cursor.fetchall()]

    # Actions
    cursor.execute("""
        SELECT hero_preflop_action, COUNT(*) as count
        FROM hands GROUP BY hero_preflop_action
        ORDER BY count DESC
    """)
    actions = [dict(row) for row in cursor.fetchall()]

    # Nombre de sessions (fichiers distincts = hand_id prefix)
    cursor.execute("""
        SELECT COUNT(DISTINCT substr(hand_id, 1, instr(hand_id, '-') - 1)) as sessions
        FROM hands
    """)
    sessions = cursor.fetchone()["sessions"]

    # Dernière session
    cursor.execute("""
        SELECT hand_id, buy_in, hero_won, hero_chips_won, created_at
        FROM hands
        ORDER BY created_at DESC
        LIMIT 50
    """)
    last_hands = [dict(row) for row in cursor.fetchall()]

    # Stats dernière session
    last_session_prefix = last_hands[0]["hand_id"].rsplit("-", 2)[0] if last_hands else None
    last_session_hands = [h for h in last_hands if h["hand_id"].startswith(last_session_prefix)] if last_session_prefix else []
    last_session_wins = sum(1 for h in last_session_hands if h["hero_won"])
    last_session_chips = sum(h["hero_chips_won"] for h in last_session_hands)

    conn.close()

    winrate = round((wins / total * 100), 1) if total > 0 else 0

    return {
        "total_hands": total,
        "total_chips": total_chips,
        "wins": wins,
        "winrate": winrate,
        "sessions": sessions,
        "top_action": dict(top_action) if top_action else None,
        "positions": positions,
        "actions": actions,
        "last_session": {
            "hands": len(last_session_hands),
            "wins": last_session_wins,
            "chips": last_session_chips,
            "date": last_session_hands[0]["created_at"] if last_session_hands else None
        }
    }