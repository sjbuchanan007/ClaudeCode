"""Generate a 1200x630 social link-preview image (Open Graph)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_logo import make_mark, lerp

W, H = 1200, 630
BG_TOP = (46, 33, 23)
BG_BOT = (20, 15, 11)
GOLD = (240, 168, 48)
GOLD_SOFT = (245, 196, 110)
CREAM = (245, 230, 200)
MUTED = (190, 172, 140)

F = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


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


def build():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, y / H))

    # soft glow behind the logo
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([W / 2 - 240, 20, W / 2 + 240, 300], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), glow)

    mark = make_mark(150)
    img.paste(mark, (int(W / 2 - 75), 56), mark)

    d = ImageDraw.Draw(img)
    ctext(d, 222, "THE VALUATOR", font("LiberationSans-Bold.ttf", 76), CREAM)
    ctext(d, 322, "Beer Value Calculator", font("LiberationSans-Regular.ttf", 40), GOLD_SOFT)
    ctext(d, 392, "Find the best value beer — down to the pence per pint",
          font("LiberationSans-Regular.ttf", 30), MUTED)

    # url pill
    url = "thevaluator.app"
    uf = font("LiberationSans-Bold.ttf", 36)
    uw = d.textlength(url, font=uf)
    pw, ph = uw + 80, 70
    px, py = (W - pw) / 2, 478
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=ph / 2, fill=GOLD)
    d.text(((W - uw) / 2, py + 14), url, font=uf, fill=(28, 20, 16))

    return img


if __name__ == "__main__":
    build().save("og-image.png")
    print("wrote og-image.png")
