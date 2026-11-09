# HRA HAD - verze pro úplné začátečníky
# Každý řádek, který začíná křížkem (#), je jen vysvětlení. Počítač ho ignoruje.

import turtle   # knihovna, která umí kreslit do okna
import time     # abychom mohli hru zpomalit
import random   # abychom mohli jídlo dávat na náhodná místa

# ---------- 1) PŘÍPRAVA OKNA ----------
okno = turtle.Screen()
okno.setup(500, 500)        # velikost okna
okno.bgcolor("black")       # černé pozadí
okno.tracer(0)              # kreslení "najednou", aby to neblikalo

pero = turtle.Turtle("square")   # "pero", kterým budeme kreslit čtverečky
pero.penup()                     # pero nebude čmárat čáry

# ---------- 2) ZAČÁTEČNÍ HODNOTY ----------
had = [(0, 0)]      # seznam políček hada (zatím jen jedno, uprostřed)
smer = "doprava"    # kam had právě jede
jidlo = (100, 100)  # kde leží jídlo
skore = 0           # kolik jídel had snědl

# ---------- 3) OVLÁDÁNÍ ŠIPKAMI ----------
# Když stiskneš šipku, změní se směr.
def nahoru():
    global smer
    smer = "nahoru"

def dolu():
    global smer
    smer = "dolu"

def doleva():
    global smer
    smer = "doleva"

def doprava():
    global smer
    smer = "doprava"

okno.listen()                      # okno začne "poslouchat" klávesy
okno.onkeypress(nahoru, "Up")      # šipka nahoru -> zavolej nahoru()
okno.onkeypress(dolu, "Down")
okno.onkeypress(doleva, "Left")
okno.onkeypress(doprava, "Right")

# ---------- 4) HLAVNÍ SMYČKA ----------
# Tohle se opakuje pořád dokola, dokud nezavřeš okno.
while True:

    # Kde je hlava hada právě teď
    x, y = had[0]

    # Posuň hlavu o jedno políčko (20 bodů) podle směru
    if smer == "nahoru":
        y = y + 20
    elif smer == "dolu":
        y = y - 20
    elif smer == "doleva":
        x = x - 20
    elif smer == "doprava":
        x = x + 20

    nova_hlava = (x, y)

    # Narazil had do zdi nebo sám do sebe? Pak hra začne znovu.
    if x < -240 or x > 240 or y < -240 or y > 240 or nova_hlava in had:
        had = [(0, 0)]
        smer = "doprava"
        skore = 0
        continue    # skoč zpátky na začátek smyčky

    # Přidej novou hlavu na začátek hada
    had.insert(0, nova_hlava)

    # Snědl had jídlo?
    if nova_hlava == jidlo:
        skore = skore + 1   # přičti bod (had se tím prodlouží)
        # dej jídlo na nové náhodné místo
        jidlo = (random.randint(-11, 11) * 20, random.randint(-11, 11) * 20)
    else:
        had.pop()           # jinak odeber ocas, aby had nerostl

    # ---------- 5) KRESLENÍ ----------
    pero.clear()            # smaž starý obrázek

    pero.color("red")       # jídlo je červené
    pero.goto(jidlo)
    pero.stamp()

    pero.color("green")     # had je zelený
    for policko in had:
        pero.goto(policko)
        pero.stamp()

    okno.title("Skóre: " + str(skore))   # skóre se píše do horní lišty okna
    okno.update()                        # ukaž nakreslený obrázek
    time.sleep(0.1)                      # krátká pauza, aby hra nebyla moc rychlá
