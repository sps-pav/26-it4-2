# Databáze e-shopu Listnatec

Soubory: `databaze.sql` (celá databáze + vzorová data + dotazy), `er-diagram.svg` (ER diagram).
Systém: MySQL / MariaDB (InnoDB, utf8mb4). Spuštění: `mysql -u root -p < databaze.sql`.

## Tabulky (11)

| Tabulka | Účel | Primární klíč |
|---|---|---|
| `role` | role uživatele (zákazník, administrátor, skladník) | `id_role` |
| `uzivatel` | zákazníci a administrátoři, heslo jen jako hash | `id_uzivatel` |
| `kategorie` | kategorie květin | `id_kategorie` |
| `produkt` | květiny (cena, sklad, péče) | `id_produkt` |
| `produkt_kategorie` | M:N produkt ↔ kategorie | `(id_produkt, id_kategorie)` |
| `stav_objednavky` | nová / zaplacená / odeslaná / zrušená | `id_stav` |
| `zpusob_platby` | simulovaná platba | `id_platba` |
| `objednavka` | hlavička objednávky a dodací údaje | `id_objednavka` |
| `polozka_objednavky` | M:N objednávka ↔ produkt (množství, cena za kus) | `(id_objednavka, id_produkt)` |
| `kosik_polozka` | M:N uživatel ↔ produkt (košík) | `(id_uzivatel, id_produkt)` |
| `kontaktni_zprava` | zprávy z kontaktního formuláře | `id_zprava` |

## Vztahy

- **1:N:** role→uživatel, uživatel→objednávka, stav→objednávka, platba→objednávka, uživatel→kontaktní zpráva
- **M:N (3×):** produkt↔kategorie, objednávka↔produkt (vlastní atributy `mnozstvi`, `cena_za_kus`), uživatel↔produkt (košík, atribut `mnozstvi`)

## Cizí klíče a chování při mazání

| Cizí klíč | ON DELETE | Proč |
|---|---|---|
| `uzivatel.id_role` | RESTRICT | roli, kterou někdo má, nejde smazat |
| `objednavka.id_uzivatel` | RESTRICT | uživatel s objednávkami se nesmí smazat, historie musí zůstat |
| `objednavka.id_stav`, `id_platba` | RESTRICT | číselníky se používají v objednávkách |
| `polozka_objednavky.id_objednavka` | CASCADE | položky nemají smysl bez objednávky |
| `polozka_objednavky.id_produkt` | RESTRICT | prodaný produkt nejde smazat, jen skrýt (`viditelny = 0`) |
| `produkt_kategorie.*` | CASCADE | maže se jen vazba, ne produkt ani kategorie |
| `kosik_polozka.*` | CASCADE | košík nemá smysl bez uživatele nebo produktu |
| `kontaktni_zprava.id_uzivatel` | SET NULL | zpráva zůstane, jen ztratí vazbu na smazaného uživatele |

## Integritní omezení

`CHECK`: `produkt.cena >= 0`, `produkt.sklad >= 0`, `polozka_objednavky.mnozstvi > 0`, `polozka_objednavky.cena_za_kus >= 0`, `kosik_polozka.mnozstvi > 0`.
`UNIQUE`: `uzivatel.email`, `kategorie.nazev`, `role.nazev`, `stav_objednavky.nazev`, `zpusob_platby.nazev`.

## Splnění dalších požadavků

- **Transakce:** vytvoření objednávky (objednávka + položky + odečtení skladu + vyprázdnění košíku) je v `databaze.sql`, část 6. Při chybě (např. `sklad` by klesl pod 0 a porušil `CHECK`) se provede `ROLLBACK`.
- **Historie cen:** `polozka_objednavky.cena_za_kus` se uloží v okamžiku nákupu. Změna `produkt.cena` staré objednávky nezmění. Celková cena se neukládá, počítá se (`SUM`) ve view.
- **VIEW:** `v_prehled_objednavek` (objednávky s celkovou cenou).
- **Index:** `idx_produkt_nazev` na `produkt(nazev)` zrychluje vyhledávání `LIKE 'text%'` v katalogu.
- **Pokročilé dotazy:** LEFT JOIN, HAVING, podotaz, SUM, COUNT, AVG viz `databaze.sql`, část 4.
- **Bezpečnost:** v PHP jen parametrizované dotazy (prepared statements), hesla přes `password_hash()`.

## Normalizace (BCNF)

U každé tabulky je každá netriviální funkční závislost typu *klíč → atribut*, takže je v BCNF.

| Tabulka | Klíč | Proč BCNF |
|---|---|---|
| `role` | `id_role` (kandidát `nazev`) | jediný další atribut je klíč |
| `uzivatel` | `id_uzivatel` (kandidát `email`) | jméno, hash, role a datum závisí jen na uživateli |
| `kategorie` | `id_kategorie` (kandidát `nazev`) | popis závisí na kategorii |
| `produkt` | `id_produkt` | cena, sklad, popis i péče popisují jen konkrétní produkt |
| `produkt_kategorie` | `(id_produkt, id_kategorie)` | žádné neklíčové atributy |
| `stav_objednavky`, `zpusob_platby` | `id_stav`, `id_platba` | číselníky s jedním atributem |
| `objednavka` | `id_objednavka` | datum, stav, platba i dodací údaje popisují právě tuto objednávku (adresa je záměrně kopie z doby objednávky, nezávisí na uživateli) |
| `polozka_objednavky` | `(id_objednavka, id_produkt)` | množství a cena platí pro dvojici objednávka + produkt |
| `kosik_polozka` | `(id_uzivatel, id_produkt)` | množství platí pro dvojici uživatel + produkt |
| `kontaktni_zprava` | `id_zprava` | všechny atributy popisují jednu zprávu |
