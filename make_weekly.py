"""Reusable weekly 'best value' graphic for The Valuator.

To make a new one: edit SHOP, WEEK and DEALS below, then run:  python3 make_weekly.py
Each deal is:  (brand, quantity, size_ml, price, clubcard_price_or_None)
It auto-works out price-per-pint (using the best available price), ranks them,
and draws the top 5 onto a branded graphic (weekly-best.png).
"""
from make_tesco import ranked_card

# ─────────────────────────────  EDIT THIS EACH WEEK  ─────────────────────────────
SHOP = "Tesco"
WEEK = "this week"
TOP_N = 5  # how many to show (max 5 fits the layout)

# brand, qty, size(ml), price£, clubcard£ (or None)
DEALS = [
    ("Heineken",    15, 440, 16.00, 13.00),
    ("Carling",     18, 440, 15.99, None),
    ("Stella",      18, 440, 17.89, None),
    ("Madri",       15, 440, 19.00, 15.00),
    ("San Miguel",  10, 440, 13.00, 10.00),
    ("Corona",      18, 330, 18.99, 15.00),
    ("Cruzcampo",   12, 330, 12.25, 11.00),
    ("Birra Moretti", 18, 330, 26.25, 18.00),
    ("Peroni",      10, 330, 14.00, None),
]
# ─────────────────────────────────────────────────────────────────────────────────

ML_PER_PINT = 568.261


def price_per_pint(qty, size, price, cc):
    eff = min(price, cc) if cc is not None else price
    return eff / (qty * size / ML_PER_PINT), eff


def build():
    ranked = []
    for brand, qty, size, price, cc in DEALS:
        ppint, eff = price_per_pint(qty, size, price, cc)
        detail = "%d × %d ml  ·  £%.2f%s" % (
            qty, size, eff, " (Clubcard)" if cc is not None and cc < price else "")
        ranked.append((ppint, brand, detail))
    ranked.sort(key=lambda r: r[0])

    rows = []
    for i, (ppint, brand, detail) in enumerate(ranked[:TOP_N]):
        rows.append((brand, detail, ppint, i == 0, "CHEAPEST" if i == 0 else ""))

    print("=== full ranking ===")
    for ppint, brand, detail in ranked:
        print("  £%.2f/pint  %-14s %s" % (ppint, brand, detail))

    ranked_card(
        "weekly-best.png",
        "THIS WEEK'S BEST VALUE",
        "%s  ·  %s  ·  best price per pint" % (SHOP, WEEK),
        rows,
    )


if __name__ == "__main__":
    build()
