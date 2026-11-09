# Technický přehled

## Datové toky
Prohlížeč odešle formulář → Flask (`app.py`) zkontroluje vstupy → připravený SQL dotaz čte nebo mění SQLite → Flask připraví HTML → prohlížeč stránku zobrazí.

## Kam sáhnout, když chceš něco změnit
- Barvy: `static/style.css`
- Texty na úvodní stránce: `templates/index.html`
- Logika košíku: funkce `pridat_kosik`, `upravit_kosik`, `polozky_kosiku` v `app.py`
- Logika objednávky: `vytvor_objednavku` v `app.py`
- Databázové tabulky: `databaze/schema.sql`

## Rizika
Nedostatek skladu, špatná data z formuláře, zapomenuté přihlášení, nespuštěná databáze a neúmyslná změna SQL schématu.

## Jak začít s vývojem
Nejprve uprav vzhled nebo texty, pak spusť web a testy. Commituj po jednotlivých malých změnách.
