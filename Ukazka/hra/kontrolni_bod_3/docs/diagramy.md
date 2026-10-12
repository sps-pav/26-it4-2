# Vývojové diagramy: Houbař

Tři klíčové mechaniky. Diagramy jsou v jazyce Mermaid, GitHub/GitLab je vykreslí.
Zjednodušené verze jsou i na webu na stránce *O projektu*.

## 1. Herní smyčka (`hra/partie.py`)

```mermaid
flowchart TD
    A([Start partie]) --> B[Přečti události]
    B --> C{Esc?}
    C -- ano --> K
    C -- ne --> D{Pauza?}
    D -- ano --> V[Vykresli scénu + nápis PAUZA] --> B
    D -- ne --> E[Posuň košík podle kláves]
    E --> F{Uplynul interval?}
    F -- ano --> G[Vytvoř novou houbu] --> H
    F -- ne --> H[Posuň houby, vyhodnoť kolize]
    H --> I{Došly životy<br>nebo čas?}
    I -- ne --> J[Vykresli scénu] --> B
    I -- ano --> K([Vrať stav a délku partie])
```

## 2. Chycení houby (`StavHry.seber` v `hra/logika.py`)

```mermaid
flowchart TD
    A([Houba se dotkla košíku]) --> B[sebrane druh += 1]
    B --> C{Je houba jedlá?}
    C -- ano --> D[skóre += body × násobič obtížnosti]
    C -- ne --> E[životy −= 1]
    D --> F([Odstraň houbu ze scény])
    E --> F
```

## 3. Uložení partie (`db.uloz_partii`)

```mermaid
flowchart TD
    A([Konec partie]) --> B[Začni transakci]
    B --> C[INSERT do partie]
    C --> D[Zjisti id nové partie]
    D --> E[INSERT do partie_houba<br>pro každý sebraný druh]
    E --> F{Chyba?}
    F -- ne --> G[COMMIT] --> H([Zobraz výsledek a žebříček])
    F -- ano --> I[ROLLBACK, v DB nezůstane nic]
    I --> J[Zapiš chybu do houbar.log] --> K([Zobraz „nepodařilo se uložit“])
```
