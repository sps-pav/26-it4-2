"""Obrazovka pro výběr obtížnosti.

Obtížnosti nejsou napsané v kódu, načítají se z tabulky `obtiznost`.
Když do databáze přidáš další řádek, objeví se tu další tlačítko.
"""
import pygame

from hra import nastaveni as n
from hra.ui import Tlacitko, napis, ukonci_aplikaci


def spust_vyber_obtiznosti(okno, hodiny, obtiznosti):
    """Zobrazí tlačítko pro každou obtížnost a vrátí vybraný záznam (nebo None = zpět)."""
    velky_font = pygame.font.Font(None, 56)
    font = pygame.font.Font(None, 34)
    maly_font = pygame.font.Font(None, 24)

    stred = n.SIRKA // 2
    # Dvojice (tlačítko, záznam z DB). Tlačítka jsou pod sebou po 70 pixelech.
    volby = [
        (Tlacitko(obtiznost["nazev"], stred, 220 + i * 70), obtiznost)
        for i, obtiznost in enumerate(obtiznosti)
    ]

    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                ukonci_aplikaci()
            if udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_ESCAPE:
                return None
            for tlacitko, obtiznost in volby:
                if tlacitko.je_kliknuto(udalost):
                    return obtiznost

        okno.fill(n.BARVA_POZADI)
        napis(okno, velky_font, "Vyber obtížnost", stred, 110)
        for tlacitko, obtiznost in volby:
            tlacitko.vykresli(okno, font)
            popis = f"životy: {obtiznost['pocet_zivotu']}, body ×{obtiznost['nasobic_bodu']}"
            napis(okno, maly_font, popis, tlacitko.obdelnik.right + 20, tlacitko.obdelnik.centery - 8,
                  n.BARVA_TLUMENA, na_stred=False)
        napis(okno, maly_font, "Esc = zpět", stred, n.VYSKA - 30, n.BARVA_TLUMENA)
        pygame.display.flip()
        hodiny.tick(n.FPS)
