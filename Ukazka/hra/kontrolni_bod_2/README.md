# Houbař: 2. kontrolní bod (konec listopadu)

Ukázka varianty A (hra + web + databáze). Takhle má projekt vypadat na konci 2. fáze:
hra se dá hrát, ukládá výsledky do databáze a web je zobrazuje.

## Co přibylo od 1. kontrolního bodu

| Požadavek 2. fáze | Kde to najdeš |
|-------------------|---------------|
| základní pohyb a logika hry | `hra/partie.py`, `hra/objekty.py`, `hra/logika.py` |
| vzorová data (INSERT) | `databaze/data.sql` |
| SELECT dotazy (JOIN, WHERE, ORDER BY, GROUP BY, LIKE) | `databaze/dotazy.sql`, `db.py` |
| hra ukládá skóre do DB | `db.uloz_partii()`, volá se z `main.py` |
| web čte data z DB | žebříček a pravidla ve `web.py` |
| login + registrace na webu | `web.py`, `templates/registrace.html`, `prihlaseni.html` |
| identifikace hráče ve hře | `hra/prihlaseni.py` |
| začátek manuálu | `docs/manual.md` |

**Zatím není:** výběr obtížnosti (hraje se jen na *Normální*), pauza, profil hráče,
UPDATE a DELETE, testy, kompletní dokumentace.

## Spuštění

```bash
pip install -r requirements.txt
python web.py        # web: http://127.0.0.1:5000, stránka Registrace
python main.py       # hra: přihlas se účtem z webu
```

Databáze `houbar.db` se vytvoří sama při prvním spuštění. Připravené účty:
`pepa`, `anicka`, `houbar`, heslo `heslo123`.

## Co který soubor dělá

| Soubor | Popis |
|--------|-------|
| `main.py` | Přepíná obrazovky: menu, přihlášení, partie, konec. Po partii zavolá uložení do DB. |
| `db.py` | **Všechny SQL dotazy.** Připojení, vytvoření DB ze skriptů, hesla, hráči, partie, žebříček. Používá ho hra i web. |
| `hra/nastaveni.py` | Konstanty: okno, barvy, rozměry košíku a hub, délka partie. |
| `hra/ui.py` | `napis()`, `Tlacitko`, nově `TextovePole` pro psaní jména a hesla. |
| `hra/menu.py` | Hlavní menu; ukazuje, kdo je přihlášený. |
| `hra/prihlaseni.py` | Formulář jméno + heslo, ověření přes `db.prihlas_hrace()`. |
| `hra/logika.py` | Pravidla bez Pygame: `vyber_druh()` (náhodná houba podle četnosti), třída `StavHry` (skóre, životy, sebrané houby). |
| `hra/objekty.py` | Třídy `Kosik` a `Houba`, pohyb a vykreslení. |
| `hra/partie.py` | Herní smyčka: události, aktualizace, vykreslení. |
| `hra/konec.py` | Obrazovka s výsledkem partie. |
| `web.py` | Stránky webu + registrace, přihlášení a odhlášení. |
| `templates/` | HTML šablony; `base.html` je společná kostra s navigací a zprávami. |
| `static/style.css` | Jediný CSS soubor. |
| `databaze/schema.sql` | CREATE TABLE, beze změny od 1. kontrolního bodu. |
| `databaze/data.sql` | INSERT, vzorová data, min. 3 řádky v každé tabulce. |
| `databaze/dotazy.sql` | Ukázkové SELECT dotazy s komentářem, co který ukazuje. |
| `databaze/er_diagram.md` | ER diagram. |
| `docs/navrh.md`, `docs/manual.md` | Návrh projektu a rozpracovaný manuál. |

## Jak jsou části propojené

```
web (registrace) ──INSERT hrac──▶ ┌────────────┐ ◀──SELECT hrac── hra (přihlášení)
web (žebříček)  ◀──SELECT JOIN──  │ houbar.db  │ ◀──INSERT partie, partie_houba── hra (konec partie)
web (pravidla)  ◀──SELECT───────  └────────────┘ ──SELECT obtiznost, druh_houby──▶ hra (partie)
```

## Na co si dát pozor
- SQL piš jen na jednom místě (`db.py`) a vždy s otazníky místo hodnot. Zápis
  `f"... WHERE jmeno = '{jmeno}'"` je chyba, i když zrovna funguje, a u obhajoby se na něj ptám.
- Heslo se neukládá čitelně, jen jeho otisk (`zahashuj_heslo`).
- Uložení partie je transakce. Zápis do `partie` a `partie_houba` proběhne celý, nebo vůbec.
- Pravidla hry jsou mimo Pygame (`logika.py`). Teď to vypadá jako zbytečnost, ale ve 3. fázi
  díky tomu napíšeš testy na pár řádků.
- Soubor `houbar.db` do gitu nepatří (je v `.gitignore`), databáze se dá kdykoli vytvořit ze SQL skriptů.
