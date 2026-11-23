import os
import sqlite3

# Cesty se berou od umístění tohoto souboru, takže hra funguje odkudkoli
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "tetris.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")


def get_connection():
    con = sqlite3.connect(DB_FILE)
    con.execute("PRAGMA foreign_keys = ON")  # zapne hlídání cizích klíčů
    return con


# Spustí schema.sql: vytvoří tabulky a úspěchy (pokud ještě neexistují)
def init_db():
    con = get_connection()
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    con.close()


# Uložení hry. Vrací seznam názvů nově získaných úspěchů.
def save_game(name, score, lines, duration):
    con = get_connection()

    # hráč: když ještě neexistuje, vytvoří se
    con.execute("INSERT OR IGNORE INTO players (name) VALUES (?)", (name,))
    player_id = con.execute(
        "SELECT id FROM players WHERE name = ?", (name,)
    ).fetchone()[0]

    # samotná hra
    con.execute(
        "INSERT INTO games (player_id, score, lines_cleared, duration_seconds) VALUES (?, ?, ?, ?)",
        (player_id, score, lines, duration)
    )

    # kontrola úspěchů, které hráč ještě nemá
    games_count = con.execute(
        "SELECT COUNT(*) FROM games WHERE player_id = ?", (player_id,)
    ).fetchone()[0]
    values = {"games": games_count, "score": score, "lines": lines}

    locked = con.execute("""
        SELECT id, name, condition_type, threshold FROM achievements
        WHERE id NOT IN (
            SELECT achievement_id FROM player_achievements WHERE player_id = ?
        )
    """, (player_id,)).fetchall()

    unlocked = []
    for ach_id, ach_name, condition_type, threshold in locked:
        if values[condition_type] >= threshold:
            con.execute(
                "INSERT INTO player_achievements (player_id, achievement_id) VALUES (?, ?)",
                (player_id, ach_id)
            )
            unlocked.append(ach_name)

    con.commit()
    con.close()
    return unlocked


# Nejlepší výsledky (výchozí top 5)
def get_top_scores(limit=5):
    con = get_connection()
    rows = con.execute("""
        SELECT players.name, games.score
        FROM games
        JOIN players ON players.id = games.player_id
        ORDER BY games.score DESC
        LIMIT ?
    """, (limit,)).fetchall()
    con.close()
    return rows
