"""Katalog: kategorie a produkty.

Všechny dotazy jsou parametrizované (otazníky místo hodnot), hodnoty od
uživatele se nikdy nevkládají přímo do textu dotazu.
"""

import sqlite3

# Řazení se nedá předat otazníkem (ORDER BY ? nefunguje). Proto má uživatel
# na výběr jen z těchto předem připravených možností a nic jiného do dotazu nepustíme.
RAZENI = {
    "nazev": "p.nazev",
    "cena": "p.cena_kc, p.nazev",
    "cena_desc": "p.cena_kc DESC, p.nazev",
}


def kategorie(spojeni):
    """Vrátí kategorie s počtem nabízených produktů (LEFT JOIN + GROUP BY)."""
    return spojeni.execute(
        """
        SELECT k.id, k.nazev, k.popis, COUNT(p.id) AS pocet_produktu
        FROM kategorie k
        LEFT JOIN produkt_kategorie pk ON pk.kategorie_id = k.id
        LEFT JOIN produkt p            ON p.id = pk.produkt_id AND p.aktivni = 1
        GROUP BY k.id, k.nazev, k.popis
        ORDER BY k.nazev
        """
    ).fetchall()


def hledej_produkty(spojeni, kategorie_id=None, hledat="", razeni="nazev"):
    """Vrátí nabízené produkty podle filtru.

    kategorie_id: jen produkty z dané kategorie (None = všechny)
    hledat:       text, který se hledá v názvu a popisu (LIKE)
    razeni:       klíč ze slovníku RAZENI
    """
    order_by = RAZENI.get(razeni, RAZENI["nazev"])
    vzor = f"%{hledat}%"
    return spojeni.execute(
        f"""
        SELECT p.*, d.nazev AS dodavatel
        FROM produkt p
        JOIN dodavatel d ON d.id = p.dodavatel_id
        WHERE p.aktivni = 1
          AND (p.nazev LIKE ? OR p.popis LIKE ?)
          AND (? IS NULL OR p.id IN (SELECT produkt_id FROM produkt_kategorie WHERE kategorie_id = ?))
        ORDER BY {order_by}
        """,
        (vzor, vzor, kategorie_id, kategorie_id),
    ).fetchall()


def najdi_produkt(spojeni, produkt_id, jen_aktivni=True):
    """Vrátí jeden produkt i s názvem dodavatele (nebo None)."""
    return spojeni.execute(
        """
        SELECT p.*, d.nazev AS dodavatel, d.mesto AS dodavatel_mesto
        FROM produkt p
        JOIN dodavatel d ON d.id = p.dodavatel_id
        WHERE p.id = ? AND (p.aktivni = 1 OR ? = 0)
        """,
        (produkt_id, int(jen_aktivni)),
    ).fetchone()


def kategorie_produktu(spojeni, produkt_id):
    """Vrátí kategorie, do kterých produkt patří (vazba M:N přes produkt_kategorie)."""
    return spojeni.execute(
        """
        SELECT k.id, k.nazev
        FROM kategorie k
        JOIN produkt_kategorie pk ON pk.kategorie_id = k.id
        WHERE pk.produkt_id = ?
        ORDER BY k.nazev
        """,
        (produkt_id,),
    ).fetchall()


def produkty_podle_id(spojeni, seznam_id):
    """Vrátí slovník {id: produkt} pro zadaná id (používá košík)."""
    seznam_id = list(seznam_id)
    if not seznam_id:
        return {}
    # Pro tři id vznikne "?, ?, ?". Počet otazníků se řídí počtem hodnot,
    # samotné hodnoty jdou do dotazu pořád jako parametry.
    otazniky = ", ".join("?" * len(seznam_id))
    radky = spojeni.execute(
        f"SELECT * FROM produkt WHERE aktivni = 1 AND id IN ({otazniky})", seznam_id
    ).fetchall()
    return {radek["id"]: radek for radek in radky}


# Administrace produktů (CRUD)
def vsechny_produkty(spojeni):
    """Vrátí všechny produkty včetně skrytých, pro tabulku v administraci."""
    return spojeni.execute(
        """
        SELECT p.*, d.nazev AS dodavatel
        FROM produkt p
        JOIN dodavatel d ON d.id = p.dodavatel_id
        ORDER BY p.aktivni DESC, p.nazev
        """
    ).fetchall()


def dodavatele(spojeni):
    """Vrátí seznam dodavatelů pro výběr ve formuláři."""
    return spojeni.execute("SELECT * FROM dodavatel ORDER BY nazev").fetchall()


def uloz_produkt(spojeni, udaje, id_kategorii, produkt_id=None):
    """Vloží nový produkt (INSERT), nebo upraví existující (UPDATE). Vrátí id produktu.

    udaje:        slovník z formuláře: nazev, popis, cena_kc, sklad, dodavatel_id
    id_kategorii: seznam id zaškrtnutých kategorií
    Neplatné údaje vyhodí ValueError s hláškou pro uživatele.
    """
    nazev = udaje.get("nazev", "").strip()
    popis = udaje.get("popis", "").strip()
    if len(nazev) < 3:
        raise ValueError("Název musí mít alespoň 3 znaky.")
    try:
        cena_kc = int(udaje.get("cena_kc", ""))
        sklad = int(udaje.get("sklad", ""))
        dodavatel_id = int(udaje.get("dodavatel_id", ""))
        id_kategorii = [int(kategorie_id) for kategorie_id in id_kategorii]
    except ValueError:
        raise ValueError("Cena, sklad, dodavatel a kategorie musí být celá čísla.") from None
    if cena_kc < 0 or sklad < 0:
        raise ValueError("Cena ani sklad nesmí být záporné.")

    try:
        with spojeni:
            if produkt_id is None:
                kurzor = spojeni.execute(
                    "INSERT INTO produkt (nazev, popis, cena_kc, sklad, dodavatel_id) VALUES (?, ?, ?, ?, ?)",
                    (nazev, popis, cena_kc, sklad, dodavatel_id),
                )
                produkt_id = kurzor.lastrowid
            else:
                spojeni.execute(
                    "UPDATE produkt SET nazev = ?, popis = ?, cena_kc = ?, sklad = ?, dodavatel_id = ? WHERE id = ?",
                    (nazev, popis, cena_kc, sklad, dodavatel_id, produkt_id),
                )
            # Kategorie: nejjednodušší je staré vazby smazat a zapsat nové.
            spojeni.execute("DELETE FROM produkt_kategorie WHERE produkt_id = ?", (produkt_id,))
            spojeni.executemany(
                "INSERT INTO produkt_kategorie (produkt_id, kategorie_id) VALUES (?, ?)",
                [(produkt_id, kategorie_id) for kategorie_id in id_kategorii],
            )
    except sqlite3.IntegrityError:
        raise ValueError("Produkt s tímto názvem už existuje, nebo je zvolen neplatný dodavatel či kategorie.") from None
    return produkt_id


def nastav_aktivni(spojeni, produkt_id, aktivni):
    """Skryje produkt z nabídky, nebo ho do ní vrátí (UPDATE)."""
    with spojeni:
        spojeni.execute("UPDATE produkt SET aktivni = ? WHERE id = ?", (int(aktivni), produkt_id))


def smaz_produkt(spojeni, produkt_id):
    """Smaže produkt (DELETE). Produkt, který už si někdo objednal, smazat nejde.

    Hlídá to cizí klíč v tabulce polozka_objednavky (ON DELETE RESTRICT).
    Jinak by ze starých objednávek zmizelo, co si zákazník koupil.
    """
    try:
        with spojeni:
            spojeni.execute("DELETE FROM produkt WHERE id = ?", (produkt_id,))
    except sqlite3.IntegrityError:
        raise ValueError("Produkt je v objednávkách, nejde smazat. Můžeš ho jen skrýt.") from None
