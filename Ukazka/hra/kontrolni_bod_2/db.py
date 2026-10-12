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


# Číselníky pro hru
def nacti_obtiznost(spojeni, nazev):
    """Vrátí jednu obtížnost podle názvu."""
    return spojeni.execute("SELECT * FROM obtiznost WHERE nazev = ?", (nazev,)).fetchone()


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


def zebricek(spojeni, limit=10):
    """Vrátí nejlepší partie: jméno hráče, skóre, obtížnost a datum (JOIN tří tabulek)."""
    return spojeni.execute(
        """
        SELECT h.jmeno, p.skore, o.nazev AS obtiznost, p.trvani_s, p.odehrano
        FROM partie p
        JOIN hrac h      ON h.id = p.hrac_id
        JOIN obtiznost o ON o.id = p.obtiznost_id
        ORDER BY p.skore DESC, p.odehrano
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
