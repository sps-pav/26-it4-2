# Dokumentace projektu

## Účel
KopačkyShop je školní webový e-shop na prodej fotbalových kopaček (varianta B, bez hry).

## Technologie
HTML a CSS = vzhled, Python Flask = backend, SQLite = databáze, pytest = testování.

## Připojení a spuštění
Podle `README.md`. Databáze se vytvoří při prvním spuštění. Nejsou potřeba placené služby.

## Struktura
`app.py` = hlavní logika, `templates` = HTML, `static` = CSS, `databaze` = SQL, `tests` = testy, `docs` = popisy.

## Bezpečnost
Hesla se ukládají jako hash, SQL používá parametry. Admin se kontroluje na serveru. Platba je pouze simulovaná. Pro veřejné nasazení by bylo nutné přidat ochranu CSRF, bezpečný produkční klíč a další zabezpečení.

## Databáze, normalizace (BCNF)
Každá tabulka má klíč, který určuje ostatní údaje: `role(id)`, `uzivatele(id)` (email je navíc unikátní), `kategorie(id)`, `produkty(id)`, `velikosti(id)` (unikátní je také číslo), `produkt_velikost(produkt_id, velikost_id)`, `objednavky(id)` a `polozky_objednavky(id)`. Žádný další neklíčový údaj neurčuje jiný neklíčový údaj. Cena při nákupu je samostatně uložená v položce, protože se v čase může lišit od aktuální ceny produktu.

## Vazby a mazání
RESTRICT chrání historické produkty, uživatele a velikosti před smazáním. CASCADE pro položky objednávky znamená, že kdyby se smyla objednávka, zmizí i její položky. Aplikace však běžně objednávky nemaže.

## VIEW a index
`prehled_objednavek` počítá sumu z cen uložených při nákupu a používá se ve webu. `idx_produkty_znacka` pomáhá hledání produktů podle značky.

## Omezení
Určeno pro lokální školní prezentaci, bez skutečných plateb, dopravy a produkční bezpečnosti.
