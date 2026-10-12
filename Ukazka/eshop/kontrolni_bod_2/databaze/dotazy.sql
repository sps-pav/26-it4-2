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
