# Technický přehled: Houbař

Pro někoho, kdo má projekt převzít a pokračovat ve vývoji.

## Struktura kódu

| Vrstva | Soubory | Pravidlo |
|--------|---------|----------|
| Data | `db.py`, `databaze/*.sql` | SQL se píše **jen** v `db.py` |
| Pravidla hry | `hra/logika.py` | žádný import Pygame, musí jít testovat bez okna |
| Obrazovky hry | `hra/menu.py`, `prihlaseni.py`, `vyber_obtiznosti.py`, `partie.py`, `konec.py` | každá má vlastní smyčku a vrací výsledek |
| Řízení hry | `main.py` | jen přepíná obrazovky, žádná herní logika |
| Web | `web.py`, `templates/`, `static/` | funkce pro adresu jen zavolá `db.py` a vykreslí šablonu |

## Datové toky
Podrobně v [`navrh.md`](navrh.md). Ve zkratce:

1. Web zapíše hráče (`registruj_hrace`).
2. Hra hráče ověří (`prihlas_hrace`) a načte číselníky (`nacti_obtiznosti`, `nacti_druhy_hub`).
3. Hra po partii zapíše výsledek (`uloz_partii`, jedna transakce do dvou tabulek).
4. Web výsledky čte (`zebricek`, `souhrn_hracu`, `partie_hrace`, `statistika_hub`).

## Jak začít s vývojem
1. Naklonuj repozitář, vytvoř virtuální prostředí, `pip install -r requirements.txt`.
2. Spusť `python -m unittest`, musí projít všechny testy.
3. Projdi `main.py` (je krátký) a podle něj jednotlivé obrazovky.

Typické úpravy:

| Chci | Udělám |
|-------|---------|
| přidat druh houby | `INSERT` do `druh_houby` (a do `data.sql`), kód se nemění |
| přidat obtížnost | `INSERT` do `obtiznost`, tlačítko se objeví samo |
| změnit rychlost košíku, délku partie | `hra/nastaveni.py` |
| přidat stránku na web | funkce s `@app.route` ve `web.py` + šablona v `templates/` + odkaz v `base.html` |
| přidat sloupec do tabulky | `schema.sql`, `data.sql`, funkce v `db.py`; pak smazat `houbar.db` |

## Rizika a slabá místa

| Riziko | Dopad | Jak ho zmírnit |
|--------|-------|----------------|
| změna schématu bez smazání `houbar.db` | hra hlásí chybějící sloupec | po změně `schema.sql` smazat `houbar.db` |
| hra a web zapisují současně | SQLite krátce zamkne soubor | zápisy jsou krátké transakce; při větším provozu přejít na MySQL |
| rychlost hry závisí na FPS | na pomalém PC padají houby pomaleji | přepočítat pohyb na čas snímku (`dt`) |
| vývojový server Flasku | nevhodný pro internet | pro školní předvedení stačí, jinak nasadit přes WSGI server |
| chybí ochrana proti CSRF | cizí stránka by mohla odeslat formulář za přihlášeného | doplnit token do formulářů |
