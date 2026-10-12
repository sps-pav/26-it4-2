"""Uživatelské účty: registrace, přihlášení a práce s hesly."""
import hashlib
import hmac
import secrets
import sqlite3


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


def registruj(spojeni, email, jmeno, heslo):
    """Vytvoří zákaznický účet a vrátí jeho id. Při neplatných údajích vyhodí ValueError."""
    email = email.strip().lower()
    jmeno = jmeno.strip()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Zadej platný e-mail.")
    if len(jmeno) < 2:
        raise ValueError("Zadej jméno.")
    if len(heslo) < 6:
        raise ValueError("Heslo musí mít alespoň 6 znaků.")
    try:
        with spojeni:                            # with = commit, při chybě rollback
            kurzor = spojeni.execute(
                "INSERT INTO uzivatel (email, jmeno, heslo_hash) VALUES (?, ?, ?)",
                (email, jmeno, zahashuj_heslo(heslo)),
            )
    except sqlite3.IntegrityError:
        # Sloupec email je UNIQUE, takže databáze sama odmítne druhý stejný e-mail.
        raise ValueError("Účet s tímto e-mailem už existuje.") from None
    return kurzor.lastrowid


def prihlas(spojeni, email, heslo):
    """Vrátí záznam uživatele, pokud sedí e-mail i heslo, jinak None."""
    uzivatel = spojeni.execute(
        "SELECT * FROM uzivatel WHERE email = ?", (email.strip().lower(),)
    ).fetchone()
    if uzivatel is None or not over_heslo(heslo, uzivatel["heslo_hash"]):
        return None
    return uzivatel
