# Dokumentace: Zelený kout

## Účel
Zelený kout je školní e-shop s pokojovými rostlinami. Ukazuje celou cestu zboží od katalogu přes košík a objednávku až po vyřízení
v administraci, to vše nad jednou relační databází.

## Technologie

| Oblast | Technologie | Verze |
|--------|-------------|-------|
| Server | Python, Flask | Python 3.10+, Flask 3 |
| Web | HTML 5, CSS 3, šablony Jinja | |
| Databáze | SQLite (modul `sqlite3` je součástí Pythonu) | 3 |
| Testy | `unittest` (součást Pythonu) | |

## Struktura projektu

```
├── app.py             adresy webu a jejich obsluha (žádné SQL)
├── db.py              připojení k databázi, vytvoření DB ze skriptů
├── ucty.py            registrace, přihlášení, otisky hesel
├── katalog.py         dotazy na produkty a kategorie + správa produktů
├── kosik.py           košík, čisté funkce nad slovníkem
├── objednavky.py      vytvoření objednávky (transakce), stavy, statistiky
├── templates/         HTML šablony (base.html = společná kostra)
├── static/style.css   jediný CSS soubor
├── databaze/          schema.sql, data.sql, dotazy.sql, ER diagram
├── tests/             automatizované testy
└── docs/              tato dokumentace
```

## Spuštění

```bash
python -m venv .venv
.venv\Scripts\activate              # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python app.py                       # http://127.0.0.1:5000
python -m unittest                  # testy
```

Databázi není potřeba vytvářet ručně, při prvním spuštění ji `db.py` založí
ze souborů `databaze/schema.sql` a `databaze/data.sql`. Ruční vytvoření:

```bash
sqlite3 eshop.db < databaze/schema.sql
sqlite3 eshop.db < databaze/data.sql
```

Chceš začít s čistou databází? Smaž soubor `eshop.db` a spusť aplikaci znovu.

## Závislosti
Jen `flask` (viz `requirements.txt`).

## Databáze

| Požadavek zadání (varianta B) | Jak je splněn |
|-------------------------------|---------------|
| min. 7 tabulek | 8: `uzivatel`, `dodavatel`, `kategorie`, `produkt`, `produkt_kategorie`, `stav_objednavky`, `objednavka`, `polozka_objednavky` |
| min. 2 vztahy M:N, jeden s atributy | `produkt_kategorie`; `polozka_objednavky` (množství, cena za kus) |
| CHECK a zvolené ON DELETE | `schema.sql`, u každého cizího klíče komentář proč |
| transakce při objednávce | `objednavky.vytvor_objednavku()` |
| historie cen | `polozka_objednavky.cena_za_kus_kc` |
| pohled | `v_objednavka`, používá ho historie objednávek i administrace |
| vlastní index | `idx_objednavka_uzivatel`, `idx_polozka_produkt` |
| LEFT JOIN, HAVING, vnořený dotaz, agregace | `databaze/dotazy.sql`, `katalog.py`, `objednavky.py` |
| parametrizované dotazy, hash hesel | všude otazníky; `ucty.zahashuj_heslo()` |
| zdůvodnění BCNF | [`databaze/er_diagram.md`](../databaze/er_diagram.md) |

## Omezení
- Vývojový server Flasku, určený jen pro jeden počítač (localhost).
- Žádná skutečná platba, doprava ani odesílání e-mailů.
- Košík je v session, takže po odhlášení nebo na jiném zařízení je prázdný.
- Formuláře nemají ochranu proti CSRF a web neběží přes HTTPS.
- Produkty nemají fotografie (jen zástupný symbol).
- Ceny jsou v celých korunách a bez DPH.
