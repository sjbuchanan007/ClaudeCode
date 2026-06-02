"""Generate a Facebook promo graphic announcing The Valuator's return."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_logo import make_mark, lerp

W = H = 1080
BG_TOP = (46, 33, 23)
BG_BOT = (20, 15, 11)
GOLD = (240, 168, 48)
GOLD_SOFT = (245, 196, 110)
CREAM = (245, 230, 200)
MUTED = (185, 168, 136)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def centre_text(d, cy, text, fnt, fill, letter_spacing=0):
    """Draw text horizontally centred at vertical position cy (top)."""
    if letter_spacing == 0:
        w = d.textlength(text, font=fnt)
        d.text(((W - w) / 2, cy), text, font=fnt, fill=fill)
        return
    # manual letter spacing
    widths = [d.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + letter_spacing * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, cy), ch, font=fnt, fill=fill)
        x += w + letter_spacing


def build():
    img = Image.new("RGB", (W, H), BG_BOT)
    d = ImageDraw.Draw(img)
    # vertical gradient
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, y / H))
    # soft radial glow behind the logo
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([W/2-300, 150, W/2+300, 620], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    gold_layer = Image.new("RGB", (W, H), GOLD)
    img.paste(gold_layer, (0, 0), glow)

    # logo mark
    mark = make_mark(360)
    img.paste(mark, (int(W/2 - 180), 110), mark)

    d = ImageDraw.Draw(img)

    # "IT'S BACK" eyebrow
    centre_text(d, 470, "IT'S BACK", font("LiberationSans-Bold.ttf", 34),
                GOLD, letter_spacing=14)

    # Main headline
    centre_text(d, 520, "THE VALUATOR", font("LiberationSans-Bold.ttf", 96), CREAM)

    # Sub headline
    centre_text(d, 640, "Now a free web app — for everyone",
                font("LiberationSans-Regular.ttf", 40), GOLD_SOFT)

    # divider
    d.line([(W/2 - 240, 720), (W/2 + 240, 720)], fill=(90, 72, 50), width=2)

    # body lines
    centre_text(d, 752, "No longer iOS-only. No App Store. No downloads.",
                font("LiberationSans-Regular.ttf", 33), MUTED)
    centre_text(d, 800, "Compare any beer's value — down to the pence per ml.",
                font("LiberationSans-Regular.ttf", 33), MUTED)

    # device line
    centre_text(d, 858, "iPhone  ·  Android  ·  Tablet  ·  Laptop",
                font("LiberationSans-Bold.ttf", 30), CREAM, letter_spacing=2)

    # URL pill
    url = "thevaluator.app"
    fnt = font("LiberationSans-Bold.ttf", 40)
    tw = d.textlength(url, font=fnt)
    pad_x, pad_y = 44, 22
    pill_w = tw + pad_x * 2
    pill_h = 40 + pad_y * 2
    px = (W - pill_w) / 2
    py = 930
    d.rounded_rectangle([px, py, px + pill_w, py + pill_h],
                        radius=pill_h / 2, fill=GOLD)
    d.text(((W - tw) / 2, py + pad_y - 4), url, font=fnt, fill=(28, 20, 16))

    return img


if __name__ == "__main__":
    build().save("promo.png")
    print("wrote promo.png")
