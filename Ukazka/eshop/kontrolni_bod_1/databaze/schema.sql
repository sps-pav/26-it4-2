-- Zelený kout: schéma databáze (DDL)
-- Databáze: SQLite. Spuštění ručně:  sqlite3 eshop.db < databaze/schema.sql
-- (aplikace si databázi vytvoří sama při prvním spuštění, viz db.py)
--
-- Rozdíly proti MySQL, které znáš z hodin:
--   AUTO_INCREMENT se tady píše INTEGER PRIMARY KEY AUTOINCREMENT
--   VARCHAR(n), DATETIME se tady píše TEXT
--   BOOLEAN se tady píše INTEGER s CHECK (0 / 1)
--
-- 8 tabulek, 2 vztahy M:N (produkt a kategorie, objednávka a produkt),
-- 1 pohled a 2 vlastní indexy.
PRAGMA foreign_keys = ON;

-- Uživatel = zákazník nebo administrátor obchodu.
CREATE TABLE uzivatel (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT    NOT NULL UNIQUE,                       -- slouží jako přihlašovací jméno
    jmeno       TEXT    NOT NULL,
    heslo_hash  TEXT    NOT NULL,                              -- nikdy ne heslo v čitelné podobě
    je_admin    INTEGER NOT NULL DEFAULT 0 CHECK (je_admin IN (0, 1)),
    registrovan TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Dodavatel (pěstitel).  Vztah 1:N: jeden dodavatel dodává víc produktů.
CREATE TABLE dodavatel (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev TEXT    NOT NULL UNIQUE,
    mesto TEXT    NOT NULL
);

CREATE TABLE kategorie (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev TEXT    NOT NULL UNIQUE,
    popis TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE produkt (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev        TEXT    NOT NULL UNIQUE,
    popis        TEXT    NOT NULL DEFAULT '',
    cena_kc      INTEGER NOT NULL CHECK (cena_kc >= 0),        -- celé koruny, žádná desetinná čísla
    sklad        INTEGER NOT NULL DEFAULT 0 CHECK (sklad >= 0),-- sklad nikdy nesmí jít do mínusu
    aktivni      INTEGER NOT NULL DEFAULT 1 CHECK (aktivni IN (0, 1)),  -- 0 = skrytý z nabídky
    dodavatel_id INTEGER NOT NULL,
    -- RESTRICT: dodavatele, který má produkty, smazat nejde
    FOREIGN KEY (dodavatel_id) REFERENCES dodavatel (id) ON DELETE RESTRICT
);

-- Vazební tabulka vztahu M:N mezi produktem a kategorií
-- (monstera je zároveň "Nenáročné" i "Do polostínu").
CREATE TABLE produkt_kategorie (
    produkt_id   INTEGER NOT NULL,
    kategorie_id INTEGER NOT NULL,
    PRIMARY KEY (produkt_id, kategorie_id),
    -- CASCADE: se smazaným produktem nebo kategorií zmizí i jejich zařazení
    FOREIGN KEY (produkt_id)   REFERENCES produkt (id)   ON DELETE CASCADE,
    FOREIGN KEY (kategorie_id) REFERENCES kategorie (id) ON DELETE CASCADE
);

-- Číselník stavů: 1 nová, 2 zaplacená, 3 odeslaná, 4 zrušená (plní data.sql).
CREATE TABLE stav_objednavky (
    id    INTEGER PRIMARY KEY,
    nazev TEXT    NOT NULL UNIQUE
);

-- Objednávka.  Zákazník má víc objednávek a v jednom stavu je víc objednávek (dvakrát 1:N).
CREATE TABLE objednavka (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    uzivatel_id   INTEGER NOT NULL,
    stav_id       INTEGER NOT NULL DEFAULT 1,
    adresa        TEXT    NOT NULL,
    zpusob_platby TEXT    NOT NULL CHECK (zpusob_platby IN ('dobirka', 'prevod')),
    vytvoreno     TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    -- RESTRICT: zákazníka s objednávkami smazat nejde (doklady musí zůstat)
    FOREIGN KEY (uzivatel_id) REFERENCES uzivatel (id)        ON DELETE RESTRICT,
    FOREIGN KEY (stav_id)     REFERENCES stav_objednavky (id) ON DELETE RESTRICT
);

-- Položka objednávky = vazební tabulka vztahu M:N mezi objednávkou a produktem
-- s vlastními atributy: kolik kusů a za kolik se v tu chvíli prodávalo.
CREATE TABLE polozka_objednavky (
    objednavka_id  INTEGER NOT NULL,
    produkt_id     INTEGER NOT NULL,
    mnozstvi       INTEGER NOT NULL CHECK (mnozstvi > 0),
    cena_za_kus_kc INTEGER NOT NULL CHECK (cena_za_kus_kc >= 0),   -- cena v okamžiku nákupu
    PRIMARY KEY (objednavka_id, produkt_id),
    FOREIGN KEY (objednavka_id) REFERENCES objednavka (id) ON DELETE CASCADE,
    -- RESTRICT: prodaný produkt smazat nejde, jinak by ze starých objednávek zmizelo zboží
    FOREIGN KEY (produkt_id)    REFERENCES produkt (id)    ON DELETE RESTRICT
);

-- Index pro historii objednávek zákazníka:  ... WHERE uzivatel_id = ?
CREATE INDEX idx_objednavka_uzivatel ON objednavka (uzivatel_id);

-- Index pro statistiky prodejů podle produktu. Primární klíč začíná sloupcem
-- objednavka_id, takže hledání podle produkt_id by bez indexu četlo celou tabulku.
CREATE INDEX idx_polozka_produkt ON polozka_objednavky (produkt_id);

-- Pohled: objednávka se jménem zákazníka, názvem stavu a spočítanou cenou.
-- Celková cena se nikam neukládá, vždy se dopočítá z položek.
CREATE VIEW v_objednavka AS
SELECT o.id,
       o.uzivatel_id,
       u.jmeno                                            AS zakaznik,
       u.email,
       o.stav_id,
       s.nazev                                            AS stav,
       o.adresa,
       o.zpusob_platby,
       o.vytvoreno,
       COALESCE(SUM(po.mnozstvi), 0)                      AS pocet_kusu,
       COALESCE(SUM(po.mnozstvi * po.cena_za_kus_kc), 0)  AS celkem_kc
FROM objednavka o
JOIN uzivatel u        ON u.id = o.uzivatel_id
JOIN stav_objednavky s ON s.id = o.stav_id
LEFT JOIN polozka_objednavky po ON po.objednavka_id = o.id
GROUP BY o.id;
