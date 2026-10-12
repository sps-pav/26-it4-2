"""Přihlašovací obrazovka hry.

Hráč zadá jméno a heslo k účtu, který si vytvořil na webu (stránka Registrace).
Hra tak ví, komu má výsledek partie zapsat do databáze.
"""
import pygame

import db
from hra import nastaveni as n
from hra.ui import TextovePole, Tlacitko, napis, ukonci_aplikaci


def spust_prihlaseni(okno, hodiny, spojeni):
    """Zobrazí formulář a vrátí záznam přihlášeného hráče, nebo None (zpět do menu)."""
    velky_font = pygame.font.Font(None, 56)
    font = pygame.font.Font(None, 34)
    maly_font = pygame.font.Font(None, 24)

    stred = n.SIRKA // 2
    pole_jmeno = TextovePole("Jméno", stred, 220)
    pole_heslo = TextovePole("Heslo", stred, 310, skryte=True)
    pole_jmeno.aktivni = True
    tlacitko = Tlacitko("Přihlásit", stred, 400)
    chyba = ""

    while True:
        potvrzeno = False
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                ukonci_aplikaci()
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_ESCAPE:
                    return None
                if udalost.key == pygame.K_TAB:
                    # Tabulátor přepíná mezi poli jako ve formuláři na webu.
                    pole_jmeno.aktivni, pole_heslo.aktivni = pole_heslo.aktivni, pole_jmeno.aktivni
                    continue
                if udalost.key == pygame.K_RETURN:
                    potvrzeno = True
                    continue
            if tlacitko.je_kliknuto(udalost):
                potvrzeno = True
                continue
            pole_jmeno.zpracuj(udalost)
            pole_heslo.zpracuj(udalost)

        if potvrzeno:
            hrac = db.prihlas_hrace(spojeni, pole_jmeno.text, pole_heslo.text)
            if hrac is not None:
                return hrac
            chyba = "Špatné jméno nebo heslo."
            pole_heslo.text = ""

        okno.fill(n.BARVA_POZADI)
        napis(okno, velky_font, "Přihlášení", stred, 110)
        pole_jmeno.vykresli(okno, font, maly_font)
        pole_heslo.vykresli(okno, font, maly_font)
        tlacitko.vykresli(okno, font)
        if chyba:
            napis(okno, maly_font, chyba, stred, 455, n.BARVA_CHYBA)
        napis(okno, maly_font, "Účet si vytvoříš na webu: python web.py, stránka Registrace", stred,
              n.VYSKA - 60, n.BARVA_TLUMENA)
        napis(okno, maly_font, "Tab = další pole, Enter = přihlásit, Esc = zpět", stred,
              n.VYSKA - 30, n.BARVA_TLUMENA)
        pygame.display.flip()
        hodiny.tick(n.FPS)
