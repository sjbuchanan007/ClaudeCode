#!/usr/bin/env python3
"""Generate the Wolves Ay We bot profile picture: a geometric wolf head in the
club's old gold and black. Outputs avatar.png (1024x1024)."""
from PIL import Image, ImageDraw

GOLD = (250, 166, 26)      # Wolves old gold
BLACK = (20, 20, 20)
SIZE = 1024
S = SIZE / 512.0           # scale factor (coords designed on a 512 grid)

def sc(pts):
    return [(x * S, y * S) for (x, y) in pts]

img = Image.new("RGB", (SIZE, SIZE), GOLD)
d = ImageDraw.Draw(img)

# subtle darker-gold ring for a badge feel
d.ellipse([12*S, 12*S, 500*S, 500*S], outline=(214, 138, 16), width=int(10*S))

# --- wolf head (black) ---
head = [
    (120, 96),   # left ear tip
    (206, 176),  # left ear inner
    (256, 150),  # dip between ears
    (306, 176),  # right ear inner
    (392, 96),   # right ear tip
    (372, 214),  # right upper cheek
    (402, 300),  # right outer cheek
    (332, 362),  # right jaw
    (300, 420),  # right of snout
    (256, 452),  # chin
    (212, 420),  # left of snout
    (180, 362),  # left jaw
    (110, 300),  # left outer cheek
    (140, 214),  # left upper cheek
]
d.polygon(sc(head), fill=BLACK)

# --- eyes (gold negative space, angled = fierce) ---
left_eye = [(196, 258), (250, 240), (240, 286)]
right_eye = [(316, 258), (262, 240), (272, 286)]
d.polygon(sc(left_eye), fill=GOLD)
d.polygon(sc(right_eye), fill=GOLD)

# --- muzzle highlight: gold notch leaving a black nose tip ---
muzzle = [(230, 372), (282, 372), (256, 414)]
d.polygon(sc(muzzle), fill=GOLD)
nose = [(244, 372), (268, 372), (256, 392)]
d.polygon(sc(nose), fill=BLACK)

img.save("avatar.png")
print("wrote avatar.png", img.size)
