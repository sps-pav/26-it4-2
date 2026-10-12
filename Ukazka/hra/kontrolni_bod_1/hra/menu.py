"""Hlavní menu hry.

Obrazovka má vlastní smyčku: čte události, kreslí tlačítka a skončí ve chvíli,
kdy si hráč něco vybere. Výsledek vrací jako text, podle kterého se main.py
rozhodne, co bude dál.
"""
import pygame

from hra import nastaveni as n
from hra.ui import Tlacitko, napis, ukonci_aplikaci


def spust_menu(okno, hodiny, jmeno_hrace=None):
    """Zobrazí menu a vrátí volbu hráče: "hrat", "odhlasit" nebo "konec"."""
    velky_font = pygame.font.Font(None, 96)
    font = pygame.font.Font(None, 36)
    maly_font = pygame.font.Font(None, 24)

    stred = n.SIRKA // 2
    tlacitko_hrat = Tlacitko("Hrát", stred, 290)
    tlacitko_konec = Tlacitko("Konec", stred, 360)

    while True:
        # 1) události
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                ukonci_aplikaci()
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_RETURN:
                    return "hrat"
                if udalost.key == pygame.K_ESCAPE:
                    return "konec"
            if tlacitko_hrat.je_kliknuto(udalost):
                return "hrat"
            if tlacitko_konec.je_kliknuto(udalost):
                return "konec"

        # 2) vykreslení
        okno.fill(n.BARVA_POZADI)
        napis(okno, velky_font, n.NAZEV_HRY, stred, 140)
        napis(okno, maly_font, "Chytej jedlé houby, muchomůrkám se vyhni.", stred, 200, n.BARVA_TLUMENA)
        tlacitko_hrat.vykresli(okno, font)
        tlacitko_konec.vykresli(okno, font)
        if jmeno_hrace:
            napis(okno, maly_font, f"Přihlášen: {jmeno_hrace}", stred, n.VYSKA - 60, n.BARVA_OK)
        napis(okno, maly_font, "Enter = hrát, Esc = konec", stred, n.VYSKA - 30, n.BARVA_TLUMENA)

        pygame.display.flip()
        hodiny.tick(n.FPS)


def spust_pripravuje_se(okno, hodiny):
    """Dočasná obrazovka pro 1. kontrolní bod, samotná hra ještě není hotová."""
    font = pygame.font.Font(None, 48)
    maly_font = pygame.font.Font(None, 28)
    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                ukonci_aplikaci()
            if udalost.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
        okno.fill(n.BARVA_POZADI)
        napis(okno, font, "Hra se připravuje...", n.SIRKA // 2, n.VYSKA // 2 - 20)
        napis(okno, maly_font, "Zpět do menu: libovolná klávesa", n.SIRKA // 2, n.VYSKA // 2 + 30,
              n.BARVA_TLUMENA)
        pygame.display.flip()
        hodiny.tick(n.FPS)
