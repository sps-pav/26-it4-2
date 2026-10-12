"""Obrazovka po skončení partie: výsledek a přehled sebraných hub."""
import pygame

from hra import nastaveni as n
from hra.ui import Tlacitko, napis, ukonci_aplikaci


def spust_konec(okno, hodiny, stav, druhy, ulozeno, nejlepsi=()):
    """Ukáže skóre a sebrané houby. Skončí po stisku klávesy nebo tlačítka.

    stav:     StavHry z právě dohrané partie
    druhy:    druhy hub z databáze (kvůli názvům)
    ulozeno:  True, pokud se výsledek podařilo zapsat do databáze
    nejlepsi: řádky žebříčku (jméno, skóre), které se vypíšou vpravo
    """
    velky_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 34)
    maly_font = pygame.font.Font(None, 26)
    tlacitko = Tlacitko("Zpět do menu", n.SIRKA // 2, n.VYSKA - 70)

    while True:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                ukonci_aplikaci()
            if udalost.type == pygame.KEYDOWN and udalost.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                return
            if tlacitko.je_kliknuto(udalost):
                return

        okno.fill(n.BARVA_POZADI)
        napis(okno, velky_font, "Konec hry", n.SIRKA // 2, 80)
        napis(okno, font, f"Skóre: {stav.skore}", n.SIRKA // 2, 150)
        if ulozeno:
            napis(okno, maly_font, "Výsledek je uložený v databázi.", n.SIRKA // 2, 185, n.BARVA_OK)
        else:
            napis(okno, maly_font, "Výsledek se nepodařilo uložit.", n.SIRKA // 2, 185, n.BARVA_CHYBA)

        # Sebrané houby: vypíšeme jen druhy, které hráč opravdu chytil.
        napis(okno, font, "Sebráno", 80, 230, na_stred=False)
        y = 270
        for druh in druhy:
            pocet = stav.sebrane.get(druh["id"], 0)
            if pocet:
                napis(okno, maly_font, f"{druh['nazev']}: {pocet}×", 80, y, n.BARVA_TLUMENA, na_stred=False)
                y += 28

        napis(okno, font, "Nejlepší hráči", 460, 230, na_stred=False)
        y = 270
        for poradi, radek in enumerate(nejlepsi, start=1):
            napis(okno, maly_font, f"{poradi}. {radek['jmeno']}: {radek['skore']}", 460, y,
                  n.BARVA_TLUMENA, na_stred=False)
            y += 28

        tlacitko.vykresli(okno, font)
        pygame.display.flip()
        hodiny.tick(n.FPS)
