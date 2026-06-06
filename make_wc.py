"""World Cup marketing graphics for The Valuator (1080x1080 squares)."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_logo import make_mark, lerp

W = H = 1080
BG_TOP = (46, 33, 23)
BG_BOT = (20, 15, 11)
GOLD = (240, 168, 48)
GOLD_SOFT = (245, 196, 110)
CREAM = (245, 230, 200)
MUTED = (190, 172, 140)
GREEN = (92, 184, 92)
PITCH = (60, 110, 60)

F = "/usr/share/fonts/truetype/liberation/"
ML_PER_PINT = 568.261


def font(n, s):
    return ImageFont.truetype(F + n, s)


def ctext(d, cy, text, fnt, fill, ls=0):
    if ls == 0:
        w = d.textlength(text, font=fnt)
        d.text(((W - w) / 2, cy), text, font=fnt, fill=fill)
        return
    ws = [d.textlength(c, font=fnt) for c in text]
    x = (W - (sum(ws) + ls * (len(text) - 1))) / 2
    for c, w in zip(text, ws):
        d.text((x, cy), c, font=fnt, fill=fill)
        x += w + ls


def bg(d):
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, y / H))


def glow(img, cx, cy, rx, ry, strength=70, blur=90):
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=strength)
    g = g.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), g)


def football(d, cx, cy, r, fill=(245, 245, 245), ink=(20, 20, 20)):
    """A simple stylised football: white disc + central pentagon + seams."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    pent = []
    pr = r * 0.42
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pent.append((cx + pr * math.cos(a), cy + pr * math.sin(a)))
    d.polygon(pent, fill=ink)
    for (px, py) in pent:
        ang = math.atan2(py - cy, px - cx)
        d.line([(px, py), (cx + r * math.cos(ang), cy + r * math.sin(ang))],
               fill=ink, width=max(2, int(r * 0.06)))


def pill(d, cy, text, fnt, bgc=GOLD, fgc=(28, 20, 16), padx=44, h=76):
    tw = d.textlength(text, font=fnt)
    pw = tw + padx * 2
    px = (W - pw) / 2
    d.rounded_rectangle([px, cy, px + pw, cy + h], radius=h / 2, fill=bgc)
    d.text(((W - tw) / 2, cy + (h - fnt.size) / 2 - 4), text, font=fnt, fill=fgc)


def tag(d, cy, text):
    fnt = font("LiberationSans-Bold.ttf", 30)
    tw = d.textlength(text, font=fnt)
    pw, h = tw + 44, 50
    px = (W - pw) / 2
    d.rounded_rectangle([px, cy, px + pw, cy + h], radius=h / 2, fill=GREEN)
    d.text(((W - tw) / 2, cy + 9), text, font=fnt, fill=(12, 28, 12))


# ---------- 1. Match-day value ----------
def matchday():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    bg(d)
    glow(img, W / 2, 300, 260, 220)
    d = ImageDraw.Draw(img)
    img.paste(make_mark(150), (int(W / 2 - 75), 110), make_mark(150))
    d = ImageDraw.Draw(img)
    football(d, 870, 230, 70)
    tag(d, 330, "MATCH DAY")
    ctext(d, 410, "DON'T OVERPAY", font("LiberationSans-Bold.ttf", 86), CREAM)
    ctext(d, 510, "ON THE BEERS", font("LiberationSans-Bold.ttf", 86), CREAM)
    ctext(d, 640, "Find the best value before the big games —",
          font("LiberationSans-Regular.ttf", 34), MUTED)
    ctext(d, 686, "down to the pence per pint.",
          font("LiberationSans-Regular.ttf", 34), MUTED)
    pill(d, 820, "thevaluator.app", font("LiberationSans-Bold.ttf", 40))
    return img


# ---------- 2. Multipack showdown ----------
def showdown():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    bg(d)
    d.line([(60, 250), (1020, 250)], fill=(70, 56, 38), width=2)
    football(d, 92, 92, 46)
    ctext(d, 70, "MULTIPACK SHOWDOWN", font("LiberationSans-Bold.ttf", 60), CREAM)
    ctext(d, 160, "same beer, same shop — which deal actually wins?",
          font("LiberationSans-Regular.ttf", 30), MUTED)

    deals = [
        ("18 × 440 ml", 14.00, 18 * 440),
        ("10 × 440 ml", 9.00, 10 * 440),
        ("4 × 440 ml", 5.00, 4 * 440),
    ]
    rows = []
    for label, price, ml in deals:
        ppint = price / (ml / ML_PER_PINT)
        rows.append((label, price, ppint))
    rows.sort(key=lambda r: r[2])

    top, rh = 300, 150
    for i, (label, price, ppint) in enumerate(rows):
        y = top + i * rh
        best = i == 0
        d.rounded_rectangle([60, y, 1020, y + rh - 22], radius=20,
                            fill=(44, 58, 37) if best else (42, 31, 23))
        d.text((100, y + 28), label, font=font("LiberationSans-Bold.ttf", 46), fill=CREAM)
        d.text((100, y + 82), "£%.2f" % price, font=font("LiberationSans-Regular.ttf", 30), fill=MUTED)
        vf = font("LiberationSans-Bold.ttf", 54)
        val = "£%.2f/pint" % ppint
        vw = d.textlength(val, font=vf)
        d.text((985 - vw, y + 46), val, font=vf, fill=GOLD if best else GOLD_SOFT)
        if best:
            bf = font("LiberationSans-Bold.ttf", 24)
            lw = d.textlength(label, font=font("LiberationSans-Bold.ttf", 46))
            bx = 100 + lw + 20
            d.rounded_rectangle([bx, y + 30, bx + d.textlength("BEST", font=bf) + 28, y + 66],
                                radius=18, fill=GREEN)
            d.text((bx + 14, y + 34), "BEST", font=bf, fill=(12, 28, 12))

    pill(d, 880, "Compare yours · thevaluator.app", font("LiberationSans-Bold.ttf", 34))
    return img


# ---------- 3. Bargain or bluff? ----------
def bluff():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    bg(d)
    glow(img, W / 2, 320, 260, 200)
    d = ImageDraw.Draw(img)
    football(d, 540, 150, 64)
    ctext(d, 280, "BARGAIN", font("LiberationSans-Bold.ttf", 96), GOLD)
    ctext(d, 384, "OR BLUFF?", font("LiberationSans-Bold.ttf", 96), CREAM)
    ctext(d, 520, "Spotted a beer deal in the supermarket?",
          font("LiberationSans-Regular.ttf", 34), MUTED)
    ctext(d, 566, "Check the real value before you fill the trolley.",
          font("LiberationSans-Regular.ttf", 34), MUTED)
    # placeholder deal box
    d.rounded_rectangle([180, 660, 900, 770], radius=18, outline=(90, 72, 50), width=3)
    ctext(d, 695, 'e.g. "18 cans for £14" — is it really?',
          font("LiberationSans-Bold.ttf", 36), GOLD_SOFT)
    pill(d, 860, "thevaluator.app", font("LiberationSans-Bold.ttf", 40))
    return img


if __name__ == "__main__":
    matchday().save("wc-matchday.png"); print("wrote wc-matchday.png")
    showdown().save("wc-showdown.png"); print("wrote wc-showdown.png")
    bluff().save("wc-bluff.png"); print("wrote wc-bluff.png")
