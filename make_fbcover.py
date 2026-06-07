"""Facebook page cover image (1640x624) with content kept in the safe zone."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_logo import make_mark, lerp

W, H = 1640, 624
BG_TOP = (46, 33, 23)
BG_BOT = (20, 15, 11)
GOLD = (240, 168, 48)
GOLD_SOFT = (245, 196, 110)
CREAM = (245, 230, 200)
MUTED = (195, 178, 145)

F = "/usr/share/fonts/truetype/liberation/"


def font(n, s):
    return ImageFont.truetype(F + n, s)


def ctext(d, cy, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, cy), text, font=fnt, fill=fill)


def build():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, y / H))

    # central glow
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse([W / 2 - 360, H / 2 - 220, W / 2 + 360, H / 2 + 220], fill=60)
    g = g.filter(ImageFilter.GaussianBlur(110))
    img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), g)

    # logo + wordmark, clustered in the centre (mobile-safe)
    mark = make_mark(120)
    img.paste(mark, (int(W / 2 - 60), 96), mark)
    d = ImageDraw.Draw(img)
    ctext(d, 246, "THE VALUATOR", font("LiberationSans-Bold.ttf", 78), CREAM)
    ctext(d, 350, "Beer Value Calculator", font("LiberationSans-Regular.ttf", 38), GOLD_SOFT)
    ctext(d, 418, "Find the best value beer — free, on any device · thevaluator.app",
          font("LiberationSans-Regular.ttf", 28), MUTED)
    return img


if __name__ == "__main__":
    build().save("fb-cover.png")
    print("wrote fb-cover.png")
