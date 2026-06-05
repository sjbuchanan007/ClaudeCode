#!/usr/bin/env python3
"""Generate the Wolves Ay We bot banner/header (1500x500) in old gold & black,
matching the avatar. Bottom-left is kept clear for the overlapping avatar."""
from PIL import Image, ImageDraw, ImageFont

GOLD = (250, 166, 26)
BLACK = (20, 20, 20)
W, H = 1500, 500
FONTS = "/mnt/skills/examples/canvas-design/canvas-fonts"

# wolf head on a 512 grid (bbox centre ~ (256, 274), height ~356)
HEAD = [(120,96),(206,176),(256,150),(306,176),(392,96),(372,214),(402,300),
        (332,362),(300,420),(256,452),(212,420),(180,362),(110,300),(140,214)]
L_EYE = [(196,258),(250,240),(240,286)]
R_EYE = [(316,258),(262,240),(272,286)]
MUZZLE = [(230,372),(282,372),(256,414)]
NOSE = [(244,372),(268,372),(256,392)]

def draw_wolf(d, cx, cy, target_h):
    s = target_h / 356.0
    def tf(pts):
        return [(cx + (x-256)*s, cy + (y-274)*s) for (x, y) in pts]
    d.polygon(tf(HEAD), fill=BLACK)
    d.polygon(tf(L_EYE), fill=GOLD)
    d.polygon(tf(R_EYE), fill=GOLD)
    d.polygon(tf(MUZZLE), fill=GOLD)
    d.polygon(tf(NOSE), fill=BLACK)

img = Image.new("RGB", (W, H), GOLD)
d = ImageDraw.Draw(img)

# wolf on the right
draw_wolf(d, 1255, 250, 360)

# wordmark + tagline, centred in the left-middle (clear of bottom-left avatar)
title = ImageFont.truetype(f"{FONTS}/BigShoulders-Bold.ttf", 170)
tag = ImageFont.truetype(f"{FONTS}/Outfit-Bold.ttf", 40)
cx = 620
d.text((cx, 195), "WOLVES AY WE", font=title, fill=BLACK, anchor="mm")
# accent rule
d.rectangle([cx-300, 285, cx+300, 293], fill=BLACK)
d.text((cx, 330), "OUT OF DARKNESS COMETH LIGHT", font=tag, fill=BLACK, anchor="mm")
d.text((cx, 378), "unofficial fan bot", font=tag, fill=(120, 78, 8), anchor="mm")

img.save("banner.png")
print("wrote banner.png", img.size)
