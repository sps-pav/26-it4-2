"""Katalog: kategorie a produkty.

Všechny dotazy jsou parametrizované (otazníky místo hodnot), hodnoty od
uživatele se nikdy nevkládají přímo do textu dotazu.
"""

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
