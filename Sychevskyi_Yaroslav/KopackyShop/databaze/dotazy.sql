-- Hledání kopaček podle názvu (LIKE), JOIN a řazení.
SELECT p.nazev, k.nazev AS kategorie, p.cena
FROM produkty p JOIN kategorie k ON k.id=p.kategorie_id
WHERE p.nazev LIKE '%Pro%' ORDER BY p.cena ASC;

-- LEFT JOIN: ukáže i produkty, které ještě nikdo nekoupil.
SELECT p.nazev, COALESCE(SUM(po.mnozstvi),0) AS prodano
FROM produkty p LEFT JOIN polozky_objednavky po ON po.produkt_id=p.id
GROUP BY p.id ORDER BY prodano DESC;

-- HAVING, COUNT, SUM a AVG: statistika objednávek uživatelů.
SELECT u.email, COUNT(o.id) AS pocet, SUM(v.celkem) AS trzba, AVG(v.celkem) AS prumer
FROM uzivatele u JOIN objednavky o ON o.uzivatel_id=u.id
JOIN prehled_objednavek v ON v.id=o.id
WHERE o.stav != 'zrusena'
GROUP BY u.id HAVING COUNT(o.id) >= 1;

-- Poddotaz: produkty dražší než průměrná cena.
SELECT nazev, cena FROM produkty WHERE cena > (SELECT AVG(cena) FROM produkty);

-- UPDATE a DELETE jsou ukázky: spouštěj je jen při vědomé úpravě dat.
-- UPDATE produkty SET cena=1990 WHERE id=1;
-- DELETE FROM produkt_velikost WHERE produkt_id=1 AND velikost_id=1;
