"""Herní objekty, které se kreslí na obrazovku: košík hráče a padající houba."""
import pygame

from hra import nastaveni as n


def hex_na_rgb(barva):
    """Převede barvu z databáze ("#a0522d") na trojici čísel pro Pygame."""
    barva = barva.lstrip("#")
    return tuple(int(barva[i:i + 2], 16) for i in (0, 2, 4))


class Kosik:
    """Košík, kterým hráč pohybuje doleva a doprava po spodní hraně okna."""

    def __init__(self):
        self.obdelnik = pygame.Rect(0, 0, n.KOSIK_SIRKA, n.KOSIK_VYSKA)
        self.obdelnik.midbottom = (n.SIRKA // 2, n.VYSKA - n.VYSKA_TRAVY)

    def pohni(self, smer):
        """Posune košík: smer = -1 doleva, 1 doprava, 0 stojí. Nevyjede z okna."""
        self.obdelnik.x += smer * n.KOSIK_RYCHLOST
        self.obdelnik.clamp_ip(pygame.Rect(0, 0, n.SIRKA, n.VYSKA))

    def vykresli(self, okno):
        """Nakreslí košík jako hnědý obdélník se světlým okrajem."""
        pygame.draw.rect(okno, n.BARVA_KOSIK, self.obdelnik, border_radius=6)
        pygame.draw.rect(okno, n.BARVA_TEXT, self.obdelnik, width=2, border_radius=6)


class Houba:
    """Jedna padající houba. Druh (body, barva, jedlá/jedovatá) je z databáze."""

    def __init__(self, druh, x, rychlost):
        self.druh = druh
        self.rychlost = rychlost
        self.y = float(-n.HOUBA_VELIKOST)          # přesná poloha (desetinné číslo)
        self.obdelnik = pygame.Rect(x, int(self.y), n.HOUBA_VELIKOST, n.HOUBA_VELIKOST)
        self.barva = hex_na_rgb(druh["barva"])

    def aktualizuj(self):
        """Posune houbu o kus dolů."""
        self.y += self.rychlost
        self.obdelnik.y = int(self.y)

    def je_na_zemi(self):
        """True, pokud houba dopadla do trávy a hráč ji nechytil."""
        return self.obdelnik.bottom >= n.VYSKA - n.VYSKA_TRAVY + n.HOUBA_VELIKOST // 2

    def vykresli(self, okno):
        """Nakreslí houbu: bílá noha a barevný klobouk; jedovatá má tečky."""
        o = self.obdelnik
        noha = pygame.Rect(0, 0, o.width // 3, o.height // 2)
        noha.midbottom = o.midbottom
        pygame.draw.rect(okno, (235, 225, 200), noha, border_radius=4)
        klobouk = pygame.Rect(o.left, o.top, o.width, o.height * 2 // 3)
        pygame.draw.ellipse(okno, self.barva, klobouk)
        if not self.druh["jedla"]:
            for posun in (-9, 0, 9):
                pygame.draw.circle(okno, (255, 255, 255), (o.centerx + posun, klobouk.centery - 2), 3)
