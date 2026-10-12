"""Spouštěcí soubor hry Houbař:  python main.py

Tady se jen přepíná mezi obrazovkami. Každá obrazovka (menu, přihlášení,
partie, konec) je ve vlastním souboru ve složce hra/.
"""
import logging
import sqlite3

import pygame

import db
from hra import nastaveni as n
from hra.konec import spust_konec
from hra.menu import spust_menu
from hra.partie import spust_partii
from hra.prihlaseni import spust_prihlaseni
from hra.vyber_obtiznosti import spust_vyber_obtiznosti


def main():
    """Vytvoří okno a v cyklu střídá obrazovky, dokud hráč nezvolí Konec."""
    logging.basicConfig(filename=n.SOUBOR_LOGU, level=logging.INFO, encoding="utf-8",
                        format="%(asctime)s %(levelname)s %(message)s")
    pygame.init()
    okno = pygame.display.set_mode((n.SIRKA, n.VYSKA))
    pygame.display.set_caption(n.NAZEV_HRY)
    hodiny = pygame.time.Clock()

    # Jedno připojení k databázi na celou dobu běhu hry.
    spojeni = db.pripoj()
    db.vytvor_databazi(spojeni)
    hrac = None                      # přihlášený hráč (záznam z DB) nebo None

    try:
        while True:
            volba = spust_menu(okno, hodiny, hrac["jmeno"] if hrac else None)
            if volba == "konec":
                break
            if volba == "odhlasit":
                hrac = None
                continue

            # Bez přihlášení se nehraje, nevěděli bychom, komu uložit skóre.
            if hrac is None:
                hrac = spust_prihlaseni(okno, hodiny, spojeni)
                if hrac is None:
                    continue
                logging.info("Přihlášen hráč %s", hrac["jmeno"])

            obtiznost = spust_vyber_obtiznosti(okno, hodiny, db.nacti_obtiznosti(spojeni))
            if obtiznost is None:
                continue
            druhy = db.nacti_druhy_hub(spojeni)

            stav, trvani_s = spust_partii(okno, hodiny, druhy, obtiznost)

            # Chyba databáze nesmí shodit hru. Zapíšeme ji do logu a hráči to řekneme.
            ulozeno = False
            nejlepsi = []
            try:
                db.uloz_partii(spojeni, hrac["id"], obtiznost["id"], stav.skore, trvani_s, stav.sebrane)
                ulozeno = True
                nejlepsi = db.zebricek(spojeni, obtiznost_id=obtiznost["id"], limit=5)
            except sqlite3.Error:
                logging.exception("Práce s databází po skončení partie selhala")
            spust_konec(okno, hodiny, stav, druhy, ulozeno, nejlepsi)
    finally:
        spojeni.close()
        pygame.quit()


if __name__ == "__main__":
    main()
