"""Nákupní košík.

Košík je obyčejný slovník {id produktu (text): množství} uložený v session
(podepsané cookie v prohlížeči). Do databáze se zapíše až hotová objednávka.

Funkce tady neznají Flask ani databázi, jen dostanou slovník a vrátí slovník.
Díky tomu se dají snadno testovat (tests/test_kosik.py).
"""

MAX_KUSU = 99       # víc kusů jednoho produktu do košíku nedovolíme


def over_mnozstvi(mnozstvi):
    """Převede množství z formuláře na celé číslo; nesmysl vyhodí ValueError."""
    try:
        mnozstvi = int(mnozstvi)
    except (TypeError, ValueError):
        raise ValueError("Množství musí být celé číslo.") from None
    if not 0 <= mnozstvi <= MAX_KUSU:
        raise ValueError(f"Množství musí být mezi 0 a {MAX_KUSU}.")
    return mnozstvi


def pridej(kosik, produkt_id, mnozstvi=1):
    """Přidá produkt do košíku (k už vloženým kusům přičte další)."""
    klic = str(produkt_id)
    kosik[klic] = over_mnozstvi(kosik.get(klic, 0) + over_mnozstvi(mnozstvi))
    if kosik[klic] == 0:
        del kosik[klic]
    return kosik


def nastav(kosik, produkt_id, mnozstvi):
    """Nastaví přesné množství produktu; nula produkt z košíku odebere."""
    klic = str(produkt_id)
    mnozstvi = over_mnozstvi(mnozstvi)
    if mnozstvi == 0:
        kosik.pop(klic, None)
    else:
        kosik[klic] = mnozstvi
    return kosik


def pocet_kusu(kosik):
    """Kolik kusů je v košíku dohromady (číslo u odkazu Košík v navigaci)."""
    return sum(kosik.values())


def sestav_polozky(kosik, produkty):
    """Spojí košík s údaji o produktech z databáze.

    produkty: slovník {id produktu: záznam produktu}
    Vrátí (seznam položek, celková cena). Produkt, který mezitím z nabídky
    zmizel, se přeskočí.
    """
    polozky = []
    celkem = 0
    for klic, mnozstvi in kosik.items():
        produkt = produkty.get(int(klic))
        if produkt is None:
            continue
        mezisoucet = produkt["cena_kc"] * mnozstvi
        polozky.append({"produkt": produkt, "mnozstvi": mnozstvi, "mezisoucet": mezisoucet})
        celkem += mezisoucet
    return polozky, celkem
