"""Generate a modernised calligraphic 'v' lettermark (gold on dark)."""
from PIL import Image, ImageDraw


# ---- palette (matches the app dark theme) ----
BG_TOP = (44, 31, 22)
BG_BOT = (24, 18, 14)
GOLD_TOP = (245, 185, 70)
GOLD_BOT = (176, 122, 28)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def cubic(p0, p1, p2, p3, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = (u**3 * p0[0] + 3 * u**2 * t * p1[0] +
             3 * u * t**2 * p2[0] + t**3 * p3[0])
        y = (u**3 * p0[1] + 3 * u**2 * t * p1[1] +
             3 * u * t**2 * p2[1] + t**3 * p3[1])
        pts.append((x, y))
    return pts


# Outline of the 'v' traced clockwise in normalised 0..1 coords (y down).
# Each entry is a cubic bezier (start, c1, c2, end); ends chain together.
A = (0.150, 0.480)   # flourish tip (left), tapered to a point
SEGMENTS = [
    # outer (top) edge of the flourish: tip -> over the arch peak
    (A, (0.150, 0.405), (0.255, 0.345), (0.395, 0.350)),
    # outer (left) edge of the thick down-stroke, down to the bottom point
    ((0.395, 0.350), (0.420, 0.520), (0.450, 0.720), (0.445, 0.865)),
    # little foot at the bottom point
    ((0.445, 0.865), (0.452, 0.892), (0.474, 0.892), (0.492, 0.876)),
    # outer (right) edge of the thin up-stroke, up to the top-right tip
    ((0.492, 0.876), (0.590, 0.720), (0.705, 0.540), (0.842, 0.360)),
    # round the top-right tip back to its inner edge (serif)
    ((0.842, 0.360), (0.855, 0.340), (0.818, 0.340), (0.795, 0.360)),
    # inner (left) edge of the up-stroke down to the valley (right of notch)
    ((0.795, 0.360), (0.760, 0.435), (0.585, 0.640), (0.475, 0.795)),
    # inner (right) edge of the down-stroke up to the concave shoulder
    ((0.475, 0.795), (0.520, 0.650), (0.510, 0.530), (0.455, 0.450)),
    # shoulder bridging the down-stroke into the flourish (closes the gap)
    ((0.455, 0.450), (0.400, 0.430), (0.355, 0.430), (0.300, 0.440)),
    # underside of the flourish closing back at the tapered tip
    ((0.300, 0.440), (0.235, 0.455), (0.182, 0.488), A),
]


DY = -0.055  # nudge the glyph up so it sits visually centred


def build_outline(S, dy=DY):
    pts = []
    for seg in SEGMENTS:
        pts.extend([(x * S, (y + dy) * S) for (x, y) in cubic(*seg)])
    return pts


def gold_gradient(S):
    gold = Image.new("RGB", (S, S))
    gd = ImageDraw.Draw(gold)
    for y in range(S):
        gd.line([(0, y), (S, y)], fill=lerp(GOLD_TOP, GOLD_BOT, y / S))
    return gold


def glyph_mask(S):
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).polygon(build_outline(S), fill=255)
    return mask


def make_icon(size):
    """Gold 'v' on the dark theme background — for app icon / favicon."""
    SS = 4
    S = size * SS
    img = Image.new("RGB", (S, S), BG_BOT)
    d = ImageDraw.Draw(img)
    for y in range(S):
        d.line([(0, y), (S, y)], fill=lerp(BG_TOP, BG_BOT, y / S))
    img.paste(gold_gradient(S), (0, 0), glyph_mask(S))
    return img.resize((size, size), Image.LANCZOS)


def make_mark(size):
    """Gold 'v' on a transparent background — for the in-app header logo."""
    SS = 4
    S = size * SS
    gold = gold_gradient(S).convert("RGBA")
    gold.putalpha(glyph_mask(S))
    return gold.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    for sz in (180, 192, 512):
        make_icon(sz).save("icon-%d.png" % sz)
        print("wrote icon-%d.png" % sz)
    make_mark(512).save("logo-mark.png")
    print("wrote logo-mark.png")
    make_icon(1024).save("logo-preview.png")
    print("wrote logo-preview.png")
