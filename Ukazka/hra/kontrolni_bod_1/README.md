# Houbař: 1. kontrolní bod (konec října)

Ukázka varianty A (hra + web + databáze). Takhle má projekt vypadat na konci 1. fáze.

**Téma:** postřehová hra, ve které hráč chytá do košíku padající houby. Jedlé dávají body,
jedovaté berou životy. Výsledky se budou ukládat do databáze a zobrazovat na webu.

## Co má být hotové a jestli to tu je

| Požadavek 1. fáze | Kde to najdeš |
|-------------------|---------------|
| výběr tématu | tento soubor, `docs/navrh.md` |
| funkční hlavní menu, základní okno Pygame | `main.py`, `hra/menu.py` |
| návrh rozložení projektu, datové toky | `docs/navrh.md` |
| návrh databáze, ER diagram | `databaze/er_diagram.md` |
| CREATE TABLE skripty | `databaze/schema.sql` |
| struktura HTML souborů, navigace | `web.py`, `templates/`, `static/style.css` |

**Zatím není (a nevadí to):** samotná hra, propojení s databází, přihlášení, testy.
Tlačítko *Hrát* ukáže jen obrazovku „Hra se připravuje“, žebříček na webu je prázdný.

## Spuštění

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python main.py                  # hra (zatím jen menu)
python web.py                   # web: http://127.0.0.1:5000
```

## Co který soubor dělá

| Soubor | Popis |
|--------|-------|
| `main.py` | Spustí hru: vytvoří okno a v cyklu zobrazuje menu, dokud hráč nezvolí Konec. |
| `hra/nastaveni.py` | Konstanty: velikost okna, FPS, barvy. |
| `hra/ui.py` | Funkce `napis()` a třída `Tlacitko`, protože Pygame hotová tlačítka nemá. |
| `hra/menu.py` | Hlavní menu (Hrát / Konec) a dočasná obrazovka „Hra se připravuje“. |
| `web.py` | Flask aplikace se čtyřmi stránkami. Zatím bez databáze. |
| `templates/base.html` | Společná kostra stránek: hlavička, navigace, patička. |
| `templates/index.html`, `pravidla.html`, `zebricek.html`, `o_projektu.html` | Jednotlivé stránky; dědí z `base.html`. |
| `static/style.css` | Jediný CSS soubor pro celý web. |
| `databaze/schema.sql` | Návrh všech pěti tabulek (CREATE TABLE s PK, FK, UNIQUE, NOT NULL, DEFAULT, CHECK). |
| `databaze/er_diagram.md` | ER diagram a popis vztahů 1:N a M:N. |
| `docs/navrh.md` | Téma, části projektu, datové toky a plán práce. |
| `requirements.txt` | Seznam knihoven pro `pip install`. |
| `Issues.txt` | Sem zapisují spolužáci chyby při peer review. |

## Na co si dát pozor
- Databázi navrhni celou už teď. `schema.sql` obsahuje i tabulky, které se začnou
  používat až ve 2. fázi. Přidělávat tabulky do rozpracovaného projektu je mnohem pracnější.
- Menu musí opravdu fungovat, myší i klávesnicí, včetně zavření okna křížkem. To je první věc,
  kterou u kontrolního bodu zkouším.
- Navigace webu je v jedné šabloně (`base.html`). Pokud ji máš zkopírovanou v každé stránce,
  oprav to dřív, než stránek přibude.
- Commity v této fázi mohly vypadat třeba takhle:
  `feat: okno hry a hlavní menu`, `feat: kostra webu s navigací`, `docs: návrh a datové toky`,
  `docs: ER diagram`, `feat: schema.sql`.
