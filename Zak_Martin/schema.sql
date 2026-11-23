-- =====================================================
--  Databáze hry Tetris (SQLite)
--  Soubor se spouští automaticky při startu hry (db.py),
--  nebo ručně:  sqlite3 tetris.db < schema.sql
-- =====================================================

PRAGMA foreign_keys = ON;

-- Hráči
CREATE TABLE IF NOT EXISTS players (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Odehrané hry (každá hra patří jednomu hráči)
CREATE TABLE IF NOT EXISTS games (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id         INTEGER NOT NULL,
    score             INTEGER NOT NULL CHECK (score >= 0),
    lines_cleared     INTEGER NOT NULL DEFAULT 0 CHECK (lines_cleared >= 0),
    duration_seconds  INTEGER NOT NULL DEFAULT 0 CHECK (duration_seconds >= 0),
    played_at         TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Seznam všech úspěchů
CREATE TABLE IF NOT EXISTS achievements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL UNIQUE,
    description     TEXT    NOT NULL,
    condition_type  TEXT    NOT NULL CHECK (condition_type IN ('games', 'score', 'lines')),
    threshold       INTEGER NOT NULL CHECK (threshold > 0)
);

-- Které úspěchy který hráč získal (vazba M:N)
CREATE TABLE IF NOT EXISTS player_achievements (
    player_id       INTEGER NOT NULL,
    achievement_id  INTEGER NOT NULL,
    unlocked_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (player_id, achievement_id),
    FOREIGN KEY (player_id)      REFERENCES players(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
);

-- Indexy pro rychlé řazení a vyhledávání
CREATE INDEX IF NOT EXISTS idx_games_score  ON games(score DESC);
CREATE INDEX IF NOT EXISTS idx_games_player ON games(player_id);

-- Výchozí úspěchy
-- condition_type: games = počet odehraných her, score = skóre v jedné hře, lines = řádky v jedné hře
INSERT OR IGNORE INTO achievements (name, description, condition_type, threshold) VALUES
    ('Nováček',         'Odehraj první hru',            'games', 1),
    ('Pravidelný hráč', 'Odehraj 5 her',                'games', 5),
    ('Tisícovka',       'Získej 1000 bodů v jedné hře', 'score', 1000),
    ('Mistr',           'Získej 3000 bodů v jedné hře', 'score', 3000),
    ('Čistič',          'Smaž 10 řádků v jedné hře',    'lines', 10);
