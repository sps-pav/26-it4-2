# ER diagram – KopačkyShop

Diagram můžeš otevřít v editoru, který podporuje Mermaid (např. GitHub).

```mermaid
erDiagram
 role ||--o{ uzivatele : ma
 uzivatele ||--o{ objednavky : vytvari
 kategorie ||--o{ produkty : obsahuje
 produkty ||--o{ produkt_velikost : nabizi
 velikosti ||--o{ produkt_velikost : patri
 objednavky ||--o{ polozky_objednavky : obsahuje
 produkty ||--o{ polozky_objednavky : prodava_se
 velikosti ||--o{ polozky_objednavky : ma
 role { int id PK string nazev }
 uzivatele { int id PK string email string heslo int role_id FK }
 kategorie { int id PK string nazev }
 produkty { int id PK string nazev int cena int kategorie_id FK }
 velikosti { int id PK int cislo }
 produkt_velikost { int produkt_id PK int velikost_id PK int sklad }
 objednavky { int id PK int uzivatel_id FK string stav }
 polozky_objednavky { int id PK int objednavka_id FK int produkt_id FK int velikost_id FK int mnozstvi int cena_za_kus }
```

**M:N číslo 1:** produkt ↔ velikost přes `produkt_velikost` (navíc sklad).

**M:N číslo 2:** objednávka ↔ produkt přes `polozky_objednavky` (navíc množství a původní cena).
