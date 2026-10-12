# Zelený kout: 3. kontrolní bod (konec prosince, finální odevzdání)

Ukázka varianty B (e-shop) v hotovém stavu.

**Téma:** e-shop s pokojovými rostlinami a doplňky. Zákazník nakupuje přes katalog
a košík, administrátor spravuje produkty a vyřizuje objednávky.

| | |
|---|---|
| **Server** | Python 3 + Flask |
| **Web** | HTML 5, CSS 3 (bez frameworku) |
| **Databáze** | SQLite, 8 tabulek, 2 vztahy M:N, pohled, 2 indexy |
| **Testy** | unittest, 15 testů, z toho 7 nad databází |

## Spuštění

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python app.py                   # http://127.0.0.1:5000
python -m unittest              # testy
```

Databáze `eshop.db` se vytvoří sama.

| E-mail | Heslo | Role |
|--------|-------|------|
| `jana@example.com`, `petr@example.com`, `lucie@example.com` | `heslo123` | zákazník |
| `admin@zelenykout.example` | `admin123` | administrátor |

## Co přibylo od 2. kontrolního bodu

| Požadavek 3. fáze | Kde to najdeš |
|-------------------|---------------|
| historie objednávek zákazníka | `templates/objednavky.html`, `objednavka.html` |
| administrace: CRUD produktů | `katalog.py` (dolní část), `templates/admin_produkty.html`, `admin_produkt.html` |
| administrace: stavy objednávek | `objednavky.zmen_stav()`, `templates/admin_objednavky.html` |
| administrace: přehled a statistiky | `objednavky.souhrn()`, `trzby_podle_kategorie()`, `nejprodavanejsi()` |
| UPDATE, DELETE, HAVING, pohled, transakce v SQL | `databaze/dotazy.sql` |
| zdůvodnění normalizace (BCNF) | `databaze/er_diagram.md` |
| ošetření chyb | chybové stránky 403/404/500 v `app.py`, `templates/chyba.html` |
| min. 4 testy, 2 nad databází | `tests/` |
| 4 dokumenty + 3 vývojové diagramy | `docs/` |

## Splnění zadání (varianta B)

| Část zadání | Splněno čím |
|-------------|-------------|
| katalog, filtr, hledání, řazení, detail | `/katalog`, `/produkt/<id>` |
| registrace, přihlášení, hash hesel | `ucty.py` |
| košík | `kosik.py`, `/kosik` |
| objednávka s kontrolou skladu | `objednavky.vytvor_objednavku()` |
| historie objednávek | `/objednavky`, `/objednavka/<id>` |
| administrace: CRUD, stavy, 2 statistiky | `/admin`, `/admin/produkty`, `/admin/objednavky` |
| min. 6 stránek, 1 CSS | 16 stránek (18 šablon), `static/style.css` |
| validace vstupů na serveru | `ValueError` v `kosik.py`, `ucty.py`, `katalog.py`, `objednavky.py` |
| rozšířené požadavky na DB | tabulka v [`docs/dokumentace.md`](docs/dokumentace.md#databáze) |

## Co který soubor dělá

| Soubor | Popis |
|--------|-------|
| `app.py` | Adresy webu: obchod, košík, účet, moje objednávky, administrace, chybové stránky. **Žádné SQL.** |
| `db.py` | Připojení k SQLite a vytvoření databáze ze skriptů. |
| `ucty.py` | Registrace, přihlášení, otisky hesel. |
| `katalog.py` | Dotazy na produkty a kategorie; pro administraci `uloz_produkt()`, `nastav_aktivni()`, `smaz_produkt()`. |
| `kosik.py` | Košík, čisté funkce nad slovníkem. |
| `objednavky.py` | Vytvoření objednávky (transakce), historie, změna stavu s vracením na sklad, statistiky. |
| `templates/base.html` | Společná kostra: navigace, košík, zprávy. |
| `templates/index.html`, `katalog.html`, `produkt.html`, `doprava.html`, `o_projektu.html` | Veřejná část obchodu. |
| `templates/kosik.html`, `objednat.html` | Košík a dokončení objednávky. |
| `templates/registrace.html`, `prihlaseni.html` | Účet. |
| `templates/objednavky.html`, `objednavka.html` | Historie a detail objednávky. |
| `templates/admin_*.html` | Administrace; `admin_menu.html` je společná podnabídka. |
| `templates/chyba.html` | Chybová stránka. |
| `static/style.css` | Jediný CSS soubor. |
| `databaze/schema.sql` | CREATE TABLE, VIEW, INDEX. |
| `databaze/data.sql` | INSERT, vzorová data. |
| `databaze/dotazy.sql` | 15 komentovaných dotazů: SELECT všech druhů, UPDATE, DELETE, transakce. |
| `databaze/er_diagram.md` | ER diagram, vztahy, chování při mazání, zdůvodnění BCNF. |
| `tests/test_kosik.py` | 4 testy košíku. |
| `tests/test_objednavky.py` | 7 testů nad databází (objednávka, rollback, historie cen, storno, mazání, hledání). |
| `tests/test_web.py` | 4 testy webu (celý nákup, přihlášení, práva). |
| `docs/` | `dokumentace.md`, `manual.md`, `prezentace.md`, `prehled.md`, `diagramy.md`, `navrh.md`. |
| `Issues.txt` | Chyby z peer review. |

## Na co si dát pozor
- Testuj to, co se může pokazit: objednávku při nedostatku zboží, zdražení po nákupu,
  zrušení objednávky, cizí objednávku, zákazníka v administraci.
- Práva kontroluj na serveru. Schovat odkaz *Administrace* nestačí, adresu `/admin`
  může kdokoli napsat ručně. Každá admin funkce začíná voláním `jen_admin()`.
- Mazat, nebo skrývat? Prodaný produkt smazat nejde (a nemá jít). Proto má sloupec `aktivni`.
- Před odevzdáním smaž `eshop.db` a spusť všechno znovu. Ověříš tím, že projekt jde
  rozjet jen z toho, co je v gitu. Přesně takhle ho budu spouštět já.
