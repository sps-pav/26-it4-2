"""Jedna partie hry: hlavní herní smyčka.

V každém snímku se opakuje totéž:
    1) události (klávesnice, zavření okna)
    2) aktualizace (pohyb košíku, padání hub, kolize, skóre)
    3) vykreslení
"""
import random

import pygame

from hra import nastaveni as n
from hra.logika import StavHry, vyber_druh
from hra.objekty import Houba, Kosik
from hra.ui import napis, ukonci_aplikaci


def vykresli_partii(okno, font, kosik, houby, stav, zbyva_s):
    """Nakreslí celou herní scénu včetně horního řádku se skóre."""
    okno.fill(n.BARVA_POZADI)
    pygame.draw.rect(okno, n.BARVA_TRAVA, (0, n.VYSKA - n.VYSKA_TRAVY, n.SIRKA, n.VYSKA_TRAVY))
    for houba in houby:
        houba.vykresli(okno)
    kosik.vykresli(okno)
    napis(okno, font, f"Skóre: {stav.skore}", 15, 12, na_stred=False)
    napis(okno, font, f"Čas: {zbyva_s} s", n.SIRKA // 2, 24)
    napis(okno, font, f"Životy: {stav.zivoty}", n.SIRKA - 140, 12, na_stred=False)


def spust_partii(okno, hodiny, druhy, obtiznost, nahoda=random):
    """Odehraje jednu partii a vrátí dvojici (stav hry, délka partie v sekundách).

    druhy:     druhy hub načtené z databáze
    obtiznost: záznam z tabulky obtiznost (rychlost, interval, životy, násobič)
    nahoda:    generátor náhody (v testech se dá nahradit pevným)
    """
    font = pygame.font.Font(None, 32)

    kosik = Kosik()
    houby = []
    stav = StavHry(obtiznost["pocet_zivotu"], obtiznost["nasobic_bodu"])
    uplynulo_ms = 0
    do_dalsi_houby_ms = 0

    while True:
        # tick() počká, aby hra běžela na 60 FPS, a vrátí délku snímku v ms
        dt = hodiny.tick(n.FPS)

        # 1) události
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                ukonci_aplikaci()
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_ESCAPE:
                    return stav, uplynulo_ms // 1000      # hráč partii vzdal

        zbyva_s = max(0, n.DELKA_PARTIE_S - uplynulo_ms // 1000)

        # 2) aktualizace
        uplynulo_ms += dt

        klavesy = pygame.key.get_pressed()
        smer = 0
        if klavesy[pygame.K_LEFT] or klavesy[pygame.K_a]:
            smer -= 1
        if klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d]:
            smer += 1
        kosik.pohni(smer)

        # Nová houba se objeví vždy po uplynutí intervalu z tabulky obtiznost.
        do_dalsi_houby_ms -= dt
        if do_dalsi_houby_ms <= 0:
            druh = vyber_druh(druhy, nahoda)
            x = nahoda.randint(0, n.SIRKA - n.HOUBA_VELIKOST)
            rychlost = obtiznost["rychlost_padu"]
            houby.append(Houba(druh, x, rychlost))
            do_dalsi_houby_ms = obtiznost["interval_ms"]

        # Procházíme kopii seznamu (houby[:]), protože z něj během cyklu mažeme.
        for houba in houby[:]:
            houba.aktualizuj()
            if houba.obdelnik.colliderect(kosik.obdelnik):
                stav.seber(houba.druh)
                houby.remove(houba)
            elif houba.je_na_zemi():
                houby.remove(houba)

        if stav.je_konec or uplynulo_ms >= n.DELKA_PARTIE_S * 1000:
            return stav, uplynulo_ms // 1000

        # 3) vykreslení
        vykresli_partii(okno, font, kosik, houby, stav, zbyva_s)
        pygame.display.flip()
