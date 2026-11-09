# ⚽ KopačkyShop – maturitní projekt 2026/27

**Varianta B: E-shop bez hry.** Obchod s fotbalovými kopačkami Nike, Adidas a Puma.

**Autor:** DOPLŇ PŘÍJMENÍ A JMÉNO.

## Jak to spustit (Windows)
1. Otevři příkazový řádek ve složce `KopackyShop`.
2. `python -m venv .venv`
3. `.venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python app.py`
6. V prohlížeči otevři **http://127.0.0.1:5000**.

Na macOS/Linux se prostředí aktivuje pomocí `source .venv/bin/activate`.

Při prvním spuštění se automaticky založí `obchod.db` se vzorovými daty.

## Demo přístupy (jen pro školní ukázku)
- Zákazník: `zakaznik@demo.cz` / `demo1234`
- Administrátor: `admin@demo.cz` / `demo1234`

Tyto účty jsou určené pouze na lokální zkoušení. Projekt nevystavuj veřejně bez změny hesel a `SECRET_KEY`.

## Co který soubor dělá
- `app.py` – backend: adresy stránek, ověření uživatele, košík, objednávky, administrace.
- `db_config.py` – cesta k databázi.
- `templates/` – HTML stránky a tlačítka (frontend).
- `static/style.css` – vzhled obchodu (frontend).
- `databaze/schema.sql` – tabulky, klíče, index, VIEW.
- `databaze/data.sql` – ukázkové kopačky, role, kategorie, velikosti.
- `databaze/dotazy.sql` – SQL ukázky pro zadání.
- `databaze/er_diagram.md` – ER diagram v Mermaid formátu.
- `tests/` – čtyři automatizované testy.
- `docs/` – dokumentace, manuál, prezentace a diagramy.
- `Issues.txt` – chyby z peer review zapisované spolužáky.

## Jak spustit testy
`python -m pytest -q`

## Co si před odevzdáním upravit
Doplň autora a vlastní texty, přidej vlastní fotografie kopaček s povolením použití, projdi ručně všechny funkce a ukaž učiteli, že kódu rozumíš. Pozor, databáze se necommituje (je v `.gitignore`).

## Omezení
Platba se jen simuluje; neukládají se skutečná platební data. Obrázky jsou zatím jednoduché symboly bot. Pro školní lokální provoz, nikoliv veřejný produkční e-shop.
