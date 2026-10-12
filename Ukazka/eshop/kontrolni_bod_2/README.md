# Zelený kout: 2. kontrolní bod (konec listopadu)

Ukázka varianty B (e-shop). Takhle má projekt vypadat na konci 2. fáze:
katalog čte z databáze a zákazník dokáže nakoupit.

## Co přibylo od 1. kontrolního bodu

| Požadavek 2. fáze | Kde to najdeš |
|-------------------|---------------|
| vzorová data (INSERT) | `databaze/data.sql` |
| katalog z DB: kategorie, hledání, řazení | `katalog.py`, `templates/katalog.html` |
| detail produktu | `templates/produkt.html` |
| registrace a přihlášení, hesla jako hash | `ucty.py`, `templates/registrace.html`, `prihlaseni.html` |
| košík | `kosik.py`, `templates/kosik.html` |
| vytvoření objednávky **v transakci** | `objednavky.py`, `templates/objednat.html` |
| SELECT dotazy (JOIN, LEFT JOIN, WHERE, ORDER BY, GROUP BY, LIKE, vnořený dotaz) | `databaze/dotazy.sql` |
| začátek manuálu | `docs/manual.md` |

**Zatím není:** historie objednávek, administrace (produkty a stavy objednávek se dají měnit
jen přímo v databázi), UPDATE a DELETE v `dotazy.sql`, chybové stránky, testy, kompletní dokumentace.

## Spuštění

```bash
pip install -r requirements.txt
python app.py        # http://127.0.0.1:5000
```

Databáze `eshop.db` se vytvoří sama při prvním spuštění.
Zákazníci: `jana@example.com`, `petr@example.com`, `lucie@example.com`, heslo `heslo123`.

## Co který soubor dělá

| Soubor | Popis |
|--------|-------|
| `app.py` | Adresy webu. Přečte požadavek, zavolá funkci z ostatních souborů, vykreslí šablonu. **Žádné SQL.** |
| `db.py` | Připojení k SQLite a vytvoření databáze ze `schema.sql` + `data.sql`. |
| `ucty.py` | `registruj()`, `prihlas()`, otisky hesel (PBKDF2 se solí). |
| `katalog.py` | Dotazy na kategorie a produkty: filtr, hledání (LIKE), řazení, detail, produkty pro košík. |
| `kosik.py` | Košík jako slovník v session: `pridej()`, `nastav()`, `pocet_kusu()`, `sestav_polozky()`. Bez DB a bez Flasku. |
| `objednavky.py` | `vytvor_objednavku()`: objednávka + položky + odečtení skladu v jedné transakci. |
| `templates/` | HTML šablony; `base.html` je společná kostra s navigací, košíkem a zprávami. |
| `static/style.css` | Jediný CSS soubor. |
| `databaze/schema.sql` | CREATE TABLE, VIEW, INDEX, beze změny od 1. kontrolního bodu. |
| `databaze/data.sql` | INSERT, vzorová data včetně čtyř objednávek. |
| `databaze/dotazy.sql` | Ukázkové SELECT dotazy s komentářem, co který ukazuje. |
| `databaze/er_diagram.md` | ER diagram. |
| `docs/navrh.md`, `docs/manual.md` | Návrh projektu a rozpracovaný manuál. |

## Jak probíhá nákup

```
katalog ──▶ Do košíku ──▶ košík (session) ──▶ Objednat ──▶ přihlášení? ──▶ adresa + platba
                                                                               │
                              ┌────────────── jedna transakce ─────────────────▼──┐
                              │ INSERT objednavka                                 │
                              │ pro každou položku: UPDATE sklad, INSERT položka  │
                              │ chyba kdekoli = ROLLBACK, v DB nezůstane nic      │
                              └───────────────────────────────────────────────────┘
```

## Na co si dát pozor
- SQL piš vždy s otazníky místo hodnot, nikdy `f"... WHERE nazev LIKE '%{hledat}%'"`.
  Jediná věc, která se do dotazu skládá textem, je `ORDER BY`, a ta se vybírá z pevného
  slovníku `RAZENI` v `katalog.py`.
- Cenu nikdy neber z formuláře. Košík si pamatuje jen id a množství, cena se vždy čte z databáze.
- Sklad kontroluj až v databázi, ne jen v košíku: `UPDATE ... WHERE sklad >= ?`. Mezi vložením
  do košíku a objednáním mohl zboží koupit někdo jiný.
- Vyzkoušej si rollback: vlož do košíku víc druhů zboží, v druhém okně jedno vykup
  (nebo mu v DB sniž sklad) a objednej. Objednávka nesmí vzniknout ani zčásti.
- Soubor `eshop.db` do gitu nepatří (je v `.gitignore`).
