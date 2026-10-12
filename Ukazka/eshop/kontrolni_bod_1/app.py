"""E-shop Zelený kout (Flask):  python app.py, web pak běží na http://127.0.0.1:5000

V 1. kontrolním bodě je hotová jen kostra webu: stránky, navigace a vzhled.
Katalog zatím ukazuje pár produktů napsaných přímo tady v kódu, ve
2. kontrolním bodě je nahradí data z databáze.
"""
from flask import Flask, render_template

app = Flask(__name__)

# Dočasná data, dokud katalog nečte z databáze. Klíče se jmenují stejně jako
# sloupce v tabulce produkt, takže šablonu pak nebude potřeba přepisovat.
PRODUKTY = [
    {"nazev": "Monstera deliciosa", "popis": "Oblíbená rostlina s děrovanými listy.", "cena_kc": 349, "sklad": 12},
    {"nazev": "Zamiokulkas", "popis": "Téměř nezničitelná rostlina s lesklými listy.", "cena_kc": 289, "sklad": 8},
    {"nazev": "Echeveria", "popis": "Sukulent ve tvaru růžice.", "cena_kc": 79, "sklad": 30},
    {"nazev": "Kaktus Mammillaria", "popis": "Kulovitý kaktus, na jaře kvete.", "cena_kc": 99, "sklad": 0},
]


# Pomocné funkce
@app.template_filter("kc")
def format_kc(castka):
    """Filtr do šablon: z čísla 1299 udělá "1 299 Kč". Použití: {{ produkt.cena_kc | kc }}"""
    return f"{castka:,}".replace(",", " ") + " Kč"


# Obchod: úvod, katalog, detail produktu
@app.route("/")
def index():
    """Úvodní stránka."""
    return render_template("index.html")


@app.route("/katalog")
def stranka_katalog():
    """Seznam produktů."""
    return render_template("katalog.html", produkty=PRODUKTY)


@app.route("/doprava")
def doprava():
    """Informace o dopravě a platbě."""
    return render_template("doprava.html")


@app.route("/o-projektu")
def o_projektu():
    """Informace o autorovi, technologiích a diagramy."""
    return render_template("o_projektu.html")


if __name__ == "__main__":
    # debug=True: server se po úpravě kódu sám restartuje a ukáže chyby. Jen pro vývoj!
    app.run(debug=True)
