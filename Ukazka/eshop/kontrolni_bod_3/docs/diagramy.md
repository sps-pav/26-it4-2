# Vývojové diagramy: Zelený kout

Tři klíčové mechaniky. Diagramy jsou v jazyce Mermaid, GitHub/GitLab je vykreslí.
Zjednodušené verze jsou i na webu na stránce *O projektu*.

## 1. Vytvoření objednávky (`objednavky.vytvor_objednavku`)

```mermaid
flowchart TD
    A([POST /objednat]) --> B{Košík, adresa<br>a platba v pořádku?}
    B -- ne --> X([Hláška, nic se neuloží])
    B -- ano --> C[Začni transakci]
    C --> D[INSERT objednavka]
    D --> E{Další položka<br>v košíku?}
    E -- ne --> K[COMMIT]
    K --> L([Vyprázdni košík,<br>zobraz detail objednávky])
    E -- ano --> F{Produkt je<br>v nabídce?}
    F -- ne --> R
    F -- ano --> G[UPDATE produkt SET sklad = sklad − n<br>WHERE sklad >= n]
    G --> H{Změnil se řádek?}
    H -- ne, zboží nestačí --> R[ROLLBACK]
    R --> X
    H -- ano --> I[INSERT polozka_objednavky<br>s aktuální cenou]
    I --> E
```

## 2. Přidání do košíku (`app.pridat_do_kosiku` + `kosik.pridej`)

```mermaid
flowchart TD
    A([POST /kosik/pridat]) --> B{Produkt existuje<br>a je v nabídce?}
    B -- ne --> N([Stránka 404])
    B -- ano --> C{Množství je<br>celé číslo 0 až 99?}
    C -- ne --> H([Hláška: neplatné množství])
    C -- ano --> D[nové množství = v košíku + přidávané]
    D --> E{Nové množství<br>≤ sklad?}
    E -- ne --> S([Hláška: skladem jen N ks])
    E -- ano --> F[Ulož košík do session]
    F --> G([Přesměruj na košík])
```

## 3. Změna stavu objednávky (`objednavky.zmen_stav`)

```mermaid
flowchart TD
    A([POST /admin/objednavka/id/stav]) --> B{Přihlášený<br>administrátor?}
    B -- ne --> Z([403 Zakázáno])
    B -- ano --> C[Začni transakci]
    C --> D{Objednávka existuje<br>a není zrušená?}
    D -- ne --> X([ROLLBACK + hláška])
    D -- ano --> E{Nový stav<br>= zrušená?}
    E -- ano --> F[UPDATE produkt:<br>vrať množství na sklad]
    F --> G
    E -- ne --> G[UPDATE objednavka SET stav_id]
    G --> H[COMMIT]
    H --> I([Zpět na seznam objednávek])
```
