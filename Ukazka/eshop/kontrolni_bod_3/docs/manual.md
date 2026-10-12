# Uživatelský manuál: Zelený kout

## 1. Spuštění

```bash
pip install -r requirements.txt
python app.py        # obchod na adrese http://127.0.0.1:5000
```

Databáze `eshop.db` se vytvoří sama při prvním spuštění.

## 2. Účty k vyzkoušení

| E-mail | Heslo | Role |
|--------|-------|------|
| `jana@example.com`, `petr@example.com`, `lucie@example.com` | `heslo123` | zákazník |
| `admin@zelenykout.example` | `admin123` | administrátor |

Vlastní účet si vytvoříš na stránce **Registrace**.

## 3. Nákup krok za krokem
1. **Katalog**: vyber kategorii, hledej podle názvu nebo popisu, seřaď podle ceny.
2. Kliknutím na název otevřeš **detail produktu** (popis, dodavatel, kategorie, počet kusů skladem).
3. **Do košíku**: z katalogu přidá 1 kus, z detailu zvolené množství.
4. **Košík**: změň množství (0 = odebrat), dole vidíš celkovou cenu.
5. **Pokračovat k objednávce**: pokud nejsi přihlášený, obchod tě pošle na přihlášení.
6. Vyplň doručovací adresu, vyber způsob platby a potvrď **Závazně objednat**.
7. Zobrazí se detail nové objednávky. Všechny své objednávky najdeš pod **Moje objednávky**.

## 4. Administrace
Po přihlášení administrátora přibude v navigaci odkaz **Administrace**.

| Stránka | Co na ní uděláš |
|---------|-----------------|
| Přehled | počet nových objednávek, celkové tržby, docházející zboží, tržby podle kategorie, nejprodávanější produkty |
| Produkty | **+ Nový produkt**, úprava (klik na název), **Skrýt / Zobrazit**, **Smazat** |
| Objednávky | filtr podle stavu, změna stavu (nová, zaplacená, odeslaná, případně zrušená) |

- Produkt, který už si někdo objednal, smazat nejde, dá se jen skrýt z nabídky.
- Zrušení objednávky vrátí zboží na sklad. Zrušenou objednávku už nejde změnit.

## 5. Příklad použití
1. Přihlásím se jako `lucie@example.com`.
2. V katalogu vyberu kategorii *Sukulenty a kaktusy*, seřadím od nejlevnějšího.
3. Vložím do košíku 2× Echeveria a 1× Aloe vera, objednám na dobírku.
4. Odhlásím se a přihlásím jako administrátor a objednávku vidím v *Objednávkách* jako novou,
   v *Produktech* ubyly kusy na skladě.
5. Změním stav na *odeslaná*. Lucie to uvidí v *Moje objednávky*.

## 6. Chybové stavy

| Co se stalo | Co uvidíš | Co s tím |
|-------------|-----------|----------|
| špatný e-mail nebo heslo | „Špatný e-mail nebo heslo.“ | zkus to znovu, případně se zaregistruj |
| e-mail je při registraci obsazený | „Účet s tímto e-mailem už existuje.“ | přihlas se, nebo použij jiný e-mail |
| do košíku chceš víc kusů, než je skladem | „Produkt X je skladem jen N ks.“ | sniž množství |
| mezitím zboží vykoupil někdo jiný | při objednání „Produkt X je skladem jen N ks.“, objednávka se nevytvoří | uprav košík a objednej znovu |
| množství není číslo 0 až 99 | „Množství musí být mezi 0 a 99.“ | zadej platné množství |
| prázdný košík při objednání | „Košík je prázdný.“ | vlož něco do košíku |
| krátká adresa nebo nevybraná platba | hláška u formuláře | doplň údaje |
| objednání bez přihlášení | přesměrování na přihlášení (košík zůstane) | přihlas se |
| zákazník otevře `/admin` | stránka „Sem má přístup jen administrátor.“ | přihlas se jako administrátor |
| neexistující adresa, produkt nebo cizí objednávka | stránka „Tohle jsme nenašli.“ | vrať se na úvod |
| mazání prodaného produktu | „Produkt je v objednávkách, nejde smazat.“ | produkt skryj |
