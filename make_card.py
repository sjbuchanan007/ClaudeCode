"""Mock-up of the shareable image card (how the in-app canvas version will look)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_logo import make_mark, lerp

W = H = 1080
BG_TOP = (46, 33, 23)
BG_BOT = (20, 15, 11)
GOLD = (240, 168, 48)
GOLD_SOFT = (245, 196, 110)
CREAM = (245, 230, 200)
MUTED = (185, 168, 136)
GREEN = (92, 184, 92)
ROW = (42, 31, 23)
ROW_BEST = (40, 52, 34)

FONT = "/usr/share/fonts/truetype/liberation/"
ML_PER_PINT = 568.261


def f(name, size):
    return ImageFont.truetype(FONT + name, size)


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


# sample comparison
beers = [
    {"name": "Stella Artois", "sub": "4 × 440 ml", "price": 5.00, "ml": 1760},
    {"name": "Guinness Draught", "sub": "500 ml can", "price": 2.20, "ml": 500},
    {"name": "BrewDog Punk IPA", "sub": "330 ml bottle", "price": 1.80, "ml": 330},
    {"name": "Camden Hells", "sub": "330 ml can", "price": 2.00, "ml": 330},
]
for b in beers:
    b["ppml"] = b["price"] * 100 / b["ml"]
beers.sort(key=lambda b: b["ppml"])


def build():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, y / H))

    # header: logo + title
    mark = make_mark(120)
    img.paste(mark, (int(W / 2 - 60), 56), mark)
    d = ImageDraw.Draw(img)
    ctext(d, 196, "BEER VALUE COMPARISON", f("LiberationSans-Bold.ttf", 46), CREAM)
    ctext(d, 258, "ranked best value first  ·  pence per ml",
          f("LiberationSans-Regular.ttf", 28), MUTED)

    # rows
    top = 330
    rh = 132
    for i, b in enumerate(beers):
        y = top + i * rh
        best = i == 0
        d.rounded_rectangle([60, y, 1020, y + rh - 18], radius=20,
                            fill=ROW_BEST if best else ROW)
        # rank circle
        cx, cy = 130, y + (rh - 18) / 2
        r = 38
        if best:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
            num_fill = (28, 20, 16)
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 72, 50), width=3)
            num_fill = MUTED
        nf = f("LiberationSans-Bold.ttf", 40)
        nw = d.textlength(str(i + 1), font=nf)
        d.text((cx - nw / 2, cy - 28), str(i + 1), font=nf, fill=num_fill)

        # name + sub
        d.text((196, y + 26), b["name"], font=f("LiberationSans-Bold.ttf", 42), fill=CREAM)
        d.text((196, y + 76), b["sub"], font=f("LiberationSans-Regular.ttf", 28), fill=MUTED)

        # BEST badge
        if best:
            bf = f("LiberationSans-Bold.ttf", 24)
            bw = d.textlength("BEST", font=bf)
            bx = 196 + d.textlength(b["name"], font=f("LiberationSans-Bold.ttf", 42)) + 22
            d.rounded_rectangle([bx, y + 30, bx + bw + 28, y + 66], radius=18, fill=GREEN)
            d.text((bx + 14, y + 33), "BEST", font=bf, fill=(12, 28, 12))

        # value (right aligned)
        vf = f("LiberationSans-Bold.ttf", 50)
        val = "%.3fp/ml" % b["ppml"]
        vw = d.textlength(val, font=vf)
        d.text((1000 - vw, y + 36), val, font=vf, fill=GOLD if best else GOLD_SOFT)

    # footer pill
    url = "thevaluator.app"
    uf = f("LiberationSans-Bold.ttf", 38)
    uw = d.textlength(url, font=uf)
    pw, ph = uw + 88, 76
    px, py = (W - pw) / 2, 968
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=ph / 2, fill=GOLD)
    d.text(((W - uw) / 2, py + 16), url, font=uf, fill=(28, 20, 16))

    return img


if __name__ == "__main__":
    build().save("card-mockup.png")
    print("wrote card-mockup.png")
