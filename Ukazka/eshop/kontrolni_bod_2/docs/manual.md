# Uživatelský manuál: Zelený kout

> Rozpracovaná verze (2. kontrolní bod). Chybí historie objednávek, administrace a chybové stavy.

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
7. Obchod potvrdí číslo objednávky a košík se vyprázdní.
