-- Ukazkova data e-shopu. INSERT OR IGNORE zabrani duplicitam pri dalsim spusteni.
INSERT OR IGNORE INTO role(id,nazev) VALUES (1,'zakaznik'),(2,'admin'),(3,'spravce_skladu');
INSERT OR IGNORE INTO kategorie(id,nazev) VALUES (1,'Lisovky'),(2,'Turfy'),(3,'Salovky');
INSERT OR IGNORE INTO velikosti(id,cislo) VALUES (1,40),(2,41),(3,42),(4,43),(5,44),(6,45);
INSERT OR IGNORE INTO produkty(id,nazev,znacka,popis,cena,kategorie_id,obrazek) VALUES
(1,'Mercurial Speed','Nike','Lehke a rychle kopacky na prirodni travu.',3290,1,'kopacky-1.svg'),
(2,'Predator Control','Adidas','Kopacky pro presnou prihravku a kontrolu mice.',2990,1,'kopacky-2.svg'),
(3,'Ultra Match','Puma','Lehky model pro rychle zmeny smeru.',2690,1,'kopacky-3.svg'),
(4,'Phantom Strike','Nike','Pohodlny strih a cit pro mic.',3190,1,'kopacky-4.svg'),
(5,'Copa Pure','Adidas','Mekky svrs ek a pohodli pri hre.',2490,1,'kopacky-5.svg'),
(6,'Future Ultimate','Puma','Flexibilni konstrukce pro kreativni hrace.',3390,1,'kopacky-6.svg'),
(7,'Tiempo Legend','Nike','Klasicky pohodlny model na travu.',2790,1,'kopacky-7.svg'),
(8,'X Crazyfast','Adidas','Lehke kopacky pro maximalni tempo.',3090,1,'kopacky-8.svg'),
(9,'King Pro','Puma','Univerzalni model s dobrym kontaktem s micem.',2290,1,'kopacky-9.svg'),
(10,'Street Turf','Nike','Turfy s mnoha malymi spunty na umele povrchy.',2190,2,'kopacky-10.svg'),
(11,'Predator League TF','Adidas','Odolne turfy na umele travniky.',2390,2,'kopacky-11.svg'),
(12,'Future Play IT','Puma','Salovky na halovy fotbal.',1890,3,'kopacky-12.svg');
INSERT OR IGNORE INTO produkt_velikost(produkt_id,velikost_id,sklad)
SELECT p.id,v.id,5 FROM produkty p CROSS JOIN velikosti v WHERE p.id BETWEEN 1 AND 12;
