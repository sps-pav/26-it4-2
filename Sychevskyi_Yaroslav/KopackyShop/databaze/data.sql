-- Ukázková data lze bezpečně doplnit do prázdné databáze.
INSERT OR IGNORE INTO role(id,nazev) VALUES (1,'zakaznik'),(2,'admin'),(3,'spravce_skladu');
INSERT OR IGNORE INTO kategorie(id,nazev) VALUES (1,'Lisovky'),(2,'Turfy'),(3,'Sálovky');
INSERT OR IGNORE INTO velikosti(id,cislo) VALUES (1,40),(2,41),(3,42),(4,43),(5,44);
INSERT OR IGNORE INTO produkty(id,nazev,znacka,popis,cena,kategorie_id,obrazek) VALUES
 (1,'Speed Pro','Nike','Lehké kopačky pro rychlou hru.',2490,1,''),
 (2,'Control X','Adidas','Pohodlné kopačky na umělý povrch.',1890,2,''),
 (3,'Indoor Star','Puma','Sálovky do tělocvičny.',1390,3,'');
INSERT OR IGNORE INTO produkt_velikost(produkt_id,velikost_id,sklad) VALUES
 (1,1,5),(1,2,4),(1,3,3),(2,2,6),(2,3,2),(2,4,3),(3,3,8),(3,4,2),(3,5,4);
-- Ukázkoví uživatelé a objednávky vznikají přes aplikaci, aby hesla byla správně zahashovaná.
-- Přidáme dalších šest kopaček do obchodu.
-- Každá má svoje číslo, název, značku, popis, cenu, kategorii a obrázek.

INSERT OR IGNORE INTO produkty
(id, nazev, znacka, popis, cena, kategorie_id, obrazek)
VALUES
(4, 'Mercurial Vapor', 'Nike', 'Rychlé kopačky na trávu.', 3299, 1, 'mercurial.jpg'),
(5, 'Phantom GX', 'Nike', 'Pohodlné kopačky pro přesnou střelu.', 2899, 1, 'phantom.jpg'),
(6, 'Predator', 'Adidas', 'Kopačky pro dobrou kontrolu míče.', 2799, 1, 'predator.jpg'),
(7, 'Copa Pure', 'Adidas', 'Pohodlné kopačky na fotbal.', 2599, 1, 'copa.jpg'),
(8, 'Future Ultimate', 'Puma', 'Moderní kopačky na trávu.', 2999, 1, 'future.jpg'),
(9, 'Ultra Ultimate', 'Puma', 'Lehké kopačky pro rychlé hráče.', 3199, 1, 'ultra.jpg');

-- Nastavíme fotky i původním třem produktům.
UPDATE produkty SET obrazek='speed.jpg' WHERE id=1;
UPDATE produkty SET obrazek='control.jpg' WHERE id=2;
UPDATE produkty SET obrazek='indoor.jpg' WHERE id=3;

-- Přidáme velikosti a počty kusů na skladě.
-- Číslo 1 až 5 označuje velikosti EU 40 až 44.

INSERT OR IGNORE INTO produkt_velikost
(produkt_id, velikost_id, sklad)
VALUES
(4,1,5), (4,2,5), (4,3,5), (4,4,5), (4,5,5),
(5,1,4), (5,2,4), (5,3,4), (5,4,4), (5,5,4),
(6,1,6), (6,2,6), (6,3,6), (6,4,6), (6,5,6),
(7,1,5), (7,2,5), (7,3,5), (7,4,5), (7,5,5),
(8,1,4), (8,2,4), (8,3,4), (8,4,4), (8,5,4),
(9,1,5), (9,2,5), (9,3,5), (9,4,5), (9,5,5);