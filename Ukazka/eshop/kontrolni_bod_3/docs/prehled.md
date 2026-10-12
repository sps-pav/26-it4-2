# Technický přehled: Zelený kout

Pro někoho, kdo má projekt převzít a pokračovat ve vývoji.

## Struktura kódu

| Vrstva | Soubory | Pravidlo |
|--------|---------|----------|
| Data | `databaze/*.sql`, `db.py` | strukturu DB určuje jen `schema.sql` |
| Logika | `ucty.py`, `katalog.py`, `kosik.py`, `objednavky.py` | funkce dostanou připojení a hodnoty, vrátí data nebo vyhodí `ValueError` s hláškou pro uživatele; neznají Flask |
| Web | `app.py` | přečte formulář, zavolá logiku, vykreslí šablonu nebo přesměruje; žádné SQL |
| Vzhled | `templates/`, `static/style.css` | šablony dědí z `base.html` |

Díky tomu, že logika nezná Flask, jdou `kosik.py` a `objednavky.py` testovat přímo,
bez spouštění serveru.

## Cesta jednoho požadavku (objednání)
1. Prohlížeč pošle `POST /objednat` s adresou a způsobem platby.
2. `app.objednat()` ověří přihlášení a načte košík ze session.
3. `objednavky.vytvor_objednavku()` v jedné transakci zapíše objednávku, odečte sklad a zapíše položky.
4. Úspěch: košík se vyprázdní, přesměrování na detail objednávky.
   Chyba (`ValueError`): transakce se vrátí zpět, hláška se zobrazí nad formulářem.

Diagramy: [`diagramy.md`](diagramy.md), datové toky: [`navrh.md`](navrh.md).

## Jak začít s vývojem
1. Naklonuj repozitář, vytvoř virtuální prostředí, `pip install -r requirements.txt`.
2. Spusť `python -m unittest`, musí projít všechny testy.
3. Přečti `databaze/schema.sql` (komentáře vysvětlují každé omezení), pak `objednavky.py`.

Typické úpravy:

| Chci | Udělám |
|-------|---------|
| přidat produkt nebo kategorii | v administraci, případně `INSERT` v `data.sql` |
| přidat způsob platby | `ZPUSOBY_PLATBY` v `objednavky.py` + `CHECK` u sloupce `zpusob_platby` |
| přidat stav objednávky | `INSERT` do `stav_objednavky` + barva `.stav-N` v CSS |
| přidat řazení v katalogu | slovník `RAZENI` v `katalog.py` + `<option>` v `katalog.html` |
| přidat stránku | funkce s `@app.route` v `app.py` + šablona + odkaz v `base.html` |
| změnit tabulku | `schema.sql`, `data.sql`, příslušné funkce; pak smazat `eshop.db` |

## Rizika a slabá místa

| Riziko | Dopad | Jak ho zmírnit |
|--------|-------|----------------|
| změna schématu bez smazání `eshop.db` | aplikace hlásí chybějící sloupec | po změně `schema.sql` smazat `eshop.db` |
| id stavů (1 = nová, 4 = zrušená) jsou i v kódu | přečíslování číselníku rozbije rušení objednávek | neměnit id, nové stavy jen přidávat |
| dva zákazníci objednají poslední kus současně | bez ošetření by sklad šel do mínusu | řeší podmínka `sklad >= ?` v `UPDATE` a `CHECK (sklad >= 0)` |
| košík v cookie má omezenou velikost (~4 kB) | stovky různých položek by se nevešly | pro velký obchod přesunout košík do databáze |
| chybí ochrana proti CSRF | cizí stránka by mohla odeslat formulář za přihlášeného | doplnit token do formulářů |
| administrátor se zakládá jen v databázi | nový admin = ruční `UPDATE uzivatel SET je_admin = 1` | doplnit správu uživatelů do administrace |
