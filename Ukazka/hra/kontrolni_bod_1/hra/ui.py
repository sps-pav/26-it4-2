"""Jednoduché prvky uživatelského rozhraní: nápis, tlačítko a textové pole.

Pygame nemá hotová tlačítka ani formuláře, proto si je tu kreslíme sami.
Tyto prvky používají všechny obrazovky (menu, přihlášení, konec hry).
"""
import sys

import pygame

from hra import nastaveni as n


def ukonci_aplikaci():
    """Korektně zavře Pygame a ukončí program (křížek v okně)."""
    pygame.quit()
    sys.exit()


def napis(okno, font, text, x, y, barva=n.BARVA_TEXT, na_stred=True):
    """Vykreslí text. Když je na_stred=True, bere se x, y jako střed textu."""
    obrazek = font.render(text, True, barva)
    obdelnik = obrazek.get_rect()
    if na_stred:
        obdelnik.center = (x, y)
    else:
        obdelnik.topleft = (x, y)
    okno.blit(obrazek, obdelnik)
    return obdelnik


class Tlacitko:
    """Obdélníkové tlačítko s textem, na které jde kliknout myší."""

    def __init__(self, text, stred_x, stred_y, sirka=260, vyska=52):
        self.text = text
        self.obdelnik = pygame.Rect(0, 0, sirka, vyska)
        self.obdelnik.center = (stred_x, stred_y)

    def vykresli(self, okno, font):
        """Nakreslí tlačítko; pokud je nad ním myš, zvýrazní ho."""
        nad_tlacitkem = self.obdelnik.collidepoint(pygame.mouse.get_pos())
        barva = n.BARVA_TLACITKO_AKTIVNI if nad_tlacitkem else n.BARVA_TLACITKO
        pygame.draw.rect(okno, barva, self.obdelnik, border_radius=10)
        pygame.draw.rect(okno, n.BARVA_TEXT, self.obdelnik, width=2, border_radius=10)
        napis(okno, font, self.text, *self.obdelnik.center)

    def je_kliknuto(self, udalost):
        """Vrátí True, pokud je událost kliknutí levým tlačítkem na toto tlačítko."""
        return (
            udalost.type == pygame.MOUSEBUTTONDOWN
            and udalost.button == 1
            and self.obdelnik.collidepoint(udalost.pos)
        )
