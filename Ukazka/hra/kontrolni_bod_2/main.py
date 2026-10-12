"""Spouštěcí soubor hry Houbař:  python main.py

Tady se jen přepíná mezi obrazovkami. Každá obrazovka (menu, přihlášení,
partie, konec) je ve vlastním souboru ve složce hra/.
"""
import pygame

import db
from hra import nastaveni as n
from hra.konec import spust_konec
from hra.menu import spust_menu
from hra.partie import spust_partii
from hra.prihlaseni import spust_prihlaseni


def main():
    """Vytvoří okno a v cyklu střídá obrazovky, dokud hráč nezvolí Konec."""
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

            # Bez přihlášení se nehraje, nevěděli bychom, komu uložit skóre.
            if hrac is None:
                hrac = spust_prihlaseni(okno, hodiny, spojeni)
                if hrac is None:
                    continue

            # Zatím se hraje jen na jednu obtížnost, výběr přibude později.
            obtiznost = db.nacti_obtiznost(spojeni, "Normální")
            druhy = db.nacti_druhy_hub(spojeni)

            stav, trvani_s = spust_partii(okno, hodiny, druhy, obtiznost)

            db.uloz_partii(spojeni, hrac["id"], obtiznost["id"], stav.skore, trvani_s, stav.sebrane)
            spust_konec(okno, hodiny, stav, druhy, ulozeno=True)
    finally:
        spojeni.close()
        pygame.quit()


if __name__ == "__main__":
    main()
