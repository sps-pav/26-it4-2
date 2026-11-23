-- Ukázkové dotazy nad databází hry Tetris

-- 1) TOP 5 nejlepších her (to samé používá hlavní menu)
SELECT players.name, games.score
FROM games
JOIN players ON players.id = games.player_id
ORDER BY games.score DESC
LIMIT 5;

-- 2) Statistiky každého hráče: počet her, nejlepší a průměrné skóre
SELECT players.name,
       COUNT(games.id)            AS pocet_her,
       MAX(games.score)           AS nejlepsi_skore,
       ROUND(AVG(games.score), 1) AS prumerne_skore
FROM players
JOIN games ON games.player_id = players.id
GROUP BY players.id
ORDER BY nejlepsi_skore DESC;

-- 3) Získané úspěchy všech hráčů
SELECT players.name, achievements.name AS uspech, player_achievements.unlocked_at
FROM player_achievements
JOIN players      ON players.id      = player_achievements.player_id
JOIN achievements ON achievements.id = player_achievements.achievement_id
ORDER BY players.name, player_achievements.unlocked_at;

-- 4) Celkový počet smazaných řádků a odehraného času
SELECT SUM(lines_cleared) AS radku_celkem, SUM(duration_seconds) AS sekund_celkem
FROM games;
