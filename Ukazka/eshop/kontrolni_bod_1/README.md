# Zelený kout: 1. kontrolní bod (konec října)

Ukázka varianty B (e-shop). Takhle má projekt vypadat na konci 1. fáze.

**Téma:** e-shop s pokojovými rostlinami a doplňky. Zákazník nakupuje přes katalog
a košík, administrátor spravuje produkty a vyřizuje objednávky.

## Co má být hotové a jestli to tu je

| Požadavek 1. fáze | Kde to najdeš |
|-------------------|---------------|
| výběr tématu (sortimentu) | tento soubor, `docs/navrh.md` |
| kostra webu s navigací | `app.py`, `templates/`, `static/style.css` |
| návrh rozložení projektu, datové toky | `docs/navrh.md` |
| návrh **všech** tabulek, ER diagram | `databaze/er_diagram.md` |
| CREATE TABLE skripty | `databaze/schema.sql` |

**Zatím není (a nevadí to):** databáze není připojená, katalog ukazuje čtyři produkty
napsané v `app.py`. Chybí košík, přihlášení, objednávky, administrace, testy.

## Spuštění

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python app.py                   # http://127.0.0.1:5000
```

## Co který soubor dělá

| Soubor | Popis |
|--------|-------|
| `app.py` | Flask aplikace se čtyřmi stránkami, filtr `kc` pro formát ceny a dočasný seznam `PRODUKTY`. |
| `templates/base.html` | Společná kostra stránek: hlavička, navigace, patička. |
| `templates/index.html` | Úvodní stránka. |
| `templates/katalog.html` | Karty produktů. Už teď používá názvy sloupců z databáze (`nazev`, `cena_kc`, `sklad`). |
| `templates/doprava.html` | Doprava, platba a stavy objednávky. |
| `templates/o_projektu.html` | Autor, technologie, stav projektu. |
| `static/style.css` | Jediný CSS soubor, bez frameworku. |
| `databaze/schema.sql` | Návrh celé databáze: 8 tabulek, pohled, 2 indexy. U každého cizího klíče komentář, proč má zvolené `ON DELETE`. |
| `databaze/er_diagram.md` | ER diagram a tabulka vztahů. |
| `docs/navrh.md` | Téma, části projektu, datové toky, plán práce. |
| `requirements.txt` | Seznam knihoven pro `pip install`. |
| `Issues.txt` | Sem zapisují spolužáci chyby při peer review. |

## Na co si dát pozor
- U e-shopu je databáze hlavní část práce. V 1. fázi má být navržená celá, včetně
  objednávek a položek, i když se zatím nepoužívá. Přečti si
  [rozšířené požadavky v zadání](../../../zadani.md#rozšířené-požadavky-na-databázi-pro-e-shop-varianta-b).
- Položka objednávky má vlastní cenu. Nejčastější chyba, kterou v návrzích vídám, je počítat cenu staré
  objednávky z aktuální ceny produktu.
- Rozmysli si mazání. Co se má stát s objednávkami, když smažu zákazníka? A s položkami,
  když smažu produkt? Odpověď patří do `schema.sql` jako `ON DELETE ...`.
- Dočasná data v kódu pojmenuj stejně jako budoucí sloupce v DB, šablonu pak nebudeš přepisovat.
- Commity v této fázi mohly vypadat třeba takhle:
  `feat: kostra webu a navigace`, `feat: katalog se statickými daty`, `docs: návrh a datové toky`,
  `docs: ER diagram`, `feat: schema.sql (tabulky, pohled, indexy)`.
