# Hardwario – e-shop s hardwarem a počítači

Hardwario je e-shop, kde si zákazník koupí počítačové komponenty (procesory, základní desky, paměti, grafické karty, disky, zdroje, skříně, chlazení) i hotové sestavy PC. Hlavní výhodou oproti běžnému e-shopu je konfigurátor sestavy, který při výběru dílů průběžně hlídá jejich vzájemnou kompatibilitu, takže zákazník nekoupí desku, na kterou se jeho procesor nevejde.

## Hlavní myšlenka

Sestavit si PC je pro začátečníky riskantní: socket procesoru, typ paměti, rozměry skříně nebo příkon zdroje – stačí jedna chyba a součástky nejdou použít. Hardwario tento problém řeší přímo v e-shopu:

1. zákazník prochází katalog jako v jakémkoli jiném obchodě,
2. nebo otevře konfigurátor, vybírá díl po dílu a hned vidí, co s čím nejde dohromady,
3. hotovou sestavu jedním kliknutím vloží do košíku a objedná.

## Funkce

### Zákazník

- katalog produktů s kategoriemi, filtrováním (výrobce, cena, parametry), řazením a vyhledáváním
- detail produktu s technickými parametry a dostupností skladem
- registrace, přihlášení, správa profilu a doručovacích adres
- košík a objednávka (výběr dopravy a platby, historie objednávek)
- konfigurátor PC
- hotové sestavy PC k okamžitému nákupu

### Administrace

- správa produktů, kategorií, výrobců a skladových zásob
- správa objednávek 
- správa uživatelů a rolí
- základní přehledy (např. tržby, nejprodávanější zboží, zboží s nízkou zásobou)

## Technologie

| Vrstva             | Použito                       |
|--------------------|-------------------------------|
| Backend            | Python 3 + Flask              |
| Databáze           | SQLite                        |
| Šablony a frontend | HTML, CSS, Jinja2, JavaScript |
| Testy              | pytest                        |
| Verzování          | Git                           |
