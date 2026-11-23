# HRA HAD v PYGAME - verze pro úplné začátečníky
# Každý řádek, který začíná křížkem (#), je jen vysvětlení. Počítač ho ignoruje.
#
# Než to spustíš poprvé, nainstaluj pygame (stačí jednou):
#     pip install pygame
#
# Ovládání: šipky. Zavřeš to křížkem okna.

import pygame   # knihovna na hry
import random   # abychom mohli jídlo dávat na náhodná místa

# ---------- 1) NASTAVENÍ ----------
VELIKOST_POLICKA = 20      # jeden čtvereček hada má 20 x 20 bodů
POCET_POLICEK = 25         # hrací plocha má 25 x 25 políček
RYCHLOST = 10              # kolik kroků za sekundu had udělá (víc = rychlejší)

CERNA = (0, 0, 0)          # barvy se píšou jako (červená, zelená, modrá)
ZELENA = (0, 200, 0)
CERVENA = (220, 0, 0)

# ---------- 2) PŘÍPRAVA OKNA ----------
pygame.init()
okno = pygame.display.set_mode((VELIKOST_POLICKA * POCET_POLICEK,
                                VELIKOST_POLICKA * POCET_POLICEK))
hodiny = pygame.time.Clock()   # hlídá, aby hra nebyla moc rychlá


# Funkce, která dá jídlo na náhodné místo (ale ne na hada)
def nove_jidlo():
    while True:
        misto = (random.randint(0, POCET_POLICEK - 1),
                 random.randint(0, POCET_POLICEK - 1))
        if misto not in had:
            return misto


# ---------- 3) ZAČÁTEČNÍ HODNOTY ----------
# Pozice hada počítáme v políčkách, ne v bodech: (sloupec, řádek)
had = [(12, 12)]        # seznam políček hada (zatím jen jedno, uprostřed)
smer = "doprava"        # kam had právě jede
jidlo = nove_jidlo()    # kde leží jídlo
skore = 0               # kolik jídel had snědl

# ---------- 4) HLAVNÍ SMYČKA ----------
# Tohle se opakuje pořád dokola, dokud nezavřeš okno.
hra_bezi = True
while hra_bezi:

    # --- Klávesy a zavření okna ---
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:          # klikl jsi na křížek
            hra_bezi = False

        if udalost.type == pygame.KEYDOWN:       # stiskl jsi klávesu
            # Had se nesmí otočit přímo do sebe (např. z doprava na doleva)
            if udalost.key == pygame.K_UP and smer != "dolu":
                smer = "nahoru"
            elif udalost.key == pygame.K_DOWN and smer != "nahoru":
                smer = "dolu"
            elif udalost.key == pygame.K_LEFT and smer != "doprava":
                smer = "doleva"
            elif udalost.key == pygame.K_RIGHT and smer != "doleva":
                smer = "doprava"

    # --- Pohyb ---
    x, y = had[0]       # kde je hlava hada právě teď

    # Posuň hlavu o jedno políčko podle směru
    # (pozor: v pygame jde řádek 0 nahoře, takže "nahoru" je MÍNUS)
    if smer == "nahoru":
        y = y - 1
    elif smer == "dolu":
        y = y + 1
    elif smer == "doleva":
        x = x - 1
    elif smer == "doprava":
        x = x + 1

    nova_hlava = (x, y)

    # Narazil had do zdi nebo sám do sebe? Pak hra začne znovu.
    if x < 0 or x >= POCET_POLICEK or y < 0 or y >= POCET_POLICEK or nova_hlava in had:
        had = [(12, 12)]
        smer = "doprava"
        skore = 0
        jidlo = nove_jidlo()
        continue        # skoč zpátky na začátek smyčky

    # Přidej novou hlavu na začátek hada
    had.insert(0, nova_hlava)

    # Snědl had jídlo?
    if nova_hlava == jidlo:
        skore = skore + 1       # přičti bod (had se tím prodlouží)
        jidlo = nove_jidlo()    # dej jídlo na nové místo
    else:
        had.pop()               # jinak odeber ocas, aby had nerostl

    # ---------- 5) KRESLENÍ ----------
    okno.fill(CERNA)    # smaž starý obrázek (celé okno načerno)

    # Jídlo - červený čtvereček
    pygame.draw.rect(okno, CERVENA,
                     (jidlo[0] * VELIKOST_POLICKA, jidlo[1] * VELIKOST_POLICKA,
                      VELIKOST_POLICKA, VELIKOST_POLICKA))

    # Had - zelené čtverečky
    for policko in had:
        pygame.draw.rect(okno, ZELENA,
                         (policko[0] * VELIKOST_POLICKA, policko[1] * VELIKOST_POLICKA,
                          VELIKOST_POLICKA - 1, VELIKOST_POLICKA - 1))

    pygame.display.set_caption("Skóre: " + str(skore))   # skóre v horní liště okna
    pygame.display.flip()        # ukaž nakreslený obrázek
    hodiny.tick(RYCHLOST)        # krátká pauza, aby hra nebyla moc rychlá

pygame.quit()   # zavři pygame, když hra skončí
