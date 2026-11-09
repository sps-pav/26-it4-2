-- Zapneme kontrolu vazeb mezi tabulkami.
PRAGMA foreign_keys = ON;

-- Role určují, kdo smí do administrace.
CREATE TABLE IF NOT EXISTS role (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nazev TEXT NOT NULL UNIQUE
);
-- Uživatel má jednu roli; heslo bude uloženo jen jako hash.
CREATE TABLE IF NOT EXISTS uzivatele (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 jmeno TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE,
 heslo TEXT NOT NULL,
 role_id INTEGER NOT NULL,
 FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE RESTRICT
);
-- Jedna kategorie obsahuje více produktů.
CREATE TABLE IF NOT EXISTS kategorie (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nazev TEXT NOT NULL UNIQUE
);
-- Produkty nikdy nemažeme při objednávkách; raději je skryjeme.
CREATE TABLE IF NOT EXISTS produkty (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nazev TEXT NOT NULL,
 znacka TEXT NOT NULL,
 popis TEXT NOT NULL,
 cena INTEGER NOT NULL CHECK(cena >= 0),
 kategorie_id INTEGER NOT NULL,
 obrazek TEXT NOT NULL DEFAULT '',
 aktivni INTEGER NOT NULL DEFAULT 1 CHECK(aktivni IN (0,1)),
 FOREIGN KEY (kategorie_id) REFERENCES kategorie(id) ON DELETE RESTRICT
);
-- Velikosti nejsou uložené přímo u produktu, protože produkt má více velikostí.
CREATE TABLE IF NOT EXISTS velikosti (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 cislo INTEGER NOT NULL UNIQUE
);
-- První vazba M:N; vlastní údaj sklad říká, kolik kusů určité velikosti máme.
CREATE TABLE IF NOT EXISTS produkt_velikost (
 produkt_id INTEGER NOT NULL,
 velikost_id INTEGER NOT NULL,
 sklad INTEGER NOT NULL DEFAULT 0 CHECK(sklad >= 0),
 PRIMARY KEY (produkt_id, velikost_id),
 FOREIGN KEY (produkt_id) REFERENCES produkty(id) ON DELETE RESTRICT,
 FOREIGN KEY (velikost_id) REFERENCES velikosti(id) ON DELETE RESTRICT
);
-- Objednávka patří jednomu uživateli.
CREATE TABLE IF NOT EXISTS objednavky (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 uzivatel_id INTEGER NOT NULL,
 vytvoreno TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 stav TEXT NOT NULL DEFAULT 'nova' CHECK(stav IN ('nova','zaplacena','odeslana','zrusena')),
 platba TEXT NOT NULL CHECK(platba IN ('dobirka','prevod')),
 doprava TEXT NOT NULL CHECK(doprava IN ('kuryr','vydejni_misto')),
 FOREIGN KEY (uzivatel_id) REFERENCES uzivatele(id) ON DELETE RESTRICT
);
-- Druhá vazba M:N; uložíme množství a cenu platnou v době nákupu.
CREATE TABLE IF NOT EXISTS polozky_objednavky (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 objednavka_id INTEGER NOT NULL,
 produkt_id INTEGER NOT NULL,
 velikost_id INTEGER NOT NULL,
 mnozstvi INTEGER NOT NULL CHECK(mnozstvi > 0),
 cena_za_kus INTEGER NOT NULL CHECK(cena_za_kus >= 0),
 FOREIGN KEY (objednavka_id) REFERENCES objednavky(id) ON DELETE CASCADE,
 FOREIGN KEY (produkt_id) REFERENCES produkty(id) ON DELETE RESTRICT,
 FOREIGN KEY (velikost_id) REFERENCES velikosti(id) ON DELETE RESTRICT
);
-- Tento index urychluje hledání produktů podle značky.
CREATE INDEX IF NOT EXISTS idx_produkty_znacka ON produkty(znacka);
-- Pohled počítá součet starých objednávek z uložených cen.
CREATE VIEW IF NOT EXISTS prehled_objednavek AS
SELECT o.id, o.uzivatel_id, o.vytvoreno, o.stav,
 COALESCE(SUM(p.mnozstvi * p.cena_za_kus),0) AS celkem
FROM objednavky o LEFT JOIN polozky_objednavky p ON p.objednavka_id=o.id
GROUP BY o.id;
