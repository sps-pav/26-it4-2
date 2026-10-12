"""Nastavení hry: všechny konstanty na jednom místě.

Když chceš změnit velikost okna, barvy nebo rychlost, měníš to jen tady
a nemusíš hledat čísla rozházená po celém kódu.
"""

NAZEV_HRY = "Houbař"

# Okno
SIRKA = 800
VYSKA = 600
FPS = 60

# Barvy (R, G, B)
BARVA_POZADI = (24, 46, 34)
BARVA_TRAVA = (38, 84, 50)
BARVA_TEXT = (240, 240, 230)
BARVA_TLUMENA = (160, 180, 165)
BARVA_TLACITKO = (92, 62, 40)
BARVA_TLACITKO_AKTIVNI = (140, 96, 60)
BARVA_CHYBA = (230, 90, 80)
BARVA_OK = (120, 210, 120)

# Košík (hráč)
KOSIK_SIRKA = 110
KOSIK_VYSKA = 28
KOSIK_RYCHLOST = 7          # o kolik pixelů se košík posune za jeden snímek
BARVA_KOSIK = (196, 150, 90)

# Houby
HOUBA_VELIKOST = 36
VYSKA_TRAVY = 40            # pruh trávy dole, na který houby dopadají

# Partie
DELKA_PARTIE_S = 60         # partie končí po 60 sekundách nebo po ztrátě životů
ZRYCHLENI_ZA_10_S = 0.10    # každých 10 s padají houby o 10 % rychleji
SOUBOR_LOGU = "houbar.log"  # sem se zapisují chyby (soubor je v .gitignore)
