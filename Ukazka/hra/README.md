# Varianta A: hra *Houbař*

Postřehová hra v Pygame: hráč chytá do košíku padající houby. Jedlé dávají body,
jedovaté berou životy. K tomu web ve Flasku (registrace, žebříček, profil) a SQLite databáze.

| Kontrolní bod | Stav | Hra | Web | Databáze | Dokumentace a testy |
|---------------|------|-----|-----|----------|---------------------|
| [1 (konec října)](kontrolni_bod_1/) | návrh a kostra | okno, hlavní menu | 4 stránky s navigací, bez DB | `schema.sql`, ER diagram | návrh s datovými toky |
| [2 (konec listopadu)](kontrolni_bod_2/) | hratelné a propojené | přihlášení, pohyb, kolize, skóre, uložení partie | registrace, přihlášení, žebříček a pravidla z DB | + `data.sql`, SELECT dotazy | + rozpracovaný manuál |
| [3 (konec prosince)](kontrolni_bod_3/) | hotovo | + obtížnosti, pauza, zrychlování, logování chyb | + profil, filtr žebříčku, diagramy, screenshot | + UPDATE, DELETE, BCNF | 4 dokumenty, 3 diagramy, 13 testů |

## Jak roste počet souborů

| | KB 1 | KB 2 | KB 3 |
|---|:---:|:---:|:---:|
| herní moduly ve složce `hra/` | 3 | 8 | 9 |
| HTML šablony | 5 | 7 | 9 |
| SQL skripty | 1 | 3 | 3 |
| dokumenty v `docs/` | 1 | 2 | 6 |
| testy | 0 | 0 | 13 |

## Spuštění libovolného kontrolního bodu

```bash
cd kontrolni_bod_3
pip install -r requirements.txt
python web.py        # web: http://127.0.0.1:5000
python main.py       # hra
python -m unittest   # testy (jen kontrolní bod 3)
```
