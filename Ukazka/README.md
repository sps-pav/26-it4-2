# Ukázkový projekt

Hotová ukázka maturitního projektu v obou variantách podle [zadání](../zadani.md),
rozdělená podle kontrolních bodů. Každá složka `kontrolni_bod_N` je samostatný
spustitelný projekt ve stavu, v jakém ho chci vidět na konci dané fáze.

| | [Varianta A: hra](hra/) | [Varianta B: e-shop](eshop/) |
|---|---|---|
| **Téma** | *Houbař*, chytání padajících hub | *Zelený kout*, obchod s pokojovými rostlinami |
| **Technologie** | Python + Pygame, Flask, SQLite | Python + Flask, SQLite |
| **Databáze** | 5 tabulek, 1× M:N | 8 tabulek, 2× M:N, pohled, indexy, transakce |
| **1. kontrolní bod** (říjen) | [menu, kostra webu, návrh DB](hra/kontrolni_bod_1/) | [kostra webu, návrh DB](eshop/kontrolni_bod_1/) |
| **2. kontrolní bod** (listopad) | [hratelná hra, skóre v DB, login](hra/kontrolni_bod_2/) | [katalog z DB, košík, objednávka](eshop/kontrolni_bod_2/) |
| **3. kontrolní bod** (prosinec) | [hotový projekt](hra/kontrolni_bod_3/) | [hotový projekt](eshop/kontrolni_bod_3/) |

## Jak ukázku číst

1. Otevři `README.md` v kontrolním bodě, který tě zajímá. Je tam napsáno, co má být hotové,
   co ještě chybí, a tabulka, co který soubor dělá.
2. Projekt si spusť. Postup je v každém README, stačí `pip install -r requirements.txt`.
3. Porovnej dva po sobě jdoucí kontrolní body, uvidíš, kolik práce je mezi termíny.
   Ve VS Code klikni pravým tlačítkem na první složku a zvol *Select for Compare*, potom pravým na druhou a zvol *Compare with Selected*.

## Co si z ukázky odnést

- Rozsah: kolik toho má být hotové v říjnu, v listopadu a v prosinci.
- Strukturu: SQL na jednom místě, logika oddělená od kreslení a od webu, jedna společná šablona.
- Dokumentaci: jak má vypadat README, návrh s datovými toky, ER diagram, manuál a ostatní dokumenty.
- Práci s databází: parametrizované dotazy, transakce, cizí klíče, vzorová data a okomentované dotazy.

## Co z ukázky nejde

- Zvolit si stejné téma. *Houbař* ani *Zelený kout* už jsou obsazené.
- Kopírovat kód. Projekt je individuální a u obhajoby musíš umět vysvětlit každý řádek.
  Vlastní strukturu složek mít můžeš, povinné jsou jen `README.md` a `Issues.txt`
  (viz [README repa](../README.md)).

## Poznámky k technologiím

- Ukázka používá SQLite, aby šla spustit kdekoli bez účtu a bez sítě. V `schema.sql`
  je proto `AUTOINCREMENT` místo `AUTO_INCREMENT` a `TEXT` místo `VARCHAR`. Pokud děláš
  projekt na školním MySQL, struktura i dotazy zůstávají stejné, liší se jen tyto detaily
  a připojení (`mysql.connector`, `%s` místo `?`).
- Web je ve Flasku. Pokud děláš web v PHP, platí stejné principy: jedna společná hlavička,
  dotazy přes připravené příkazy (prepared statements), hesla přes `password_hash()`.
- Diagramy jsou psané v jazyce Mermaid (GitHub i GitLab je vykreslí). Můžeš je stejně dobře
  nakreslit v draw.io a přiložit jako obrázek.
