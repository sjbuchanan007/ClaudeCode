"""Real-data Tesco World Cup graphics for The Valuator (1080x1080)."""
from PIL import Image, ImageDraw
from make_wc import (W, H, GOLD, GOLD_SOFT, CREAM, MUTED, GREEN, font, ctext,
                     bg, glow, football)
from make_logo import make_mark


def roundRect(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def footer_disclaimer(d, note):
    # gold url pill
    url = "thevaluator.app"
    uf = font("LiberationSans-Bold.ttf", 36)
    uw = d.textlength(url, font=uf)
    pw, ph = uw + 80, 70
    px, py = (W - pw) / 2, 905
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=ph / 2, fill=GOLD)
    d.text(((W - uw) / 2, py + 14), url, font=uf, fill=(28, 20, 16))
    ctext(d, 1002, note, font("LiberationSans-Regular.ttf", 22), (150, 134, 108))


def ranked_card(fname, title, sub, rows, punch=None):
    """rows: list of (name, detail, ppint, best, badge)"""
    img = Image.new("RGB", (W, H), (20, 15, 11))
    d = ImageDraw.Draw(img); bg(d)
    football(d, 92, 100, 44)
    d.text((168, 68), title, font=font("LiberationSans-Bold.ttf", 54), fill=CREAM)
    d.text((170, 142), sub, font=font("LiberationSans-Regular.ttf", 27), fill=MUTED)
    d.line([(60, 232), (1020, 232)], fill=(70, 56, 38), width=2)

    top, rh = 270, 122
    for i, (name, detail, ppint, best, badge) in enumerate(rows):
        y = top + i * rh
        roundRect(d, [60, y, 1020, y + rh - 18], 18,
                  fill=(44, 58, 37) if best else (42, 31, 23))
        d.text((96, y + 22), name, font=font("LiberationSans-Bold.ttf", 42), fill=CREAM)
        d.text((96, y + 70), detail, font=font("LiberationSans-Regular.ttf", 27), fill=MUTED)
        vf = font("LiberationSans-Bold.ttf", 48)
        val = "£%.2f/pint" % ppint
        vw = d.textlength(val, font=vf)
        d.text((988 - vw, y + 36), val, font=vf, fill=GOLD if best else GOLD_SOFT)
        if badge:
            bf = font("LiberationSans-Bold.ttf", 22)
            lw = d.textlength(name, font=font("LiberationSans-Bold.ttf", 42))
            bx = 96 + lw + 18
            bw = d.textlength(badge, font=bf) + 24
            roundRect(d, [bx, y + 26, bx + bw, y + 60], 17, fill=GREEN)
            d.text((bx + 12, y + 30), badge, font=bf, fill=(12, 28, 12))
    if punch:
        ctext(d, top + len(rows) * rh + 40, punch,
              font("LiberationSans-Bold.ttf", 34), GOLD_SOFT)
    footer_disclaimer(d, "Prices spotted at Tesco this week · vary by store & time")
    img.save(fname); print("wrote", fname)


def hero_card(fname, big, line1, line2):
    img = Image.new("RGB", (W, H), (20, 15, 11))
    d = ImageDraw.Draw(img); bg(d)
    glow(img, W / 2, 430, 300, 240); d = ImageDraw.Draw(img)
    football(d, 540, 150, 64)
    ctext(d, 300, big, font("LiberationSans-Bold.ttf", 150), GOLD)
    ctext(d, 500, line1, font("LiberationSans-Bold.ttf", 44), CREAM)
    ctext(d, 575, line2, font("LiberationSans-Regular.ttf", 32), MUTED)
    footer_disclaimer(d, "Spotted at Tesco this week · prices vary by store & time")
    img.save(fname); print("wrote", fname)


if __name__ == "__main__":
    # A — best value match-day lagers (Clubcard, price per pint)
    ranked_card(
        "tesco-best.png",
        "MATCH-DAY BEST VALUE",
        "spotted at Tesco  ·  best price per pint",
        [
            ("Heineken", "15 × 440 ml  ·  £13.00", 1.12, True, "CHEAPEST"),
            ("Carling", "18 × 440 ml  ·  £15.99", 1.15, False, ""),
            ("Stella", "18 × 440 ml  ·  £17.89", 1.28, False, ""),
            ("Madri", "15 × 440 ml  ·  £15.00", 1.29, False, ""),
            ("San Miguel", "10 × 440 ml  ·  £10.00", 1.29, False, ""),
        ],
    )

    # B — the Birra Moretti pack trap
    ranked_card(
        "tesco-trap.png",
        "SAME BEER, MIND THE PACK",
        "Birra Moretti at Tesco — £18 for 18, or £18.25 for 12",
        [
            ("18 × 330 ml", "Birra Moretti  ·  £18 with Clubcard", 1.72, True, "6 MORE BOTTLES"),
            ("12 × 330 ml", "Birra Moretti  ·  £18.25", 2.62, False, "SAME £, LESS BEER"),
        ],
        punch="Near enough the same price — for 6 more bottles. Always check.",
    )

    # C — the value spread (why it pays to check)
    hero_card(
        "tesco-pint.png",
        "£1.12",
        "to £3.23 a pint",
        "The same lagers at Tesco — that's why it pays to check",
    )
