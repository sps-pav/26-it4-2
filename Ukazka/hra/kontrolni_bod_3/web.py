"""Webová část projektu Houbař (Flask):  python web.py, web pak běží na http://127.0.0.1:5000

Web pracuje se stejnou databází jako hra (přes společný soubor db.py):
registrace vytvoří účet, kterým se hráč přihlásí ve hře, a žebříček
ukazuje výsledky, které hra uložila.
"""
import sqlite3

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for

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


def prihlaseny_hrac_id():
    """Vrátí id přihlášeného hráče; nepřihlášeného pošle chybou 401 pryč."""
    if "hrac_id" not in session:
        abort(401)
    return session["hrac_id"]


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
    # Filtr přichází v adrese: /zebricek?obtiznost=2&hledat=pe
    hledat = request.args.get("hledat", "").strip()
    obtiznost_id = request.args.get("obtiznost", type=int)      # ze špatné hodnoty bude None
    return render_template(
        "zebricek.html",
        vysledky=db.zebricek(spojeni(), obtiznost_id, hledat, limit=20),
        souhrn=db.souhrn_hracu(spojeni()),
        obtiznosti=db.nacti_obtiznosti(spojeni()),
        hledat=hledat,
        obtiznost_id=obtiznost_id,
    )


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
            return redirect(url_for("profil"))
    return render_template("prihlaseni.html")


@app.route("/odhlaseni")
def odhlaseni():
    """Zapomene přihlášeného hráče."""
    session.clear()
    flash("Odhlášeno.", "ok")
    return redirect(url_for("index"))


# Profil: moje partie, statistika, změna hesla, mazání
@app.route("/profil")
def profil():
    """Přehled partií a sebraných hub přihlášeného hráče."""
    hrac_id = prihlaseny_hrac_id()
    return render_template(
        "profil.html",
        partie=db.partie_hrace(spojeni(), hrac_id),
        houby=db.statistika_hub(spojeni(), hrac_id),
    )


@app.route("/profil/heslo", methods=["POST"])
def zmena_hesla():
    """Změní heslo (UPDATE v databázi)."""
    hrac_id = prihlaseny_hrac_id()
    try:
        db.zmen_heslo(spojeni(), hrac_id, request.form.get("stare", ""), request.form.get("nove", ""))
    except ValueError as chyba:
        flash(str(chyba), "chyba")
    else:
        flash("Heslo je změněné.", "ok")
    return redirect(url_for("profil"))


@app.route("/profil/partie/<int:partie_id>/smazat", methods=["POST"])
def smazani_partie(partie_id):
    """Smaže jednu partii přihlášeného hráče (DELETE v databázi)."""
    if db.smaz_partii(spojeni(), partie_id, prihlaseny_hrac_id()):
        flash("Partie je smazaná.", "ok")
    else:
        flash("Tuhle partii smazat nemůžeš.", "chyba")
    return redirect(url_for("profil"))


@app.route("/profil/smazat-ucet", methods=["POST"])
def smazani_uctu():
    """Smaže celý účet včetně partií a odhlásí."""
    db.smaz_hrace(spojeni(), prihlaseny_hrac_id())
    session.clear()
    flash("Účet je smazaný.", "ok")
    return redirect(url_for("index"))


# Chybové stránky: web nesmí spadnout na nesrozumitelnou hlášku
@app.errorhandler(401)
def chyba_neprihlasen(chyba):
    """Na stránku jen pro přihlášené přišel někdo nepřihlášený."""
    flash("Nejdřív se přihlas.", "chyba")
    return redirect(url_for("prihlaseni"))


@app.errorhandler(404)
def chyba_nenalezeno(chyba):
    """Neexistující adresa."""
    return render_template("chyba.html", zprava="Tahle stránka neexistuje."), 404


@app.errorhandler(sqlite3.Error)
def chyba_databaze(chyba):
    """Databáze selhala (chybí soubor, je poškozená apod.)."""
    app.logger.exception("Chyba databáze")
    return render_template("chyba.html", zprava="Databáze teď neodpovídá, zkus to později."), 500


if __name__ == "__main__":
    # debug=True: server se po úpravě kódu sám restartuje a ukáže chyby. Jen pro vývoj!
    app.run(debug=True)
