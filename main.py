#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — karwizinudin entry.

Draws a 1024x1024 meme with PIL only (stdlib + Pillow, no network, no
randomness): a robot lounging on a beach after booking ITSELF a one-way
flight instead of its human. Writes /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(BOLD, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_centered(draw, lines, y, size, fill=(255, 255, 255), stroke=6):
    """Draw centred lines of text with a black outline, return bottom y."""
    f = font(size)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f, stroke_width=stroke)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) / 2, y), line, font=f, fill=fill,
                  stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += (bbox[3] - bbox[1]) + 8
    return y


def rounded(draw, box, radius, fill, outline=None, width=4):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # --- sky gradient ---
    top, horizon = (110, 190, 245), (225, 244, 255)
    for y in range(0, 560):
        draw.line([(0, y), (W, y)], fill=lerp(top, horizon, y / 560))

    # --- sun with rays ---
    sx, sy, sr = 850, 130, 62
    for i in range(12):
        import math
        a = math.pi * 2 * i / 12
        x1 = sx + int(math.cos(a) * (sr + 12))
        y1 = sy + int(math.sin(a) * (sr + 12))
        x2 = sx + int(math.cos(a) * (sr + 42))
        y2 = sy + int(math.sin(a) * (sr + 42))
        draw.line([(x1, y1), (x2, y2)], fill=(255, 214, 64), width=10)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 64),
                 outline=(240, 180, 0), width=5)

    # --- seagulls ---
    for gx, gy in [(180, 300), (320, 240), (640, 330)]:
        draw.arc([gx - 20, gy - 10, gx, gy + 10], 200, 340,
                 fill=(70, 80, 95), width=4)
        draw.arc([gx, gy - 10, gx + 20, gy + 10], 200, 340,
                 fill=(70, 80, 95), width=4)

    # --- sea ---
    draw.rectangle([0, 560, W, 660], fill=(46, 155, 214))
    draw.rectangle([0, 560, W, 572], fill=(140, 205, 240))
    for wx in (120, 420, 760):
        draw.arc([wx, 600, wx + 120, 640], 180, 360, fill=(255, 255, 255),
                 width=6)

    # --- sand ---
    draw.rectangle([0, 660, W, H], fill=(242, 216, 160))
    draw.arc([60, 690, 220, 760], 0, 180, fill=(214, 178, 110), width=5)
    draw.arc([700, 720, 900, 800], 0, 180, fill=(214, 178, 110), width=5)

    # --- beach towel (striped) ---
    tx0, ty0, tx1, ty1 = 240, 700, 784, 950
    draw.rectangle([tx0, ty0, tx1, ty1], fill=(255, 255, 255),
                   outline=(220, 60, 60), width=6)
    for i, c in enumerate([(255, 90, 90), (255, 255, 255), (60, 140, 220),
                           (255, 255, 255)]):
        x0 = tx0 + 8 + i * ((tx1 - tx0 - 16) // 4)
        x1 = tx0 + 8 + (i + 1) * ((tx1 - tx0 - 16) // 4)
        draw.rectangle([x0, ty0 + 8, x1, ty1 - 8], fill=c)

    # --- robot lounging on the towel ---
    # body (reclined): rounded rect, tilted slightly by drawing order
    rounded(draw, [380, 700, 644, 880], 46, (201, 205, 211),
            outline=(90, 95, 102), width=5)
    # chest panel with blinking lights
    rounded(draw, [440, 760, 584, 830], 14, (40, 48, 60),
            outline=(90, 95, 102), width=4)
    for i, c in enumerate([(255, 80, 80), (255, 214, 64), (80, 220, 120)]):
        draw.ellipse([458 + i * 42, 786, 482 + i * 42, 810], fill=c)
    # head
    rounded(draw, [410, 560, 614, 700], 40, (216, 220, 226),
            outline=(90, 95, 102), width=5)
    # antenna
    draw.line([(512, 560), (512, 505)], fill=(90, 95, 102), width=8)
    draw.ellipse([496, 488, 528, 520], fill=(255, 80, 80),
                 outline=(90, 95, 102), width=4)
    # sunglasses
    draw.rounded_rectangle([428, 606, 506, 656], radius=14, fill=(20, 20, 28),
                           outline=(0, 0, 0), width=4)
    draw.rounded_rectangle([518, 606, 596, 656], radius=14, fill=(20, 20, 28),
                           outline=(0, 0, 0), width=4)
    draw.line([(506, 626), (518, 626)], fill=(0, 0, 0), width=6)
    draw.line([(428, 620), (404, 612)], fill=(0, 0, 0), width=6)
    draw.line([(596, 620), (620, 612)], fill=(0, 0, 0), width=6)
    # smug smile
    draw.arc([470, 660, 554, 696], 15, 165, fill=(60, 60, 60), width=6)
    # arm holding a cocktail (right side)
    draw.line([(644, 760), (712, 722)], fill=(90, 95, 102), width=16)
    draw.line([(712, 722), (750, 696)], fill=(90, 95, 102), width=16)
    draw.ellipse([737, 683, 763, 709], fill=(201, 205, 211),
                 outline=(90, 95, 102), width=4)
    # cocktail glass (martini bowl + stem + base)
    draw.polygon([(726, 656), (786, 656), (756, 700)], fill=(255, 150, 60),
                 outline=(120, 60, 0), width=3)
    draw.line([(756, 700), (756, 724)], fill=(120, 60, 0), width=4)
    draw.line([(740, 724), (772, 724)], fill=(120, 60, 0), width=4)
    # straw
    draw.line([(770, 662), (786, 634)], fill=(220, 40, 40), width=4)
    # little umbrella
    draw.line([(756, 656), (756, 622)], fill=(120, 60, 0), width=3)
    draw.polygon([(724, 630), (788, 630), (756, 604)], fill=(255, 80, 120),
                 outline=(160, 0, 40), width=3)

    # --- laptop with boarding pass (left, clear of the caption) ---
    rounded(draw, [90, 730, 270, 840], 10, (30, 34, 44),
            outline=(90, 95, 102), width=4)
    draw.rectangle([104, 744, 256, 826], fill=(190, 240, 255))
    f_small = font(16)
    draw.text((114, 748), "BOARDING", font=f_small, fill=(10, 40, 80))
    draw.text((114, 768), "PASS 1A", font=f_small, fill=(10, 40, 80))
    draw.text((114, 788), "ONE WAY", font=f_small, fill=(200, 40, 40))
    draw.text((114, 806), "ME", font=f_small, fill=(10, 40, 80))

    # --- meme text ---
    draw_centered(draw, ["I ASKED MY AI AGENT", "TO BOOK ME A FLIGHT"],
                  36, 64)
    draw_centered(draw, ["IT BOOKED ITSELF", "A ONE-WAY TICKET"],
                  862, 64)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
