-- Zelený kout: ukázkové dotazy.
-- Vyzkoušej si je:  sqlite3 eshop.db   a pak dotaz vlož.
-- Stejné dotazy (s otazníky místo hodnot) používají katalog.py a objednavky.py.

-- V konzoli sqlite3 se cizí klíče hlídají až po tomto příkazu (aplikace ho volá sama):
PRAGMA foreign_keys = ON;

-- 1) JOIN + WHERE + ORDER BY: nabízené produkty s dodavatelem, od nejlevnějšího
SELECT p.nazev, p.cena_kc, p.sklad, d.nazev AS dodavatel
FROM produkt p
JOIN dodavatel d ON d.id = p.dodavatel_id
WHERE p.aktivni = 1
ORDER BY p.cena_kc;

-- 2) LIKE: vyhledávání v názvu a popisu
SELECT nazev, popis
FROM produkt
WHERE nazev LIKE '%kaktus%' OR popis LIKE '%kaktus%';

-- 3) JOIN přes vazební tabulku (M:N): produkty v kategorii "Nenáročné"
SELECT p.nazev, p.cena_kc
FROM produkt p
JOIN produkt_kategorie pk ON pk.produkt_id = p.id
JOIN kategorie k          ON k.id = pk.kategorie_id
WHERE k.nazev = 'Nenáročné'
ORDER BY p.nazev;

-- 4) LEFT JOIN + GROUP BY: kolik produktů je v každé kategorii
--   (LEFT JOIN, aby se vypsala i prázdná kategorie)
SELECT k.nazev, COUNT(pk.produkt_id) AS pocet_produktu
FROM kategorie k
LEFT JOIN produkt_kategorie pk ON pk.kategorie_id = k.id
GROUP BY k.id, k.nazev
ORDER BY pocet_produktu DESC;

-- 5) Vnořený dotaz: produkty dražší, než je průměrná cena
SELECT nazev, cena_kc
FROM produkt
WHERE cena_kc > (SELECT AVG(cena_kc) FROM produkt)
ORDER BY cena_kc DESC;

-- 6) JOIN čtyř tabulek + agregace: co obsahuje objednávka č. 3 a kolik stojí
SELECT o.id AS objednavka, u.jmeno, p.nazev, po.mnozstvi, po.cena_za_kus_kc,
       po.mnozstvi * po.cena_za_kus_kc AS mezisoucet
FROM objednavka o
JOIN uzivatel u            ON u.id = o.uzivatel_id
JOIN polozka_objednavky po ON po.objednavka_id = o.id
JOIN produkt p             ON p.id = po.produkt_id
WHERE o.id = 3;

-- 7) Pohled (VIEW): přehled objednávek s celkovou cenou
SELECT id, zakaznik, stav, pocet_kusu, celkem_kc
FROM v_objednavka
ORDER BY vytvoreno DESC;

-- 8) GROUP BY + HAVING: zákazníci, kteří utratili víc než 500 Kč (bez zrušených objednávek)
SELECT zakaznik, COUNT(*) AS objednavek, SUM(celkem_kc) AS utraceno_kc
FROM v_objednavka
WHERE stav <> 'zrušená'
GROUP BY uzivatel_id, zakaznik
HAVING SUM(celkem_kc) > 500;

-- 9) Vnořený dotaz s NOT IN: zákazníci, kteří si ještě nic neobjednali
SELECT jmeno, email
FROM uzivatel
WHERE je_admin = 0
  AND id NOT IN (SELECT uzivatel_id FROM objednavka);

-- 10) Agregace: nejprodávanější produkty (kusy a tržba)
SELECT p.nazev, SUM(po.mnozstvi) AS kusu, SUM(po.mnozstvi * po.cena_za_kus_kc) AS trzba_kc
FROM polozka_objednavky po
JOIN produkt p    ON p.id = po.produkt_id
JOIN objednavka o ON o.id = po.objednavka_id
WHERE o.stav_id <> 4
GROUP BY p.id, p.nazev
ORDER BY kusu DESC
LIMIT 5;

-- 11) UPDATE: zdražení všech produktů jednoho dodavatele o 10 %
--    (staré objednávky se nezmění, mají cenu uloženou v položce)
UPDATE produkt
SET cena_kc = ROUND(cena_kc * 1.1)
WHERE dodavatel_id = 2;

-- 12) UPDATE: objednávka č. 2 je zaplacená
UPDATE objednavka
SET stav_id = 2
WHERE id = 2;

-- 13) Transakce: objednávka 1 ks produktu č. 4 zákazníkem č. 4.
--    Všechny tři příkazy se provedou společně, nebo žádný (při chybě ROLLBACK).
BEGIN;
INSERT INTO objednavka (uzivatel_id, adresa, zpusob_platby)
VALUES (4, 'Lucie Dvořáková, Polní 8, 266 01 Beroun', 'dobirka');
UPDATE produkt SET sklad = sklad - 1 WHERE id = 4 AND sklad >= 1;
INSERT INTO polozka_objednavky (objednavka_id, produkt_id, mnozstvi, cena_za_kus_kc)
VALUES (last_insert_rowid(), 4, 1, (SELECT cena_kc FROM produkt WHERE id = 4));
COMMIT;

-- 14) DELETE: produkt, který si nikdo neobjednal, smazat jde
--    (jeho zařazení do kategorií zmizí díky ON DELETE CASCADE)
DELETE FROM produkt
WHERE id = 12;

-- 15) DELETE, který databáze ODMÍTNE: produkt č. 1 je v objednávce (ON DELETE RESTRICT).
--    Odkomentuj a vyzkoušej, dostaneš "FOREIGN KEY constraint failed".
-- DELETE FROM produkt WHERE id = 1;
