"""Webová část projektu Houbař (Flask):  python web.py, web pak běží na http://127.0.0.1:5000

Web pracuje se stejnou databází jako hra (přes společný soubor db.py):
registrace vytvoří účet, kterým se hráč přihlásí ve hře, a žebříček
ukazuje výsledky, které hra uložila.
"""
from flask import Flask, flash, g, redirect, render_template, request, session, url_for

import db

app = Flask(__name__)
# Klíč, kterým Flask podepisuje cookie s přihlášením. Na skutečném serveru
# by musel být tajný a nesměl by být v gitu.
app.config["SECRET_KEY"] = "vyvojovy-klic-jen-pro-skolni-projekt"
app.config["DATABAZE"] = None       # None = výchozí soubor houbar.db (testy si nastaví vlastní)


# Pomocné funkce
def spojeni():
    """Vrátí připojení k databázi pro právě zpracovávaný požadavek."""
    if "spojeni" not in g:
        g.spojeni = db.pripoj(app.config["DATABAZE"])
        db.vytvor_databazi(g.spojeni)
    return g.spojeni


@app.teardown_appcontext
def zavri_spojeni(chyba):
    """Po vyřízení požadavku připojení zavře (Flask volá automaticky)."""
    pripojeni = g.pop("spojeni", None)
    if pripojeni is not None:
        pripojeni.close()


# Stránky o hře
@app.route("/")
def index():
    """Úvodní stránka: o čem hra je."""
    return render_template("index.html")


@app.route("/pravidla")
def pravidla():
    """Pravidla hry a přehled hub."""
    # Tabulka hub se čte z databáze, takže vždy odpovídá tomu, co padá ve hře.
    return render_template("pravidla.html", druhy=db.nacti_druhy_hub(spojeni()))


@app.route("/zebricek")
def zebricek():
    """Žebříček nejlepších partií."""
    return render_template("zebricek.html", vysledky=db.zebricek(spojeni(), limit=20))


@app.route("/o-projektu")
def o_projektu():
    """Informace o autorovi, technologiích a diagramy."""
    return render_template("o_projektu.html")


# Účet: registrace, přihlášení, odhlášení
@app.route("/registrace", methods=["GET", "POST"])
def registrace():
    """GET zobrazí formulář, POST vytvoří účet."""
    if request.method == "POST":
        jmeno = request.form.get("jmeno", "")
        heslo = request.form.get("heslo", "")
        if heslo != request.form.get("heslo_znovu", ""):
            flash("Hesla se neshodují.", "chyba")
        else:
            try:
                db.registruj_hrace(spojeni(), jmeno, heslo)
            except ValueError as chyba:
                flash(str(chyba), "chyba")
            else:
                flash("Účet je vytvořený, můžeš se přihlásit tady i ve hře.", "ok")
                return redirect(url_for("prihlaseni"))
    return render_template("registrace.html")


@app.route("/prihlaseni", methods=["GET", "POST"])
def prihlaseni():
    """GET zobrazí formulář, POST ověří jméno a heslo."""
    if request.method == "POST":
        hrac = db.prihlas_hrace(spojeni(), request.form.get("jmeno", ""), request.form.get("heslo", ""))
        if hrac is None:
            flash("Špatné jméno nebo heslo.", "chyba")
        else:
            # Do session (podepsané cookie) si uložíme, kdo je přihlášený.
            session["hrac_id"] = hrac["id"]
            session["jmeno"] = hrac["jmeno"]
            flash(f"Vítej, {hrac['jmeno']}!", "ok")
            return redirect(url_for("zebricek"))
    return render_template("prihlaseni.html")


@app.route("/odhlaseni")
def odhlaseni():
    """Zapomene přihlášeného hráče."""
    session.clear()
    flash("Odhlášeno.", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # debug=True: server se po úpravě kódu sám restartuje a ukáže chyby. Jen pro vývoj!
    app.run(debug=True)
