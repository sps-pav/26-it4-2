# Varianta B: e-shop *Zelený kout*

Obchod s pokojovými rostlinami ve Flasku: katalog, košík, objednávky a administrace
nad SQLite databází. E-shop nemá herní část, proto má podle zadání **rozsáhlejší databázi**
(8 tabulek, 2 vztahy M:N, pohled, indexy, transakce) a **víc testů**.

| Kontrolní bod | Stav | Obchod | Administrace | Databáze | Dokumentace a testy |
|---------------|------|--------|--------------|----------|---------------------|
| [1 (konec října)](kontrolni_bod_1/) | návrh a kostra | 4 stránky s navigací, katalog se statickými daty | zatím není | celé `schema.sql` (tabulky, pohled, indexy), ER diagram | návrh s datovými toky |
| [2 (konec listopadu)](kontrolni_bod_2/) | dá se nakoupit | katalog z DB (filtr, hledání, řazení), detail, registrace, přihlášení, košík, objednávka v transakci | zatím není | + `data.sql`, SELECT dotazy | + rozpracovaný manuál |
| [3 (konec prosince)](kontrolni_bod_3/) | hotovo | + historie a detail objednávek, chybové stránky | produkty (CRUD), stavy objednávek, statistiky | + UPDATE, DELETE, HAVING, transakce, BCNF | 4 dokumenty, 3 diagramy, 15 testů |

## Jak roste počet souborů

| | KB 1 | KB 2 | KB 3 |
|---|:---:|:---:|:---:|
| Python moduly | 1 | 6 | 6 |
| HTML šablony | 5 | 10 | 18 |
| SQL skripty | 1 | 3 | 3 |
| dokumenty v `docs/` | 1 | 2 | 6 |
| testy | 0 | 0 | 15 |

## Spuštění libovolného kontrolního bodu

```bash
cd kontrolni_bod_3
pip install -r requirements.txt
python app.py        # http://127.0.0.1:5000
python -m unittest   # testy (jen kontrolní bod 3)
```

Přihlášení: zákazník `jana@example.com` / `heslo123`, administrátor `admin@zelenykout.example` / `admin123`
(účty existují od 2. kontrolního bodu, administrace od 3.).
