#!/usr/bin/env python3
"""Facebook cover (1640x624) in old gold & black, matching the avatar/banner.
Content kept within the centre ~80% so Facebook's mobile side-crop is safe."""
from PIL import Image, ImageDraw, ImageFont

GOLD = (250, 166, 26); BLACK = (20, 20, 20)
W, H = 1640, 624
FONTS = "/mnt/skills/examples/canvas-design/canvas-fonts"

HEAD = [(120,96),(206,176),(256,150),(306,176),(392,96),(372,214),(402,300),
        (332,362),(300,420),(256,452),(212,420),(180,362),(110,300),(140,214)]
L_EYE=[(196,258),(250,240),(240,286)]; R_EYE=[(316,258),(262,240),(272,286)]
MUZZLE=[(230,372),(282,372),(256,414)]; NOSE=[(244,372),(268,372),(256,392)]

def draw_wolf(d, cx, cy, target_h):
    s = target_h/356.0
    tf = lambda pts: [(cx+(x-256)*s, cy+(y-274)*s) for (x,y) in pts]
    d.polygon(tf(HEAD), fill=BLACK)
    for p in (L_EYE,R_EYE,MUZZLE): d.polygon(tf(p), fill=GOLD)
    d.polygon(tf(NOSE), fill=BLACK)

img = Image.new("RGB", (W,H), GOLD); d = ImageDraw.Draw(img)
draw_wolf(d, 1300, 312, 410)

title = ImageFont.truetype(f"{FONTS}/BigShoulders-Bold.ttf", 138)
tag   = ImageFont.truetype(f"{FONTS}/Outfit-Bold.ttf", 40)
cx = 585
d.text((cx, 250), "WOLVES AY WE", font=title, fill=BLACK, anchor="mm")
d.rectangle([cx-300, 345, cx+300, 353], fill=BLACK)
d.text((cx, 392), "OUT OF DARKNESS COMETH LIGHT", font=tag, fill=BLACK, anchor="mm")
d.text((cx, 440), "unofficial fan bot", font=tag, fill=(120,78,8), anchor="mm")

img.save("fb-cover.png"); print("wrote fb-cover.png", img.size)
