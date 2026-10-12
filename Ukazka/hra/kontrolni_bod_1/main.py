"""Spouštěcí soubor hry Houbař:  python main.py

Tady se jen přepíná mezi obrazovkami. Každá obrazovka (menu, přihlášení,
partie, konec) je ve vlastním souboru ve složce hra/.
"""
import pygame

from hra import nastaveni as n
from hra.menu import spust_menu, spust_pripravuje_se


def main():
    """Vytvoří okno a v cyklu střídá obrazovky, dokud hráč nezvolí Konec."""
    pygame.init()
    okno = pygame.display.set_mode((n.SIRKA, n.VYSKA))
    pygame.display.set_caption(n.NAZEV_HRY)
    hodiny = pygame.time.Clock()

    try:
        while True:
            volba = spust_menu(okno, hodiny)
            if volba == "konec":
                break
            spust_pripravuje_se(okno, hodiny)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
