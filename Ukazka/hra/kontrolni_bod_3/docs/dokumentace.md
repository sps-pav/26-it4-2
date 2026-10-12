# Dokumentace: Houbař

## Účel
Houbař je postřehová hra s webovou prezentací. Hráč chytá padající houby, výsledky
se ukládají do databáze a zobrazují se na webu v žebříčku a v profilu hráče.

## Technologie

| Oblast | Technologie | Verze |
|--------|-------------|-------|
| Hra | Python, Pygame | Python 3.10+, Pygame 2 |
| Web | Flask, HTML 5, CSS 3 | Flask 3 |
| Databáze | SQLite (modul `sqlite3` je součástí Pythonu) | 3 |
| Testy | `unittest` (součást Pythonu) | |

## Struktura projektu

```
├── main.py            spuštění hry, přepínání obrazovek
├── web.py             webová aplikace (adresy a jejich obsluha)
├── db.py              všechny SQL dotazy, společné pro hru i web
├── hra/               herní část
│   ├── nastaveni.py       konstanty (velikost okna, barvy, rychlosti)
│   ├── ui.py              nápis, tlačítko, textové pole
│   ├── menu.py            hlavní menu
│   ├── prihlaseni.py      přihlašovací obrazovka
│   ├── vyber_obtiznosti.py výběr obtížnosti z databáze
│   ├── partie.py          herní smyčka
│   ├── objekty.py         košík a houba
│   ├── logika.py          pravidla bez Pygame (skóre, životy, náhoda)
│   └── konec.py           obrazovka s výsledkem
├── templates/         HTML šablony webu
├── static/            CSS a obrázky
├── databaze/          schema.sql, data.sql, dotazy.sql, ER diagram
├── tests/             automatizované testy
└── docs/              tato dokumentace
```

## Spuštění

```bash
python -m venv .venv
.venv\Scripts\activate              # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python web.py                       # web: http://127.0.0.1:5000
python main.py                      # hra
python -m unittest                  # testy
```

Databázi není potřeba vytvářet ručně, při prvním spuštění ji `db.py` založí
ze souborů `databaze/schema.sql` a `databaze/data.sql`. Ruční vytvoření:

```bash
sqlite3 houbar.db < databaze/schema.sql
sqlite3 houbar.db < databaze/data.sql
```

Chceš začít s čistou databází? Smaž soubor `houbar.db` a spusť hru nebo web znovu.

## Závislosti
`pygame` a `flask` (viz `requirements.txt`). Nic dalšího se neinstaluje.

## Databáze
Pět tabulek: `hrac`, `obtiznost`, `druh_houby`, `partie`, `partie_houba`.
Vztahy 1:N (hráč a partie, obtížnost a partie) a M:N (partie a druh houby).
ER diagram a zdůvodnění normalizace: [`databaze/er_diagram.md`](../databaze/er_diagram.md).

## Omezení
- Web běží na vývojovém serveru Flasku, je určený jen pro jeden počítač (localhost).
- SQLite je soubor na disku, takže hra a web musí běžet na stejném počítači.
- Hesla jsou uložená jako otisk (PBKDF2 se solí), web ale nepoužívá HTTPS ani ochranu proti CSRF.
- Hra nemá zvuky a grafika je kreslená jen základními tvary Pygame.
- Okno hry má pevnou velikost 800 × 600.
