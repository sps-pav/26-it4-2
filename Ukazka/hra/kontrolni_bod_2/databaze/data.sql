-- Houbař: vzorová data (DML).  Spouští se po schema.sql.
-- Všichni vzoroví hráči mají heslo:  heslo123

INSERT INTO hrac (jmeno, heslo_hash, registrovan) VALUES
    ('pepa',   'a1b2c3d4e5f60718$95495a61bba42e73e420f853b94af897b6d7273e7c1b714a96e3122cd183fc66', '2026-10-02 14:05:00'),
    ('anicka', '0f1e2d3c4b5a6978$8aaaeec6596076eb626d7c00ebbd5dbc1de4137be266368cd1b8d1d892786851', '2026-10-05 09:30:00'),
    ('houbar', '1122334455667788$09e9a36616a58b1706ee1dbf13fb90de026aec883ca5c4cf3cbe96d243ff7342', '2026-10-11 18:45:00');

INSERT INTO obtiznost (nazev, rychlost_padu, interval_ms, pocet_zivotu, nasobic_bodu) VALUES
    ('Lehká',    2.5, 900, 5, 1),
    ('Normální', 3.5, 650, 3, 2),
    ('Těžká',    5.0, 450, 2, 3);

INSERT INTO druh_houby (nazev, body, jedla, barva, cetnost) VALUES
    ('Hřib smrkový',       10, 1, '#8b5a2b', 4),
    ('Liška obecná',        5, 1, '#e8a317', 6),
    ('Bedla vysoká',       15, 1, '#c8b08a', 2),
    ('Muchomůrka červená',  0, 0, '#d42a2a', 4),
    ('Muchomůrka zelená',   0, 0, '#7a9a4a', 2);

INSERT INTO partie (hrac_id, obtiznost_id, skore, trvani_s, odehrano) VALUES
    (1, 1,  85, 60, '2026-10-03 16:20:00'),
    (1, 2, 140, 60, '2026-10-04 17:02:00'),
    (2, 2, 190, 60, '2026-10-06 10:15:00'),
    (2, 3,  90, 22, '2026-10-07 10:40:00'),
    (3, 1,  60, 41, '2026-10-12 19:00:00');

-- Kolik kusů kterého druhu padlo do košíku v jednotlivých partiích.
-- Součet bodů odpovídá skóre partie (body druhu × počet × násobič obtížnosti).
INSERT INTO partie_houba (partie_id, druh_houby_id, pocet) VALUES
    (1, 1, 4), (1, 2, 3), (1, 3, 2), (1, 4, 1),
    (2, 1, 3), (2, 2, 5), (2, 3, 1),
    (3, 1, 5), (3, 2, 3), (3, 3, 2), (3, 4, 2),
    (4, 1, 3),            (4, 4, 1), (4, 5, 1),
    (5, 1, 2), (5, 2, 5), (5, 3, 1), (5, 4, 3), (5, 5, 2);
