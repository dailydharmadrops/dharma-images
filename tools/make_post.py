#!/usr/bin/env python3
"""Render a Daily Dharma Drops verse image (1080x1350, 4:5) as JPEG."""
import sys
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/freefont/"
SERIF = FONT_DIR + "FreeSerif.ttf"
SERIF_B = FONT_DIR + "FreeSerifBold.ttf"
SERIF_I = FONT_DIR + "FreeSerifItalic.ttf"

W, H = 1080, 1350
BG = (251, 244, 230)
MAROON = (110, 30, 30)
SAFFRON = (214, 110, 20)
INK = (60, 40, 30)
SOFT = (130, 100, 80)


def font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_font(draw, path, text, start, max_w, min_size=28):
    size = start
    while size > min_size:
        f = font(path, size)
        if max(draw.textlength(l, font=f) for l in text.split("\n")) <= max_w:
            return f
        size -= 2
    return font(path, min_size)


def centered_block(draw, y, lines, fnt, fill, gap):
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text(((W - w) / 2, y), ln, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def render(dev, tam, source, out_path, handle="@daily.dharma.drops"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # frame
    d.rectangle([36, 36, W - 36, H - 36], outline=SAFFRON, width=4)
    d.rectangle([52, 52, W - 52, H - 52], outline=MAROON, width=1)

    # header
    f_head = font(SERIF_B, 40)
    title = "DAILY DHARMA DROPS"
    tw = d.textlength(title, font=f_head)
    d.text(((W - tw) / 2, 100), title, font=f_head, fill=MAROON)
    d.line([(W / 2 - 80, 168), (W / 2 + 80, 168)], fill=SAFFRON, width=4)

    # Devanagari
    f_dev = fit_font(d, SERIF_B, dev, 56, W - 160)
    y = centered_block(d, 400, dev.split("\n"), f_dev, MAROON, 30)

    # divider
    y += 30
    d.line([(W / 2 - 40, y), (W / 2 + 40, y)], fill=SAFFRON, width=3)
    y += 60

    # Tamil
    f_tam = fit_font(d, SERIF, tam, 48, W - 160)
    y = centered_block(d, y, tam.split("\n"), f_tam, INK, 26)

    # source
    f_src = font(SERIF_I, 36)
    src_lines = wrap(d, source, f_src, W - 240)
    sy = y + 70
    centered_block(d, sy, src_lines, f_src, SAFFRON, 14)

    # footer
    f_foot = font(SERIF, 32)
    hw = d.textlength(handle, font=f_foot)
    d.text(((W - hw) / 2, H - 150), handle, font=f_foot, fill=SOFT)

    img.save(out_path, "JPEG", quality=92, optimize=True)
    return y, sy


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Render a Daily Dharma Drops verse image")
    ap.add_argument("out", help="output .jpg path")
    ap.add_argument("--dev", required=True, help="Devanagari verse; use \\n between the two half-verse lines")
    ap.add_argument("--tam", required=True, help="Tamil-script verse; use \\n between the two half-verse lines")
    ap.add_argument("--source", required=True, help='e.g. "Bhagavad Gita 6.17"')
    a = ap.parse_args()
    render(a.dev.replace("\\n", "\n"), a.tam.replace("\\n", "\n"), a.source, a.out)
    print("wrote", a.out)
