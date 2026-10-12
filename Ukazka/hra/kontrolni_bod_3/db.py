"""Práce s databází: jediné místo v projektu, kde se píše SQL.

Tento soubor používá hra (main.py) i web (web.py). Obě části tak čtou
a zapisují stejná data stejným způsobem.

Všechny dotazy jsou parametrizované (otazníky místo hodnot). Hodnoty od
uživatele se nikdy nevkládají přímo do textu dotazu. Tím se bráníme
útoku SQL injection.
"""
import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path

SLOZKA = Path(__file__).resolve().parent
DB_SOUBOR = SLOZKA / "houbar.db"            # vznikne při prvním spuštění, do gitu nepatří
SLOZKA_SQL = SLOZKA / "databaze"


# Připojení a vytvoření databáze
def pripoj(cesta=None):
    """Otevře připojení k databázi. Bez parametru použije soubor houbar.db.

    V testech se předává ":memory:", databáze pak žije jen v paměti.
    """
    spojeni = sqlite3.connect(cesta or DB_SOUBOR)
    spojeni.row_factory = sqlite3.Row            # ke sloupcům jde přistupovat jménem
    spojeni.execute("PRAGMA foreign_keys = ON")  # SQLite jinak cizí klíče nehlídá
    return spojeni


def vytvor_databazi(spojeni, s_daty=True):
    """Pokud tabulky ještě neexistují, vytvoří je ze schema.sql (a naplní z data.sql)."""
    existuje = spojeni.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'hrac'"
    ).fetchone()
    if existuje:
        return
    spojeni.executescript((SLOZKA_SQL / "schema.sql").read_text(encoding="utf-8"))
    if s_daty:
        spojeni.executescript((SLOZKA_SQL / "data.sql").read_text(encoding="utf-8"))
    spojeni.commit()


# Hesla
def zahashuj_heslo(heslo, sul=None):
    """Vrátí text "sůl$otisk". Samotné heslo se do databáze nikdy neukládá."""
    if sul is None:
        sul = secrets.token_hex(8)
    otisk = hashlib.pbkdf2_hmac("sha256", heslo.encode("utf-8"), sul.encode("ascii"), 100_000)
    return f"{sul}${otisk.hex()}"


def over_heslo(heslo, ulozeny_hash):
    """Zjistí, jestli zadané heslo odpovídá uloženému otisku."""
    sul = ulozeny_hash.split("$")[0]
    return hmac.compare_digest(zahashuj_heslo(heslo, sul), ulozeny_hash)


# Hráči
def registruj_hrace(spojeni, jmeno, heslo):
    """Vytvoří účet a vrátí jeho id. Při neplatných údajích vyhodí ValueError."""
    jmeno = jmeno.strip()
    if not 3 <= len(jmeno) <= 20:
        raise ValueError("Jméno musí mít 3 až 20 znaků.")
    if len(heslo) < 6:
        raise ValueError("Heslo musí mít alespoň 6 znaků.")
    try:
        with spojeni:                            # with = commit, při chybě rollback
            kurzor = spojeni.execute(
                "INSERT INTO hrac (jmeno, heslo_hash) VALUES (?, ?)",
                (jmeno, zahashuj_heslo(heslo)),
            )
    except sqlite3.IntegrityError:
        # Sloupec jmeno je UNIQUE, takže databáze sama odmítne druhé stejné jméno.
        raise ValueError("Toto jméno už někdo používá.") from None
    return kurzor.lastrowid


def prihlas_hrace(spojeni, jmeno, heslo):
    """Vrátí záznam hráče, pokud sedí jméno i heslo, jinak None."""
    hrac = spojeni.execute("SELECT * FROM hrac WHERE jmeno = ?", (jmeno.strip(),)).fetchone()
    if hrac is None or not over_heslo(heslo, hrac["heslo_hash"]):
        return None
    return hrac


def najdi_hrace(spojeni, hrac_id):
    """Vrátí záznam hráče podle id (nebo None)."""
    return spojeni.execute("SELECT * FROM hrac WHERE id = ?", (hrac_id,)).fetchone()


def zmen_heslo(spojeni, hrac_id, stare_heslo, nove_heslo):
    """Změní heslo (UPDATE). Staré heslo musí sedět, jinak vyhodí ValueError."""
    hrac = najdi_hrace(spojeni, hrac_id)
    if hrac is None or not over_heslo(stare_heslo, hrac["heslo_hash"]):
        raise ValueError("Původní heslo není správně.")
    if len(nove_heslo) < 6:
        raise ValueError("Nové heslo musí mít alespoň 6 znaků.")
    with spojeni:
        spojeni.execute(
            "UPDATE hrac SET heslo_hash = ? WHERE id = ?",
            (zahashuj_heslo(nove_heslo), hrac_id),
        )


def smaz_hrace(spojeni, hrac_id):
    """Smaže účet (DELETE). Partie hráče zmizí s ním díky ON DELETE CASCADE."""
    with spojeni:
        spojeni.execute("DELETE FROM hrac WHERE id = ?", (hrac_id,))


# Číselníky pro hru
def nacti_obtiznosti(spojeni):
    """Vrátí všechny obtížnosti od nejlehčí (pomalejší pád = lehčí)."""
    return spojeni.execute("SELECT * FROM obtiznost ORDER BY rychlost_padu").fetchall()


def nacti_druhy_hub(spojeni):
    """Vrátí všechny druhy hub seřazené podle bodů."""
    return spojeni.execute("SELECT * FROM druh_houby ORDER BY body DESC, nazev").fetchall()


# Partie
def uloz_partii(spojeni, hrac_id, obtiznost_id, skore, trvani_s, sebrane):
    """Uloží odehranou partii a k ní počty sebraných hub. Vrátí id partie.

    sebrane: slovník {id druhu houby: počet kusů}
    Oba zápisy jsou v jedné transakci: buď se uloží všechno, nebo nic.
    """
    with spojeni:
        kurzor = spojeni.execute(
            "INSERT INTO partie (hrac_id, obtiznost_id, skore, trvani_s) VALUES (?, ?, ?, ?)",
            (hrac_id, obtiznost_id, skore, trvani_s),
        )
        partie_id = kurzor.lastrowid
        spojeni.executemany(
            "INSERT INTO partie_houba (partie_id, druh_houby_id, pocet) VALUES (?, ?, ?)",
            [(partie_id, druh_id, pocet) for druh_id, pocet in sebrane.items()],
        )
    return partie_id


def zebricek(spojeni, obtiznost_id=None, hledat="", limit=10):
    """Vrátí nejlepší partie (JOIN tří tabulek) s volitelným filtrem.

    obtiznost_id: jen partie na dané obtížnosti (None = všechny)
    hledat:       část jména hráče (vyhledávání přes LIKE)
    """
    return spojeni.execute(
        """
        SELECT h.jmeno, p.skore, o.nazev AS obtiznost, p.trvani_s, p.odehrano
        FROM partie p
        JOIN hrac h      ON h.id = p.hrac_id
        JOIN obtiznost o ON o.id = p.obtiznost_id
        WHERE (? IS NULL OR p.obtiznost_id = ?)
          AND h.jmeno LIKE ?
        ORDER BY p.skore DESC, p.odehrano
        LIMIT ?
        """,
        (obtiznost_id, obtiznost_id, f"%{hledat}%", limit),
    ).fetchall()


def souhrn_hracu(spojeni):
    """Pro každého hráče spočítá počet partií, nejlepší a průměrné skóre (GROUP BY)."""
    return spojeni.execute(
        """
        SELECT h.jmeno,
               COUNT(p.id)                     AS pocet_partii,
               COALESCE(MAX(p.skore), 0)       AS nejlepsi_skore,
               COALESCE(ROUND(AVG(p.skore)), 0) AS prumerne_skore
        FROM hrac h
        LEFT JOIN partie p ON p.hrac_id = h.id
        GROUP BY h.id, h.jmeno
        ORDER BY nejlepsi_skore DESC, h.jmeno
        """
    ).fetchall()


def partie_hrace(spojeni, hrac_id):
    """Vrátí všechny partie jednoho hráče od nejnovější."""
    return spojeni.execute(
        """
        SELECT p.id, p.skore, p.trvani_s, p.odehrano, o.nazev AS obtiznost
        FROM partie p
        JOIN obtiznost o ON o.id = p.obtiznost_id
        WHERE p.hrac_id = ?
        ORDER BY p.odehrano DESC, p.id DESC
        """,
        (hrac_id,),
    ).fetchall()


def statistika_hub(spojeni, hrac_id):
    """Kolik kusů kterého druhu houby hráč celkem sebral (vazba M:N přes partie_houba)."""
    return spojeni.execute(
        """
        SELECT d.nazev, d.jedla, SUM(ph.pocet) AS celkem
        FROM partie_houba ph
        JOIN partie p     ON p.id = ph.partie_id
        JOIN druh_houby d ON d.id = ph.druh_houby_id
        WHERE p.hrac_id = ?
        GROUP BY d.id, d.nazev, d.jedla
        ORDER BY celkem DESC
        """,
        (hrac_id,),
    ).fetchall()


def smaz_partii(spojeni, partie_id, hrac_id):
    """Smaže partii, ale jen pokud patří danému hráči. Vrátí True, když se něco smazalo."""
    with spojeni:
        kurzor = spojeni.execute(
            "DELETE FROM partie WHERE id = ? AND hrac_id = ?", (partie_id, hrac_id)
        )
    return kurzor.rowcount == 1
