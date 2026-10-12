"""Webová část projektu Houbař (Flask):  python web.py, web pak běží na http://127.0.0.1:5000

V 1. kontrolním bodě web zatím jen zobrazuje stránky a navigaci.
Napojení na databázi přibude ve 2. kontrolním bodě.
"""
from flask import Flask, render_template

app = Flask(__name__)


# Stránky o hře
@app.route("/")
def index():
    """Úvodní stránka: o čem hra je."""
    return render_template("index.html")


@app.route("/pravidla")
def pravidla():
    """Pravidla hry a přehled hub."""
    return render_template("pravidla.html")


@app.route("/zebricek")
def zebricek():
    """Žebříček nejlepších partií."""
    return render_template("zebricek.html")


@app.route("/o-projektu")
def o_projektu():
    """Informace o autorovi, technologiích a diagramy."""
    return render_template("o_projektu.html")


if __name__ == "__main__":
    # debug=True: server se po úpravě kódu sám restartuje a ukáže chyby. Jen pro vývoj!
    app.run(debug=True)
