-- Houbař: ukázkové dotazy.
-- Vyzkoušej si je:  sqlite3 houbar.db   a pak dotaz vlož.
-- Stejné dotazy (jen s otazníky místo hodnot) používá db.py.

-- V konzoli sqlite3 se cizí klíče hlídají až po tomto příkazu (aplikace ho volá sama):
PRAGMA foreign_keys = ON;

-- 1) JOIN + ORDER BY: žebříček, tedy nejlepší partie se jménem hráče a obtížností
SELECT h.jmeno, p.skore, o.nazev AS obtiznost, p.odehrano
FROM partie p
JOIN hrac h      ON h.id = p.hrac_id
JOIN obtiznost o ON o.id = p.obtiznost_id
ORDER BY p.skore DESC
LIMIT 10;

-- 2) WHERE: partie odehrané na obtížnost Normální se skóre aspoň 100
SELECT p.id, p.skore, p.trvani_s
FROM partie p
JOIN obtiznost o ON o.id = p.obtiznost_id
WHERE o.nazev = 'Normální' AND p.skore >= 100;

-- 3) LIKE: hráči, jejichž jméno obsahuje "ou"
SELECT id, jmeno, registrovan
FROM hrac
WHERE jmeno LIKE '%ou%';

-- 4) GROUP BY: počet partií, nejlepší a průměrné skóre každého hráče
--   (LEFT JOIN, aby se vypsal i hráč, který ještě nehrál)
SELECT h.jmeno,
       COUNT(p.id)           AS pocet_partii,
       MAX(p.skore)          AS nejlepsi_skore,
       ROUND(AVG(p.skore))   AS prumerne_skore
FROM hrac h
LEFT JOIN partie p ON p.hrac_id = h.id
GROUP BY h.id, h.jmeno
ORDER BY nejlepsi_skore DESC;

-- 5) JOIN přes vazební tabulku (M:N): co všechno sebral hráč "pepa"
SELECT d.nazev, SUM(ph.pocet) AS celkem
FROM partie_houba ph
JOIN partie p     ON p.id = ph.partie_id
JOIN hrac h       ON h.id = p.hrac_id
JOIN druh_houby d ON d.id = ph.druh_houby_id
WHERE h.jmeno = 'pepa'
GROUP BY d.id, d.nazev
ORDER BY celkem DESC;

-- 6) GROUP BY + HAVING: druhy hub, kterých se celkem sebralo víc než 10 kusů
SELECT d.nazev, SUM(ph.pocet) AS celkem
FROM partie_houba ph
JOIN druh_houby d ON d.id = ph.druh_houby_id
GROUP BY d.id, d.nazev
HAVING SUM(ph.pocet) > 10;

-- 7) UPDATE: muchomůrky budou padat častěji
UPDATE druh_houby
SET cetnost = cetnost + 1
WHERE jedla = 0;

-- 8) UPDATE: změna hesla hráče (hash vygeneruje aplikace, tady je jen ukázka tvaru)
UPDATE hrac
SET heslo_hash = 'nova_sul$novy_otisk'
WHERE jmeno = 'houbar';

-- 9) DELETE: smazání jedné partie, řádky v partie_houba zmizí díky ON DELETE CASCADE
DELETE FROM partie
WHERE id = 5;

-- 10) DELETE: smazání hráče včetně všech jeho partií (opět CASCADE)
DELETE FROM hrac
WHERE jmeno = 'houbar';
