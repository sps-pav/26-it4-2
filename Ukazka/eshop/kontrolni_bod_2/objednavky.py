"""Objednávky: vytvoření z košíku, historie, stavy a přehledy pro administraci."""

ZPUSOBY_PLATBY = {"dobirka": "Dobírka", "prevod": "Bankovní převod"}


def vytvor_objednavku(spojeni, uzivatel_id, kosik, adresa, zpusob_platby):
    """Vytvoří objednávku z košíku a vrátí její id.

    Všechno proběhne v JEDNÉ TRANSAKCI:
        1) zápis objednávky
        2) pro každou položku: odečtení ze skladu + zápis položky s aktuální cenou
    Když cokoli selže (zboží došlo, produkt zmizel z nabídky), vyhodí se ValueError
    a databáze se vrátí do stavu před objednávkou (ROLLBACK).
    """
    adresa = adresa.strip()
    if not kosik:
        raise ValueError("Košík je prázdný.")
    if len(adresa) < 10:
        raise ValueError("Zadej celou doručovací adresu.")
    if zpusob_platby not in ZPUSOBY_PLATBY:
        raise ValueError("Vyber způsob platby.")

    with spojeni:                       # začátek transakce; výjimka uvnitř = ROLLBACK
        kurzor = spojeni.execute(
            "INSERT INTO objednavka (uzivatel_id, adresa, zpusob_platby) VALUES (?, ?, ?)",
            (uzivatel_id, adresa, zpusob_platby),
        )
        objednavka_id = kurzor.lastrowid

        for klic, mnozstvi in kosik.items():
            produkt = spojeni.execute(
                "SELECT id, nazev, cena_kc, sklad FROM produkt WHERE id = ? AND aktivni = 1",
                (int(klic),),
            ).fetchone()
            if produkt is None:
                raise ValueError("Některý produkt z košíku už není v nabídce.")

            # Sklad odečteme jen tehdy, když je zboží dost (podmínka sklad >= ?).
            # Podle počtu změněných řádků poznáme, jestli se to povedlo.
            zmena = spojeni.execute(
                "UPDATE produkt SET sklad = sklad - ? WHERE id = ? AND sklad >= ?",
                (mnozstvi, produkt["id"], mnozstvi),
            )
            if zmena.rowcount == 0:
                raise ValueError(f"Produkt {produkt['nazev']} je skladem jen {produkt['sklad']} ks.")

            # Cenu kopírujeme do položky, aby pozdější zdražení starou objednávku nezměnilo.
            spojeni.execute(
                """
                INSERT INTO polozka_objednavky (objednavka_id, produkt_id, mnozstvi, cena_za_kus_kc)
                VALUES (?, ?, ?, ?)
                """,
                (objednavka_id, produkt["id"], mnozstvi, produkt["cena_kc"]),
            )
    return objednavka_id
