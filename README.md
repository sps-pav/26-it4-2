# Maturitní projekty IT4 (2026/27)

- **Zadání projektu:** [zadani.md](zadani.md) – varianta A (hra + web + databáze) nebo varianta B (e-shop s rozšířenou databází)
- **Hotová ukázka obou variant po kontrolních bodech:** [Ukazka](Ukazka/)

## Struktura repa

Každý student má **jednu složku** `Prijmeni_Jmeno` a pracuje **jen v ní**.
Jak si ji uvnitř uspořádáš, je na tobě. Jako inspirace slouží:

- [Pepa_Ukazka](Pepa_Ukazka/) – **prázdná kostra** složek, kterou si můžeš zkopírovat,
- [Ukazka](Ukazka/) – **hotové ukázkové projekty** (hra *Houbař* a e-shop *Zelený kout*),
  každý ve stavu po 1., 2. a 3. kontrolním bodě, s popisem, co který soubor dělá.

Ani jedna struktura není povinná (např. Flask projekt bude mít v kořeni `app.py`,
`templates/`, `static/`).

Povinně ve složce musí být jen:
- `README.md` – téma projektu a jak ho spustit
- `Issues.txt` – sem zapisují spolužáci chyby z peer review (formát viz [zadani.md](zadani.md))

Kostra (`Pepa_Ukazka`):

```
Pepa_Ukazka/
├── README.md               ← téma projektu + jak ho spustit (vyplň!)
├── Issues.txt              ← sem zapisují spolužáci chyby z peer review
├── requirements.txt        ← Python knihovny (pygame, mysql-connector-python, pytest…)
├── db_config.py            ← připojení k DB (doplň své údaje)
├── hra/                    ← hra / desktopová aplikace
├── web/                    ← webová prezentace (HTML, CSS, PHP…)
├── databaze/
│   ├── schema.sql          ← CREATE TABLE (DDL)
│   ├── data.sql            ← INSERT – min. 3 záznamy do každé tabulky
│   ├── dotazy.sql          ← SELECT / UPDATE / DELETE
│   └── er_diagram.*        ← ER diagram (png, pdf, drawio…)
├── tests/                  ← min. 2 automatizované testy
└── docs/                   ← dokumentace, manual, prezentace, prehled (+ diagramy)
```

## Pravidla pro git

1. **Saháš jen do své složky.** Cizí složku upravuješ jedině kvůli zápisu do `Issues.txt` při peer review.
2. **Commituj často a popisně** – min. 5 commitů na fázi:
   `feat: přidán hlavní menu`, `fix: hra padala při kolizi`, `docs: ER diagram`, `update: …`
3. **Před prací vždy `git pull`**, po práci `git add`, `git commit`, `git push`.
4. **Připojení k DB měj na jednom místě** – v `db_config.py`, který commituješ spolu s projektem (je to školní projekt, ne produkce). Nedávej tam ale heslo, které používáš i jinde.
5. **Databázový soubor (`.db`) se necommituje** (je v `.gitignore`) – DB musí jít vytvořit ze SQL skriptů v repu (`schema.sql`, `data.sql`), ty commituj vždy.
6. **Necommituj:** `venv/`, `.idea/`, `.vscode/`, `.zip`, `.exe`, zkopírované materiály z hodin ani klon celého repa do své složky.
7. Velké soubory (hudba, videa) drž rozumně malé – **jeden soubor max. ~10 MB**.

## První spuštění

```bash
git clone <url-repa>
cd <repo>/Prijmeni_Jmeno
python -m venv .venv
.venv\Scripts\activate            # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Kontrolní termíny

| Termín | Varianta A – hra | Varianta B – e-shop | Jak to má vypadat |
|--------|------------------|---------------------|-------------------|
| konec října | téma v README, funkční menu, návrh DB + ER diagram, `schema.sql` | téma v README, kostra webu s navigací, návrh celé DB + ER diagram, `schema.sql` | [hra](Ukazka/hra/kontrolni_bod_1/) · [e-shop](Ukazka/eshop/kontrolni_bod_1/) |
| konec listopadu | pohyb a logika hry, práce s DB, propojení web ↔ DB ↔ hra | katalog z DB, registrace a přihlášení, košík, objednávka v transakci | [hra](Ukazka/hra/kontrolni_bod_2/) · [e-shop](Ukazka/eshop/kontrolni_bod_2/) |
| konec prosince | **finální odevzdání** – vše podle [zadani.md](zadani.md) | **finální odevzdání** – vše včetně administrace | [hra](Ukazka/hra/kontrolni_bod_3/) · [e-shop](Ukazka/eshop/kontrolni_bod_3/) |
