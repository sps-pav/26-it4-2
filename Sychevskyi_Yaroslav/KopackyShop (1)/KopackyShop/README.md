# ⚽ KopačkyShop

Školní e-shop s fotbalovými kopačkami (Nike, Adidas, Puma). Flask + SQLite, tmavě zelený motiv.

## Spuštění (Windows)
1. Otevři příkazový řádek ve složce `KopackyShop`.
2. `py -m venv .venv`
3. `.venv\Scripts\activate`
4. `py -m pip install -r requirements.txt`
5. `py app.py`
6. Otevři http://127.0.0.1:5000

(macOS/Linux: `source .venv/bin/activate`.) Při prvním spuštění se sama vytvoří databáze `obchod.db`.

## Demo účty
- Zákazník: `zakaznik@demo.cz` / `demo1234`
- Admin: `admin@demo.cz` / `demo1234`

## Složky
- `app.py` – celý backend (stránky, košík, objednávky, admin)
- `db_config.py` – cesta k databázi
- `templates/` – HTML stránky
- `static/style.css` – vzhled (barvy, písmo)
- `static/images/` – obrázky kopaček
- `databaze/` – `schema.sql` (tabulky), `data.sql` (ukázkové kopačky)

## Obrázky kopaček
Dej fotku do `static/images/` a pojmenuj ji podle ID produktu: `kopacky-<ID>.jpg`
(např. `kopacky-5.jpg`; funguje i `.png` a `.webp`). Fotka má přednost před SVG ilustrací,
databázi měnit nemusíš. Bez souboru se ukáže `placeholder.svg`.
