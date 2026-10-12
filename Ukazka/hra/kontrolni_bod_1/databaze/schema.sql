-- Houbař: schéma databáze (DDL)
-- Databáze: SQLite. Spuštění ručně:  sqlite3 houbar.db < databaze/schema.sql
-- (hra i web si databázi vytvoří samy při prvním spuštění, viz db.py)
--
-- Rozdíly proti MySQL, které znáš z hodin:
--   AUTO_INCREMENT se tady píše INTEGER PRIMARY KEY AUTOINCREMENT
--   VARCHAR(n), DATETIME se tady píše TEXT
--   BOOLEAN se tady píše INTEGER s CHECK (0 / 1)
PRAGMA foreign_keys = ON;

-- Hráč = uživatelský účet. Vzniká registrací na webu, přihlašuje se ve hře i na webu.
CREATE TABLE hrac (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno       TEXT    NOT NULL UNIQUE,
    heslo_hash  TEXT    NOT NULL,                              -- nikdy ne heslo v čitelné podobě
    registrovan TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Číselník obtížností. Hra si z něj čte rychlost, počet životů a násobič bodů.
CREATE TABLE obtiznost (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev         TEXT    NOT NULL UNIQUE,
    rychlost_padu REAL    NOT NULL CHECK (rychlost_padu > 0),  -- pixely za snímek
    interval_ms   INTEGER NOT NULL CHECK (interval_ms > 0),    -- jak často padá nová houba
    pocet_zivotu  INTEGER NOT NULL DEFAULT 3 CHECK (pocet_zivotu > 0),
    nasobic_bodu  INTEGER NOT NULL DEFAULT 1 CHECK (nasobic_bodu > 0)
);

-- Číselník druhů hub. Jedlá houba dává body, jedovatá bere život.
CREATE TABLE druh_houby (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev   TEXT    NOT NULL UNIQUE,
    body    INTEGER NOT NULL DEFAULT 0 CHECK (body >= 0),
    jedla   INTEGER NOT NULL DEFAULT 1 CHECK (jedla IN (0, 1)),
    barva   TEXT    NOT NULL DEFAULT '#8b5a2b',                -- barva klobouku (#rrggbb)
    cetnost INTEGER NOT NULL DEFAULT 1 CHECK (cetnost > 0)     -- vyšší číslo = padá častěji
);

-- Jedna odehraná partie.  Hráč má víc partií a na jednu obtížnost se hraje víc partií (dvakrát 1:N).
CREATE TABLE partie (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    hrac_id      INTEGER NOT NULL,
    obtiznost_id INTEGER NOT NULL,
    skore        INTEGER NOT NULL DEFAULT 0 CHECK (skore >= 0),
    trvani_s     INTEGER NOT NULL DEFAULT 0 CHECK (trvani_s >= 0),
    odehrano     TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    -- smazání hráče smaže i jeho partie
    FOREIGN KEY (hrac_id)      REFERENCES hrac (id)      ON DELETE CASCADE,
    -- obtížnost, na které už někdo hrál, smazat nejde
    FOREIGN KEY (obtiznost_id) REFERENCES obtiznost (id) ON DELETE RESTRICT
);

-- Vazební tabulka vztahu M:N mezi partií a druhem houby:
-- v jedné partii hráč sebere více druhů hub a jeden druh se vyskytne v mnoha partiích.
CREATE TABLE partie_houba (
    partie_id     INTEGER NOT NULL,
    druh_houby_id INTEGER NOT NULL,
    pocet         INTEGER NOT NULL CHECK (pocet > 0),          -- kolik kusů v té partii
    PRIMARY KEY (partie_id, druh_houby_id),
    FOREIGN KEY (partie_id)     REFERENCES partie (id)     ON DELETE CASCADE,
    FOREIGN KEY (druh_houby_id) REFERENCES druh_houby (id) ON DELETE RESTRICT
);
