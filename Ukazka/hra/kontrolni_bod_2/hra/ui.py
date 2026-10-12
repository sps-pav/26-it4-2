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


class TextovePole:
    """Pole pro psaní textu (jméno, heslo). Aktivní pole má světlý rámeček."""

    MAX_DELKA = 20

    def __init__(self, popisek, stred_x, stred_y, skryte=False, sirka=320, vyska=44):
        self.popisek = popisek
        self.text = ""
        self.skryte = skryte          # True = místo znaků se kreslí hvězdičky (heslo)
        self.aktivni = False
        self.obdelnik = pygame.Rect(0, 0, sirka, vyska)
        self.obdelnik.center = (stred_x, stred_y)

    def zpracuj(self, udalost):
        """Zpracuje kliknutí (aktivace pole) a stisk kláves (psaní, mazání)."""
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            self.aktivni = self.obdelnik.collidepoint(udalost.pos)
        elif udalost.type == pygame.KEYDOWN and self.aktivni:
            if udalost.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif udalost.unicode.isprintable() and udalost.unicode != "":
                if len(self.text) < self.MAX_DELKA:
                    self.text += udalost.unicode

    def vykresli(self, okno, font, maly_font):
        """Nakreslí popisek nad polem, rámeček a napsaný text."""
        napis(okno, maly_font, self.popisek, self.obdelnik.left, self.obdelnik.top - 22,
              n.BARVA_TLUMENA, na_stred=False)
        pygame.draw.rect(okno, (15, 30, 22), self.obdelnik, border_radius=8)
        ramecek = n.BARVA_TEXT if self.aktivni else n.BARVA_TLUMENA
        pygame.draw.rect(okno, ramecek, self.obdelnik, width=2, border_radius=8)
        zobrazeny = "*" * len(self.text) if self.skryte else self.text
        if self.aktivni:
            zobrazeny += "|"
        napis(okno, font, zobrazeny, self.obdelnik.left + 10, self.obdelnik.top + 8, na_stred=False)
