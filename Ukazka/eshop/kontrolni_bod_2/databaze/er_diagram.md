# ER diagram: Zelený kout

Diagram je zapsaný v jazyce [Mermaid](https://mermaid.js.org/), GitHub i GitLab ho
vykreslí přímo při zobrazení tohoto souboru. Stejně dobře ho můžeš nakreslit
v draw.io a uložit jako `er_diagram.png`.

```mermaid
erDiagram
    UZIVATEL ||--o{ OBJEDNAVKA : "vytvořil"
    STAV_OBJEDNAVKY ||--o{ OBJEDNAVKA : "je ve stavu"
    OBJEDNAVKA ||--|{ POLOZKA_OBJEDNAVKY : "obsahuje"
    PRODUKT ||--o{ POLOZKA_OBJEDNAVKY : "byl objednán v"
    DODAVATEL ||--o{ PRODUKT : "dodává"
    PRODUKT ||--o{ PRODUKT_KATEGORIE : "patří do"
    KATEGORIE ||--o{ PRODUKT_KATEGORIE : "obsahuje"

    UZIVATEL {
        int id PK
        text email UK
        text jmeno
        text heslo_hash
        int je_admin
        text registrovan
    }
    DODAVATEL {
        int id PK
        text nazev UK
        text mesto
    }
    KATEGORIE {
        int id PK
        text nazev UK
        text popis
    }
    PRODUKT {
        int id PK
        text nazev UK
        text popis
        int cena_kc
        int sklad
        int aktivni
        int dodavatel_id FK
    }
    PRODUKT_KATEGORIE {
        int produkt_id PK,FK
        int kategorie_id PK,FK
    }
    STAV_OBJEDNAVKY {
        int id PK
        text nazev UK
    }
    OBJEDNAVKA {
        int id PK
        int uzivatel_id FK
        int stav_id FK
        text adresa
        text zpusob_platby
        text vytvoreno
    }
    POLOZKA_OBJEDNAVKY {
        int objednavka_id PK,FK
        int produkt_id PK,FK
        int mnozstvi
        int cena_za_kus_kc
    }
```

## Vztahy

| Vztah | Typ | Význam | Při mazání |
|-------|-----|--------|-----------|
| dodavatel a produkt | 1:N | dodavatel dodává mnoho produktů | RESTRICT, dodavatele s produkty smazat nejde |
| uzivatel a objednavka | 1:N | zákazník má mnoho objednávek | RESTRICT, zákazníka s objednávkami smazat nejde |
| stav_objednavky a objednavka | 1:N | v jednom stavu je mnoho objednávek | RESTRICT |
| produkt a kategorie | **M:N** | produkt je ve více kategoriích; vazební tabulka `produkt_kategorie` | CASCADE, zařazení zmizí s produktem i s kategorií |
| objednavka a produkt | **M:N** | objednávka má více produktů; vazební tabulka `polozka_objednavky` s atributy `mnozstvi` a `cena_za_kus_kc` | CASCADE ze strany objednávky, RESTRICT ze strany produktu |

Další objekty: pohled `v_objednavka` (objednávka + zákazník + stav + spočítaná cena)
a indexy `idx_objednavka_uzivatel`, `idx_polozka_produkt`.
