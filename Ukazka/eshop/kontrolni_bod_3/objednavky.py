"""Objednávky: vytvoření z košíku, historie, stavy a přehledy pro administraci."""

ZPUSOBY_PLATBY = {"dobirka": "Dobírka", "prevod": "Bankovní převod"}
STAV_NOVA = 1           # id z tabulky stav_objednavky (viz databaze/data.sql)
STAV_ZRUSENA = 4


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


def objednavky_uzivatele(spojeni, uzivatel_id):
    """Historie objednávek jednoho zákazníka (čte z pohledu v_objednavka)."""
    return spojeni.execute(
        "SELECT * FROM v_objednavka WHERE uzivatel_id = ? ORDER BY vytvoreno DESC, id DESC",
        (uzivatel_id,),
    ).fetchall()


def najdi_objednavku(spojeni, objednavka_id):
    """Vrátí dvojici (objednávka z pohledu, její položky), nebo (None, [])."""
    objednavka = spojeni.execute(
        "SELECT * FROM v_objednavka WHERE id = ?", (objednavka_id,)
    ).fetchone()
    if objednavka is None:
        return None, []
    polozky = spojeni.execute(
        """
        SELECT p.nazev, po.mnozstvi, po.cena_za_kus_kc,
               po.mnozstvi * po.cena_za_kus_kc AS mezisoucet
        FROM polozka_objednavky po
        JOIN produkt p ON p.id = po.produkt_id
        WHERE po.objednavka_id = ?
        ORDER BY p.nazev
        """,
        (objednavka_id,),
    ).fetchall()
    return objednavka, polozky


# Administrace
def stavy(spojeni):
    """Vrátí číselník stavů objednávky."""
    return spojeni.execute("SELECT * FROM stav_objednavky ORDER BY id").fetchall()


def vsechny_objednavky(spojeni, stav_id=None):
    """Všechny objednávky, volitelně jen v daném stavu."""
    return spojeni.execute(
        """
        SELECT * FROM v_objednavka
        WHERE (? IS NULL OR stav_id = ?)
        ORDER BY vytvoreno DESC, id DESC
        """,
        (stav_id, stav_id),
    ).fetchall()


def zmen_stav(spojeni, objednavka_id, novy_stav_id):
    """Změní stav objednávky. Při zrušení vrátí zboží na sklad (jedna transakce)."""
    with spojeni:
        objednavka = spojeni.execute(
            "SELECT stav_id FROM objednavka WHERE id = ?", (objednavka_id,)
        ).fetchone()
        if objednavka is None:
            raise ValueError("Objednávka neexistuje.")
        if objednavka["stav_id"] == STAV_ZRUSENA:
            raise ValueError("Zrušenou objednávku už nejde měnit.")
        if spojeni.execute("SELECT 1 FROM stav_objednavky WHERE id = ?", (novy_stav_id,)).fetchone() is None:
            raise ValueError("Neznámý stav.")

        if novy_stav_id == STAV_ZRUSENA:
            # UPDATE s poddotazem: každému produktu z objednávky přičte objednané množství.
            spojeni.execute(
                """
                UPDATE produkt
                SET sklad = sklad + (SELECT mnozstvi FROM polozka_objednavky
                                     WHERE objednavka_id = ? AND produkt_id = produkt.id)
                WHERE id IN (SELECT produkt_id FROM polozka_objednavky WHERE objednavka_id = ?)
                """,
                (objednavka_id, objednavka_id),
            )
        spojeni.execute(
            "UPDATE objednavka SET stav_id = ? WHERE id = ?", (novy_stav_id, objednavka_id)
        )


def trzby_podle_kategorie(spojeni):
    """Tržby a počet prodaných kusů v každé kategorii (zrušené objednávky se nepočítají).

    Produkt ve dvou kategoriích se započítá do obou, součet řádků proto může
    být vyšší než celkové tržby.
    """
    return spojeni.execute(
        """
        SELECT k.nazev,
               COALESCE(SUM(po.mnozstvi), 0)                     AS kusu,
               COALESCE(SUM(po.mnozstvi * po.cena_za_kus_kc), 0) AS trzba_kc
        FROM kategorie k
        LEFT JOIN produkt_kategorie pk  ON pk.kategorie_id = k.id
        LEFT JOIN polozka_objednavky po ON po.produkt_id = pk.produkt_id
             AND po.objednavka_id IN (SELECT id FROM objednavka WHERE stav_id <> ?)
        GROUP BY k.id, k.nazev
        ORDER BY trzba_kc DESC, k.nazev
        """,
        (STAV_ZRUSENA,),
    ).fetchall()


def nejprodavanejsi(spojeni, limit=5):
    """Nejprodávanější produkty podle počtu kusů."""
    return spojeni.execute(
        """
        SELECT p.nazev, SUM(po.mnozstvi) AS kusu, SUM(po.mnozstvi * po.cena_za_kus_kc) AS trzba_kc
        FROM polozka_objednavky po
        JOIN produkt p    ON p.id = po.produkt_id
        JOIN objednavka o ON o.id = po.objednavka_id
        WHERE o.stav_id <> ?
        GROUP BY p.id, p.nazev
        ORDER BY kusu DESC, p.nazev
        LIMIT ?
        """,
        (STAV_ZRUSENA, limit),
    ).fetchall()


def souhrn(spojeni):
    """Jedno číslo pro každou dlaždici v přehledu administrace."""
    return spojeni.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM objednavka WHERE stav_id = ?)                        AS novych,
            (SELECT COALESCE(SUM(celkem_kc), 0) FROM v_objednavka WHERE stav_id <> ?)  AS trzby_kc,
            (SELECT COUNT(*) FROM produkt WHERE aktivni = 1 AND sklad < 5)             AS dochazi,
            (SELECT COUNT(*) FROM uzivatel WHERE je_admin = 0)                         AS zakazniku
        """,
        (STAV_NOVA, STAV_ZRUSENA),
    ).fetchone()
