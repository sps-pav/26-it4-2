-- ==========================================================
-- databaze.sql - databaze e-shopu Listnatec (MySQL / MariaDB)
-- Obsah: 1. DDL (tabulky)  2. VIEW a INDEX  3. DML (vzorova data)
--        4. SELECT dotazy  5. UPDATE a DELETE  6. transakce objednavky
-- Spusteni: mysql -u root -p < databaze.sql
-- ==========================================================

DROP DATABASE IF EXISTS listnatec;
CREATE DATABASE listnatec CHARACTER SET utf8mb4 COLLATE utf8mb4_czech_ci;
USE listnatec;

-- ==========================================================
-- 1. DDL - VYTVORENI TABULEK
-- ==========================================================

-- ---------- role (zakaznik, administrator, ...) ----------
CREATE TABLE role (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    nazev   VARCHAR(30) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ---------- uzivatel (zakaznici i admini) ----------
CREATE TABLE uzivatel (
    id_uzivatel        INT AUTO_INCREMENT PRIMARY KEY,
    jmeno              VARCHAR(80)  NOT NULL,
    email              VARCHAR(120) NOT NULL UNIQUE,      -- prihlasovaci jmeno
    heslo_hash         VARCHAR(255) NOT NULL,             -- NIKDY ne heslo, jen hash (PHP password_hash)
    id_role            INT NOT NULL DEFAULT 1,            -- 1 = zakaznik
    datum_registrace   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- RESTRICT: roli nejde smazat, dokud ji nekdo pouziva
    CONSTRAINT fk_uzivatel_role FOREIGN KEY (id_role) REFERENCES role(id_role)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------- kategorie kvetin ----------
CREATE TABLE kategorie (
    id_kategorie INT AUTO_INCREMENT PRIMARY KEY,
    nazev        VARCHAR(60) NOT NULL UNIQUE,
    popis        VARCHAR(255)
) ENGINE=InnoDB;

-- ---------- produkt (kvetina) ----------
CREATE TABLE produkt (
    id_produkt  INT AUTO_INCREMENT PRIMARY KEY,
    nazev       VARCHAR(100)  NOT NULL,
    popis       TEXT,
    cena        DECIMAL(10,2) NOT NULL,
    sklad       INT           NOT NULL DEFAULT 0,
    svetlo      VARCHAR(100),                             -- pozadavky na peci
    zalivka     VARCHAR(100),
    teplota     VARCHAR(50),
    obrazek     VARCHAR(255),                             -- nazev souboru s fotkou
    viditelny   BOOLEAN NOT NULL DEFAULT TRUE,            -- skryty produkt se nezobrazi v katalogu
    doporuceny  BOOLEAN NOT NULL DEFAULT FALSE,           -- zobrazi se na uvodni strane
    CONSTRAINT chk_produkt_cena  CHECK (cena >= 0),
    CONSTRAINT chk_produkt_sklad CHECK (sklad >= 0)
) ENGINE=InnoDB;

-- ---------- produkt_kategorie (vazba M:N produkt <-> kategorie) ----------
CREATE TABLE produkt_kategorie (
    id_produkt   INT NOT NULL,
    id_kategorie INT NOT NULL,
    PRIMARY KEY (id_produkt, id_kategorie),               -- slozeny klic = dvojice se nemuze opakovat
    -- CASCADE: smazany produkt/kategorie = zmizi jen vazba, ne druha strana
    CONSTRAINT fk_pk_produkt   FOREIGN KEY (id_produkt)   REFERENCES produkt(id_produkt)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_pk_kategorie FOREIGN KEY (id_kategorie) REFERENCES kategorie(id_kategorie)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------- stav objednavky (nova, zaplacena, odeslana, zrusena) ----------
CREATE TABLE stav_objednavky (
    id_stav INT AUTO_INCREMENT PRIMARY KEY,
    nazev   VARCHAR(30) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ---------- zpusob platby (jen simulace, zadne skutecne platby) ----------
CREATE TABLE zpusob_platby (
    id_platba INT AUTO_INCREMENT PRIMARY KEY,
    nazev     VARCHAR(40) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ---------- objednavka ----------
CREATE TABLE objednavka (
    id_objednavka   INT AUTO_INCREMENT PRIMARY KEY,
    id_uzivatel     INT NOT NULL,
    id_stav         INT NOT NULL DEFAULT 1,               -- 1 = nova
    id_platba       INT NOT NULL,
    datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- dodaci udaje se ukladaji primo do objednavky (uzivatel se muze pozdeji odstehovat)
    jmeno_prijemce  VARCHAR(80)  NOT NULL,
    adresa          VARCHAR(120) NOT NULL,
    mesto           VARCHAR(60)  NOT NULL,
    psc             CHAR(5)      NOT NULL,
    -- RESTRICT: uzivatele s objednavkami nejde smazat (historie objednavek musi zustat)
    CONSTRAINT fk_obj_uzivatel FOREIGN KEY (id_uzivatel) REFERENCES uzivatel(id_uzivatel)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_obj_stav     FOREIGN KEY (id_stav)     REFERENCES stav_objednavky(id_stav)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_obj_platba   FOREIGN KEY (id_platba)   REFERENCES zpusob_platby(id_platba)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------- polozka_objednavky (vazba M:N objednavka <-> produkt, s vlastnimi atributy) ----------
CREATE TABLE polozka_objednavky (
    id_objednavka INT NOT NULL,
    id_produkt    INT NOT NULL,
    mnozstvi      INT NOT NULL,
    cena_za_kus   DECIMAL(10,2) NOT NULL,                 -- cena V OKAMZIKU NAKUPU (historie cen)
    PRIMARY KEY (id_objednavka, id_produkt),
    CONSTRAINT chk_polozka_mnozstvi CHECK (mnozstvi > 0),
    CONSTRAINT chk_polozka_cena     CHECK (cena_za_kus >= 0),
    -- CASCADE: smazana objednavka = smazou se i jeji polozky
    CONSTRAINT fk_pol_objednavka FOREIGN KEY (id_objednavka) REFERENCES objednavka(id_objednavka)
        ON DELETE CASCADE ON UPDATE CASCADE,
    -- RESTRICT: produkt, ktery nekdo koupil, nejde smazat (misto toho se skryje: viditelny = 0)
    CONSTRAINT fk_pol_produkt FOREIGN KEY (id_produkt) REFERENCES produkt(id_produkt)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------- kosik_polozka (vazba M:N uzivatel <-> produkt, kosik ulozeny v DB) ----------
CREATE TABLE kosik_polozka (
    id_uzivatel INT NOT NULL,
    id_produkt  INT NOT NULL,
    mnozstvi    INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_uzivatel, id_produkt),
    CONSTRAINT chk_kosik_mnozstvi CHECK (mnozstvi > 0),
    -- CASCADE: kosik nema vyznam bez uzivatele nebo produktu
    CONSTRAINT fk_kosik_uzivatel FOREIGN KEY (id_uzivatel) REFERENCES uzivatel(id_uzivatel)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_kosik_produkt  FOREIGN KEY (id_produkt)  REFERENCES produkt(id_produkt)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------- kontaktni_zprava (formular na strance Kontakt) ----------
CREATE TABLE kontaktni_zprava (
    id_zprava   INT AUTO_INCREMENT PRIMARY KEY,
    id_uzivatel INT NULL,                                 -- NULL = zprava od neprihlaseneho
    jmeno       VARCHAR(80)  NOT NULL,
    email       VARCHAR(120) NOT NULL,
    zprava      TEXT         NOT NULL,
    datum       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- SET NULL: po smazani uzivatele zprava zustane, jen bez vazby na nej
    CONSTRAINT fk_zprava_uzivatel FOREIGN KEY (id_uzivatel) REFERENCES uzivatel(id_uzivatel)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ==========================================================
-- 2. VIEW a INDEX
-- ==========================================================

-- INDEX: web hleda produkty pres LIKE 'mon%' (hledany text zacina na zacatku nazvu),
-- index na nazev tento dotaz zrychli, protoze se nemusi prochazet cela tabulka.
-- (u LIKE '%mon%' se index nepouzije)
CREATE INDEX idx_produkt_nazev ON produkt(nazev);

-- VIEW: prehled objednavek s celkovou cenou (pouziva admin i historie objednavek)
-- LEFT JOIN, aby se zobrazila i objednavka bez polozek (celkem pak bude NULL)
CREATE VIEW v_prehled_objednavek AS
SELECT o.id_objednavka,
       o.datum_vytvoreni,
       u.id_uzivatel,
       u.jmeno AS zakaznik,
       s.nazev AS stav,
       SUM(p.mnozstvi * p.cena_za_kus) AS celkova_cena
FROM objednavka o
JOIN uzivatel u        ON u.id_uzivatel = o.id_uzivatel
JOIN stav_objednavky s ON s.id_stav = o.id_stav
LEFT JOIN polozka_objednavky p ON p.id_objednavka = o.id_objednavka
GROUP BY o.id_objednavka, o.datum_vytvoreni, u.id_uzivatel, u.jmeno, s.nazev;

-- ==========================================================
-- 3. DML - VZOROVA DATA (min. 3 zaznamy do kazde tabulky)
-- ==========================================================

INSERT INTO role (nazev) VALUES ('zakaznik'), ('administrator'), ('skladnik');

-- hesla jsou jen ukazkova - v PHP se hash vytvari funkci password_hash()
INSERT INTO uzivatel (jmeno, email, heslo_hash, id_role) VALUES
 ('Admin Listnatec', 'admin@listnatec.cz', '$2y$10$ukazkovyhashadmin000000000000000000000000000000000000', 2),
 ('Jana Nováková',   'jana@email.cz',      '$2y$10$ukazkovyhashjana0000000000000000000000000000000000000', 1),
 ('Petr Svoboda',    'petr@email.cz',      '$2y$10$ukazkovyhashpetr0000000000000000000000000000000000000', 1);

INSERT INTO kategorie (nazev, popis) VALUES
 ('Listové rostliny',   'Rostliny pěstované kvůli dekorativním listům'),
 ('Sukulenty a kaktusy','Nenáročné rostliny, které zadržují vodu'),
 ('Palmy',              'Větší rostliny do světlých místností'),
 ('Kvetoucí rostliny',  'Rostliny s okrasnými květy');

INSERT INTO produkt (nazev, popis, cena, sklad, svetlo, zalivka, teplota, obrazek, doporuceny) VALUES
 ('Monstera',    'Velké listy s dírami, oblíbená i u začátečníků.', 399.00, 15, 'Hodně světla, ne přímé slunce', 'Když je půda nahoře suchá', '18-25 °C', 'monstera.jpg', TRUE),
 ('Kaktus',      'Nenáročná rostlina, zalévá se málo.',            129.00, 40, 'Plné slunce',                  'Jednou za 2-3 týdny',       '15-30 °C', 'kaktus.jpg', TRUE),
 ('Zamioculcas', 'Přežije i velmi málo světla.',                   349.00, 10, 'I stín',                       'Zřídka',                    '16-28 °C', 'zamioculcas.jpg', TRUE),
 ('Pilea',       'Malá rostlina s kulatými lístky.',               179.00, 25, 'Světlé místo',                 'Mírně vlhká půda',          '18-24 °C', 'pilea.jpg', FALSE),
 ('Areka',       'Palma, která potřebuje hodně světla.',           459.00,  5, 'Hodně světla',                 'Pravidelně',                '18-26 °C', 'areka.jpg', FALSE),
 ('Orchidej',    'Dlouho kvete, nutná opatrná zálivka.',           299.00, 12, 'Světlo bez přímého slunce',    'Ponořením jednou týdně',    '18-25 °C', 'orchidej.jpg', FALSE);

INSERT INTO produkt_kategorie (id_produkt, id_kategorie) VALUES
 (1, 1), (2, 2), (3, 1), (3, 2), (4, 1), (5, 3), (6, 4);

INSERT INTO stav_objednavky (nazev) VALUES ('nová'), ('zaplacená'), ('odeslaná'), ('zrušená');

INSERT INTO zpusob_platby (nazev) VALUES ('dobírka'), ('převodem'), ('hotově při převzetí');

INSERT INTO objednavka (id_uzivatel, id_stav, id_platba, datum_vytvoreni, jmeno_prijemce, adresa, mesto, psc) VALUES
 (2, 3, 1, '2026-10-05 14:20:00', 'Jana Nováková', 'Ukázková 1',  'Ostrava', '70000'),
 (3, 2, 2, '2026-10-12 09:10:00', 'Petr Svoboda',  'Lipová 22',   'Studénka','74213'),
 (2, 1, 1, '2026-11-02 18:45:00', 'Jana Nováková', 'Ukázková 1',  'Ostrava', '70000');

-- cena_za_kus se ulozi v okamziku nakupu (pozdejsi zmena ceny produktu ji nezmeni)
INSERT INTO polozka_objednavky (id_objednavka, id_produkt, mnozstvi, cena_za_kus) VALUES
 (1, 1, 1, 399.00),
 (1, 2, 2, 129.00),
 (2, 3, 1, 349.00),
 (3, 6, 1, 299.00),
 (3, 4, 1, 179.00);

INSERT INTO kosik_polozka (id_uzivatel, id_produkt, mnozstvi) VALUES
 (2, 3, 1), (3, 1, 2), (3, 5, 1);

INSERT INTO kontaktni_zprava (id_uzivatel, jmeno, email, zprava) VALUES
 (2,    'Jana Nováková', 'jana@email.cz',  'Dobrý den, kdy bude skladem Areka?'),
 (NULL, 'Karel Dvořák',  'karel@email.cz', 'Posíláte i na Slovensko?'),
 (3,    'Petr Svoboda',  'petr@email.cz',  'Děkuji za rychlé doručení.');

-- ==========================================================
-- 4. SELECT DOTAZY
-- ==========================================================

-- a) katalog + kategorie (JOIN pres vazebni tabulku, WHERE, ORDER BY)
SELECT p.nazev, p.cena, k.nazev AS kategorie
FROM produkt p
JOIN produkt_kategorie pk ON pk.id_produkt = p.id_produkt
JOIN kategorie k          ON k.id_kategorie = pk.id_kategorie
WHERE p.viditelny = TRUE AND k.nazev = 'Sukulenty a kaktusy'
ORDER BY p.cena ASC;

-- b) vyhledavani (LIKE) a razeni podle ceny
SELECT nazev, cena FROM produkt WHERE nazev LIKE 'Mon%' ORDER BY cena DESC;

-- c) detail produktu (? = parametr, v PHP se pouzije prepared statement)
-- SELECT * FROM produkt WHERE id_produkt = ? AND viditelny = TRUE;

-- d) kosik uzivatele s celkovou cenou kazde polozky
SELECT p.nazev, p.cena, k.mnozstvi, p.cena * k.mnozstvi AS celkem
FROM kosik_polozka k
JOIN produkt p ON p.id_produkt = k.id_produkt
WHERE k.id_uzivatel = 3;

-- e) historie objednavek zakaznika (pres VIEW)
SELECT * FROM v_prehled_objednavek WHERE id_uzivatel = 2 ORDER BY datum_vytvoreni DESC;

-- f) trzby podle kategorie (GROUP BY, SUM) - statistika pro administraci
SELECT k.nazev AS kategorie, SUM(po.mnozstvi * po.cena_za_kus) AS trzby
FROM polozka_objednavky po
JOIN objednavka o         ON o.id_objednavka = po.id_objednavka
JOIN produkt_kategorie pk ON pk.id_produkt = po.id_produkt
JOIN kategorie k          ON k.id_kategorie = pk.id_kategorie
WHERE o.id_stav <> 4                                  -- zrusene objednavky se nepocitaji
GROUP BY k.id_kategorie, k.nazev
ORDER BY trzby DESC;

-- g) nejprodavanejsi produkty (SUM, ORDER BY, LIMIT)
SELECT p.nazev, SUM(po.mnozstvi) AS prodano_kusu
FROM polozka_objednavky po
JOIN produkt p ON p.id_produkt = po.id_produkt
GROUP BY p.id_produkt, p.nazev
ORDER BY prodano_kusu DESC
LIMIT 3;

-- h) LEFT JOIN - vsechny produkty, i ty, ktere se jeste nikdy neprodaly (COUNT = 0)
SELECT p.nazev, COUNT(po.id_objednavka) AS pocet_objednavek
FROM produkt p
LEFT JOIN polozka_objednavky po ON po.id_produkt = p.id_produkt
GROUP BY p.id_produkt, p.nazev;

-- i) HAVING - zakaznici, kteri celkem utratili vic nez 500 Kc
SELECT zakaznik, SUM(celkova_cena) AS utraceno
FROM v_prehled_objednavek
GROUP BY id_uzivatel, zakaznik
HAVING SUM(celkova_cena) > 500;

-- j) podotaz - produkty drazsi nez prumerna cena (AVG)
SELECT nazev, cena FROM produkt
WHERE cena > (SELECT AVG(cena) FROM produkt)
ORDER BY cena DESC;

-- ==========================================================
-- 5. UPDATE a DELETE
-- ==========================================================

-- zmena stavu objednavky (administrace)
UPDATE objednavka SET id_stav = 2 WHERE id_objednavka = 3;

-- zdrazeni Areky - stare objednavky se nezmeni, protoze maji vlastni cena_za_kus
UPDATE produkt SET cena = 479.00 WHERE nazev = 'Areka';

-- "smazani" produktu = skryti (smazat ho nejde, kdyz je v nejake objednavce)
UPDATE produkt SET viditelny = FALSE WHERE nazev = 'Pilea';

-- smazani kontaktni zpravy
DELETE FROM kontaktni_zprava WHERE id_zprava = 2;

-- smazani polozky z kosiku
DELETE FROM kosik_polozka WHERE id_uzivatel = 3 AND id_produkt = 5;

-- ==========================================================
-- 6. TRANSAKCE - VYTVORENI OBJEDNAVKY Z KOSIKU (uzivatel c. 2)
-- Vse se provede, nebo nic. Kdyz neco selze (napr. neni dost kusu na sklade),
-- PHP zavola ROLLBACK a v databazi nezustane pulka objednavky.
-- (je v komentari, aby se pri spusteni skriptu neprodala dalsi data)
-- ==========================================================
/*
START TRANSACTION;

-- 1) zamknout radky produktu, aby je mezitim nekdo jiny neprodal
SELECT p.id_produkt, p.sklad, k.mnozstvi
FROM kosik_polozka k JOIN produkt p ON p.id_produkt = k.id_produkt
WHERE k.id_uzivatel = 2 FOR UPDATE;

-- 2) vytvorit objednavku
INSERT INTO objednavka (id_uzivatel, id_platba, jmeno_prijemce, adresa, mesto, psc)
VALUES (2, 1, 'Jana Nováková', 'Ukázková 1', 'Ostrava', '70000');
SET @id_obj = LAST_INSERT_ID();

-- 3) zkopirovat polozky z kosiku (s AKTUALNI cenou produktu)
INSERT INTO polozka_objednavky (id_objednavka, id_produkt, mnozstvi, cena_za_kus)
SELECT @id_obj, p.id_produkt, k.mnozstvi, p.cena
FROM kosik_polozka k JOIN produkt p ON p.id_produkt = k.id_produkt
WHERE k.id_uzivatel = 2;

-- 4) odecist sklad - kdyz by sklad klesl pod 0, CHECK (sklad >= 0) vyhodi chybu
UPDATE produkt p JOIN kosik_polozka k ON k.id_produkt = p.id_produkt
SET p.sklad = p.sklad - k.mnozstvi
WHERE k.id_uzivatel = 2;

-- 5) vyprazdnit kosik
DELETE FROM kosik_polozka WHERE id_uzivatel = 2;

COMMIT;   -- pri chybe v kterymkoli kroku misto toho: ROLLBACK;
*/
