"""Připojení k databázi a její vytvoření ze SQL skriptů.

Samotné dotazy jsou rozdělené podle oblastí:
    ucty.py:        registrace a přihlášení
    katalog.py:     kategorie a produkty
    objednavky.py:  vytvoření objednávky a práce s objednávkami
"""
import sqlite3
from pathlib import Path

SLOZKA = Path(__file__).resolve().parent
DB_SOUBOR = SLOZKA / "eshop.db"             # vznikne při prvním spuštění, do gitu nepatří
SLOZKA_SQL = SLOZKA / "databaze"


def pripoj(cesta=None):
    """Otevře připojení k databázi. Bez parametru použije soubor eshop.db.

    V testech se předává ":memory:", databáze pak žije jen v paměti.
    """
    spojeni = sqlite3.connect(cesta or DB_SOUBOR)
    spojeni.row_factory = sqlite3.Row            # ke sloupcům jde přistupovat jménem
    spojeni.execute("PRAGMA foreign_keys = ON")  # SQLite jinak cizí klíče nehlídá
    return spojeni


def vytvor_databazi(spojeni):
    """Pokud tabulky ještě neexistují, vytvoří je ze schema.sql a naplní z data.sql."""
    existuje = spojeni.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'produkt'"
    ).fetchone()
    if existuje:
        return
    spojeni.executescript((SLOZKA_SQL / "schema.sql").read_text(encoding="utf-8"))
    spojeni.executescript((SLOZKA_SQL / "data.sql").read_text(encoding="utf-8"))
    spojeni.commit()
