import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'grindset.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hand_id TEXT UNIQUE,
            buy_in REAL,
            small_blind INTEGER,
            big_blind INTEGER,
            hero_cards TEXT,
            hero_stack INTEGER,
            hero_stack_bb REAL,
            hero_position TEXT,
            hero_preflop_action TEXT,
            hero_won INTEGER,
            hero_chips_won INTEGER,
            board TEXT,
            streets TEXT,
            showdown TEXT,
            opponents TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hand_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hand_id TEXT,
            street TEXT,
            player TEXT,
            is_hero INTEGER,
            action TEXT,
            amount INTEGER,
            FOREIGN KEY (hand_id) REFERENCES hands(hand_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de données initialisée")

def save_hands(hands):
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for hand in hands:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO hands (
                    hand_id, buy_in, small_blind, big_blind,
                    hero_cards, hero_stack, hero_stack_bb,
                    hero_position, hero_preflop_action,
                    hero_won, hero_chips_won,
                    board, streets, showdown, opponents
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hand.get("hand_id"),
                hand.get("buy_in"),
                hand.get("small_blind"),
                hand.get("big_blind"),
                json.dumps(hand.get("hero_cards", [])),
                hand.get("hero_stack"),
                hand.get("hero_stack_bb"),
                hand.get("hero_position"),
                hand.get("hero_preflop_action"),
                1 if hand.get("hero_won") else 0,
                hand.get("hero_chips_won", 0),
                json.dumps(hand.get("board", {})),
                json.dumps(hand.get("streets", {})),
                json.dumps(hand.get("showdown", {})),
                json.dumps(hand.get("opponents", []))
            ))
            saved += 1
        except Exception as e:
            print(f"Erreur sur la main {hand.get('hand_id')}: {e}")

    conn.commit()
    conn.close()
    print(f"{saved} mains sauvegardées")

def get_all_hands():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hands ORDER BY created_at DESC')
    hands = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return hands

def save_hand_actions(hand_id: str, streets: dict):
    conn = get_connection()
    cursor = conn.cursor()

    for street, actions in streets.items():
        for action in actions:
            cursor.execute('''
                INSERT INTO hand_actions 
                (hand_id, street, player, is_hero, action, amount)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                hand_id,
                street,
                action.get("player", ""),
                1 if action.get("is_hero") else 0,
                action.get("action", ""),
                action.get("amount", 0)
            ))

    conn.commit()
    conn.close()