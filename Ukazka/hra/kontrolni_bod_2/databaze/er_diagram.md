# ER diagram: Houbař

Diagram je zapsaný v jazyce [Mermaid](https://mermaid.js.org/), GitHub i GitLab ho
vykreslí přímo při zobrazení tohoto souboru. Stejně dobře ho můžeš nakreslit
v draw.io a uložit jako `er_diagram.png`.

```mermaid
erDiagram
    HRAC ||--o{ PARTIE : "odehrál"
    OBTIZNOST ||--o{ PARTIE : "hrálo se na"
    PARTIE ||--o{ PARTIE_HOUBA : "obsahuje"
    DRUH_HOUBY ||--o{ PARTIE_HOUBA : "byl sebrán v"

    HRAC {
        int id PK
        text jmeno UK
        text heslo_hash
        text registrovan
    }
    OBTIZNOST {
        int id PK
        text nazev UK
        real rychlost_padu
        int interval_ms
        int pocet_zivotu
        int nasobic_bodu
    }
    DRUH_HOUBY {
        int id PK
        text nazev UK
        int body
        int jedla
        text barva
        int cetnost
    }
    PARTIE {
        int id PK
        int hrac_id FK
        int obtiznost_id FK
        int skore
        int trvani_s
        text odehrano
    }
    PARTIE_HOUBA {
        int partie_id PK,FK
        int druh_houby_id PK,FK
        int pocet
    }
```

## Vztahy

| Vztah | Typ | Význam |
|-------|-----|--------|
| hrac a partie | 1:N | jeden hráč odehraje mnoho partií, partie patří právě jednomu hráči |
| obtiznost a partie | 1:N | na jednu obtížnost se hraje mnoho partií |
| partie a druh_houby | **M:N** | v partii se sebere víc druhů hub, druh se objeví v mnoha partiích; řeší vazební tabulka `partie_houba` s atributem `pocet` |
