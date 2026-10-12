-- Zelený kout: vzorová data (DML).  Spouští se po schema.sql.
-- Administrátor:  admin@zelenykout.example  /  admin123
-- Zákazníci:      jana@example.com, petr@example.com, lucie@example.com  /  heslo123

-- Číselník stavů. Aplikace počítá s těmito id (1 = nová, 4 = zrušená).
INSERT INTO stav_objednavky (id, nazev) VALUES
    (1, 'nová'),
    (2, 'zaplacená'),
    (3, 'odeslaná'),
    (4, 'zrušená');

INSERT INTO uzivatel (email, jmeno, heslo_hash, je_admin, registrovan) VALUES
    ('admin@zelenykout.example', 'Správce obchodu', '99aabbccddeeff00$7a10721ceef225fe0761bcd7013048a4f62aca594830fbb517799427a9142b4f', 1, '2026-10-01 08:00:00'),
    ('jana@example.com',         'Jana Nováková',   'a1b2c3d4e5f60718$95495a61bba42e73e420f853b94af897b6d7273e7c1b714a96e3122cd183fc66', 0, '2026-10-12 17:20:00'),
    ('petr@example.com',         'Petr Svoboda',    '0f1e2d3c4b5a6978$8aaaeec6596076eb626d7c00ebbd5dbc1de4137be266368cd1b8d1d892786851', 0, '2026-10-20 09:05:00'),
    ('lucie@example.com',        'Lucie Dvořáková', '1122334455667788$09e9a36616a58b1706ee1dbf13fb90de026aec883ca5c4cf3cbe96d243ff7342', 0, '2026-11-03 20:41:00');

INSERT INTO dodavatel (nazev, mesto) VALUES
    ('Zahradnictví Lípa',    'Kladno'),
    ('Sukulenty Morava',     'Olomouc'),
    ('Keramika Hlína',       'Beroun');

INSERT INTO kategorie (nazev, popis) VALUES
    ('Nenáročné',          'Rostliny, které odpustí zapomenutou zálivku.'),
    ('Do polostínu',       'Vhodné dál od okna nebo na severní stranu.'),
    ('Kvetoucí',           'Rostliny pěstované hlavně pro květy.'),
    ('Sukulenty a kaktusy','Potřebují hodně světla a málo vody.'),
    ('Doplňky',            'Květináče, substráty a hnojiva.');

INSERT INTO produkt (nazev, popis, cena_kc, sklad, aktivni, dodavatel_id) VALUES
    ('Monstera deliciosa',   'Oblíbená rostlina s děrovanými listy. Výška cca 40 cm.',        349, 12, 1, 1),
    ('Zamiokulkas',          'Téměř nezničitelná rostlina s lesklými listy.',                 289,  8, 1, 1),
    ('Tchynin jazyk',        'Sansevieria, snese sucho i tmavší kout.',                      199, 20, 1, 1),
    ('Lopatkovec',           'Spathiphyllum s bílými květy, čistí vzduch.',                   229,  6, 1, 1),
    ('Orchidej Phalaenopsis','Kvete několik měsíců, růžové květy.',                           319,  4, 1, 1),
    ('Africká fialka',       'Drobná kvetoucí rostlina na parapet.',                           89, 15, 1, 1),
    ('Echeveria',            'Sukulent ve tvaru růžice, průměr 8 cm.',                         79, 30, 1, 2),
    ('Kaktus Mammillaria',   'Kulovitý kaktus, na jaře kvete věncem květů.',                   99,  0, 1, 2),
    ('Aloe vera',            'Léčivý sukulent, výška cca 25 cm.',                             149, 10, 1, 2),
    ('Keramický květináč 14 cm', 'Glazovaný květináč s podmiskou, bílý.',                     179, 25, 1, 3),
    ('Substrát pro sukulenty 5 l', 'Propustný substrát s pískem a perlitem.',                  69, 40, 1, 3),
    ('Fíkus lyrata',         'Vyšší rostlina s velkými listy. Dočasně nedodáváme.',           599,  0, 0, 1);

INSERT INTO produkt_kategorie (produkt_id, kategorie_id) VALUES
    (1, 1), (1, 2),
    (2, 1), (2, 2),
    (3, 1), (3, 2),
    (4, 2), (4, 3),
    (5, 3),
    (6, 3),
    (7, 4), (7, 1),
    (8, 4),
    (9, 4), (9, 1),
    (10, 5),
    (11, 5),
    (12, 2);

INSERT INTO objednavka (uzivatel_id, stav_id, adresa, zpusob_platby, vytvoreno) VALUES
    (2, 3, 'Jana Nováková, Školní 12, 272 01 Kladno',  'prevod',  '2026-10-14 10:12:00'),
    (2, 1, 'Jana Nováková, Školní 12, 272 01 Kladno',  'dobirka', '2026-11-05 19:30:00'),
    (3, 2, 'Petr Svoboda, Dlouhá 5, 110 00 Praha 1',   'prevod',  '2026-10-22 14:45:00'),
    (3, 4, 'Petr Svoboda, Dlouhá 5, 110 00 Praha 1',   'dobirka', '2026-11-01 08:15:00');

-- Položky: cena za kus je cena platná v den nákupu. Monstera tehdy stála 329 Kč,
-- dnes stojí 349 Kč, ale stará objednávka se zdražením nezměnila.
INSERT INTO polozka_objednavky (objednavka_id, produkt_id, mnozstvi, cena_za_kus_kc) VALUES
    (1, 1, 1, 329), (1, 10, 1, 179),
    (2, 7, 3,  79), (2, 11, 1,  69), (2, 9, 1, 149),
    (3, 2, 1, 289), (3, 3, 2, 199), (3, 10, 2, 179),
    (4, 5, 1, 319);
