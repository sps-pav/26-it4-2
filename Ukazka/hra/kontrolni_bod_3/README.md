# Houbař: 3. kontrolní bod (konec prosince, finální odevzdání)

Ukázka varianty A (hra + web + databáze) v hotovém stavu.

**Téma:** postřehová hra, ve které hráč chytá do košíku padající houby. Jedlé dávají body,
jedovaté berou životy. Výsledky se ukládají do databáze a zobrazují na webu.

| | |
|---|---|
| **Hra** | Python 3 + Pygame |
| **Web** | Flask, HTML 5, CSS 3 |
| **Databáze** | SQLite (5 tabulek, vztahy 1:N i M:N) |
| **Testy** | unittest, 13 testů |

## Spuštění

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python web.py                   # web: http://127.0.0.1:5000
python main.py                  # hra
python -m unittest              # testy
```

Databáze `houbar.db` se vytvoří sama. Připravené účty: `pepa`, `anicka`, `houbar`, heslo `heslo123`.

## Co přibylo od 2. kontrolního bodu

| Požadavek 3. fáze | Kde to najdeš |
|-------------------|---------------|
| doladěné mechaniky | výběr obtížnosti (`hra/vyber_obtiznosti.py`), pauza a zrychlování (`hra/partie.py`), odhlášení v menu |
| hra nepadá | chyba DB se zapíše do `houbar.log` a hráč dostane hlášku (`main.py`) |
| UPDATE, DELETE | změna hesla, smazání partie a účtu (`db.py`, `databaze/dotazy.sql`) |
| ověření normalizace (BCNF) | `databaze/er_diagram.md` |
| web: screenshot, vývojové diagramy | `static/img/hra.png`, stránka *O projektu* |
| web: profil, filtr žebříčku | `templates/profil.html`, `templates/zebricek.html` |
| min. 2 automatizované testy | `tests/test_logika.py`, `tests/test_db.py` |
| 4 dokumenty | `docs/dokumentace.md`, `manual.md`, `prezentace.md`, `prehled.md` |
| 3 vývojové diagramy | `docs/diagramy.md` |

## Splnění zadání

| Část zadání | Splněno čím |
|-------------|-------------|
| Web: min. 4 stránky, navigace, 1 CSS | Úvod, Pravidla, Žebříček, O projektu, Registrace, Přihlášení, Profil; `static/style.css` |
| Web: login, registrace, výsledky z DB | `web.py` |
| Hra: smyčka, menu, ukončení, interakce | `hra/partie.py`, `hra/menu.py` |
| Hra: identifikace hráče, ukládání do DB | `hra/prihlaseni.py`, `db.uloz_partii()` |
| DB: ER diagram, 1:N i M:N | `databaze/er_diagram.md` |
| DB: DDL, DML, SELECT, UPDATE, DELETE | `databaze/schema.sql`, `data.sql`, `dotazy.sql` |
| Propojení | hra, databáze a web přes společný `db.py` |
| Testy | `tests/` |
| Dokumentace | `docs/` + komentáře u všech funkcí a tříd |

## Co který soubor dělá

| Soubor | Popis |
|--------|-------|
| `main.py` | Přepíná obrazovky: menu, přihlášení, obtížnost, partie, konec. Zapíná logování a ošetřuje chyby DB. |
| `db.py` | **Všechny SQL dotazy** pro hru i web: účty, číselníky, uložení partie, žebříček, statistiky, mazání. |
| `web.py` | Webová aplikace: stránky o hře, účet, profil, chybové stránky. |
| `hra/nastaveni.py` | Konstanty hry. |
| `hra/ui.py` | Nápis, tlačítko, textové pole. |
| `hra/menu.py` | Hlavní menu (Hrát / Konec / Odhlásit). |
| `hra/prihlaseni.py` | Přihlášení hráče ve hře. |
| `hra/vyber_obtiznosti.py` | Tlačítka obtížností načtená z tabulky `obtiznost`. |
| `hra/logika.py` | Pravidla bez Pygame: výběr houby, skóre, životy, zrychlování. |
| `hra/objekty.py` | Košík a houba. |
| `hra/partie.py` | Herní smyčka včetně pauzy. |
| `hra/konec.py` | Výsledek partie a pět nejlepších hráčů na dané obtížnosti. |
| `templates/` | HTML šablony (`base.html` = společná kostra, `chyba.html` = chybová stránka). |
| `static/style.css`, `static/img/hra.png` | Vzhled webu a snímek ze hry. |
| `databaze/schema.sql` | CREATE TABLE. |
| `databaze/data.sql` | INSERT, vzorová data. |
| `databaze/dotazy.sql` | SELECT (JOIN, WHERE, ORDER BY, GROUP BY, HAVING, LIKE), UPDATE, DELETE. |
| `databaze/er_diagram.md` | ER diagram, vztahy, zdůvodnění BCNF. |
| `tests/test_logika.py` | 6 testů herních pravidel. |
| `tests/test_db.py` | 7 testů databáze (běží nad DB v paměti). |
| `docs/` | `dokumentace.md`, `manual.md`, `prezentace.md`, `prehled.md`, `diagramy.md`, `navrh.md`. |
| `Issues.txt` | Chyby z peer review. |

## Na co si dát pozor
- Testuj to, na čem záleží, tedy počítání skóre a ukládání do DB. Test, který ověří, že `1 + 1 == 2`, se nepočítá.
- Testy nesmí sahat na skutečnou databázi, proto používají DB v paměti.
- Před odevzdáním smaž `houbar.db` a spusť všechno znovu. Ověříš tím, že projekt jde
  rozjet jen z toho, co je v gitu. Přesně takhle ho budu spouštět já.
- Projekt nesmí spadnout. Vyzkoušej si přihlášení se špatným heslem, neexistující
  adresu na webu a profil bez přihlášení. Všude má být srozumitelná hláška.
