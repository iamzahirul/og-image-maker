#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ওজি ইমেজ মেকার · OG Image Maker
================================
সোশ্যাল শেয়ার কার্ড (১২০০×৬৩০) বানান — টাইটেল, সাবটাইটেল আর ব্যাজ দিন,
সুন্দর গ্রেডিয়েন্ট ছবি তৈরি হয়ে যাবে। বাংলা টেক্সট সাপোর্টসহ।

ব্যবহার:
  python3 og_maker.py --title "আমার প্রজেক্ট" --subtitle "বিস্তারিত লিখুন" \
      --badge "Day 12 of 100" --theme green --out card.png

থিম: dark · green · gold · blue · sunset
"""

import argparse
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

VERSION = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

FONT_BN = os.path.join(ASSETS, "NotoSansBengali-Regular.ttf")
FONT_BN_BOLD = os.path.join(ASSETS, "NotoSansBengali-Bold.ttf")
FONT_EN = os.path.join(ASSETS, "NotoSans-Regular.ttf")

# থিম: (শেষ-ব্যাকগ্রাউন্ড উপর, নিচ, অ্যাকসেন্ট রঙ)
THEMES = {
    "dark":   ((12, 18, 32), (5, 8, 18), (0, 201, 143)),
    "green":  ((0, 77, 58), (1, 33, 26), (0, 220, 140)),
    "gold":   ((30, 24, 6), (10, 8, 3), (245, 192, 74)),
    "blue":   ((10, 30, 60), (4, 10, 26), (90, 167, 255)),
    "sunset": ((48, 16, 58), (18, 6, 24), (255, 122, 184)),
}
DEFAULT_THEME = "dark"
DEFAULT_SIZE = (1200, 630)
TEXT = (232, 237, 248)
MUTED = (170, 180, 200)


def parse_size(text):
    """'1200x630' → (1200, 630)"""
    m = re.match(r"^\s*(\d{2,4})\s*[x×]\s*(\d{2,4})\s*$", text, re.I)
    if not m:
        raise ValueError(f"সাইজ বোঝা গেল না: '{text}' (ফরম্যাট: 1200x630)")
    w, h = int(m.group(1)), int(m.group(2))
    if not (200 <= w <= 4000 and 100 <= h <= 3000):
        raise ValueError("সাইজ খুব ছোট বা বড় (প্রস্থ ২০০-৪০০০, উচ্চতা ১০০-৩০০০)")
    return (w, h)


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def make_gradient(size, top, bottom):
    """উপর→নিচ ভার্টিক্যাল গ্রেডিয়েন্ট ইমেজ"""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        c = lerp_color(top, bottom, y / max(h - 1, 1))
        for x in range(w):
            px[x, y] = c
    return img


def wrap_text(draw, text, font, max_width, max_lines=3):
    """শব্দ-ভিত্তিক টেক্সট র‍্যাপ → লাইন লিস্ট"""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:max(len(lines[-1]) - 1, 0)] + "…"
    return lines


def load_fonts(scale=1.0):
    """সাইজ অনুযায়ী স্কেল করা ফন্ট ডিকশনারি"""
    return {
        "title": ImageFont.truetype(FONT_BN_BOLD, int(64 * scale)),
        "subtitle": ImageFont.truetype(FONT_BN, int(30 * scale)),
        "badge": ImageFont.truetype(FONT_EN, int(22 * scale)),
        "footer": ImageFont.truetype(FONT_BN, int(22 * scale)),
    }


def draw_decoration(draw, size, accent):
    """কর্নারে হালকা ডেকোরেটিভ সার্কেল"""
    w, h = size
    soft = tuple(min(255, int(c * 0.9)) for c in accent)
    draw.ellipse([w - 260, -120, w + 140, 280], outline=soft, width=3)
    draw.ellipse([w - 180, -40, w + 60, 200], outline=soft, width=2)
    draw.ellipse([-140, h - 220, 180, h + 100], outline=soft, width=2)


def draw_badge(draw, pos, text, font, accent):
    """ছোট পিল-ব্যাজ"""
    x, y = pos
    pad_x, pad_y = 22, 10
    tw = draw.textlength(text, font=font)
    th = font.size
    box = [x, y, x + tw + pad_x * 2, y + th + pad_y * 2]
    draw.rounded_rectangle(box, radius=(th + pad_y * 2) // 2, fill=accent)
    fg = (4, 18, 13) if sum(accent) > 360 else TEXT
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
    return box[3]


def make_card(title, subtitle="", badge="", footer="@iamzahirul",
              theme=DEFAULT_THEME, size=DEFAULT_SIZE):
    """সব প্যারামিটার → পিলো ইমেজ (পিওর-ইশ ফাংশন, টেস্টে ব্যবহৃত)"""
    if theme not in THEMES:
        raise ValueError(f"অজানা থিম: {theme} (অপশন: {', '.join(THEMES)})")
    top, bottom, accent = THEMES[theme]
    w, h = size
    img = make_gradient(size, top, bottom)
    draw = ImageDraw.Draw(img)
    draw_decoration(draw, size, accent)

    scale = min(w / 1200, h / 630)
    fonts = load_fonts(scale)
    margin = int(80 * scale)

    y = int(70 * scale)
    if badge:
        y = draw_badge(draw, (margin, y), badge, fonts["badge"], accent) + int(40 * scale)
    else:
        y += int(30 * scale)

    max_w = w - margin * 2
    lines = wrap_text(draw, title, fonts["title"], max_w, max_lines=3)
    line_h = int(fonts["title"].size * 1.25)
    for ln in lines:
        draw.text((margin, y), ln, font=fonts["title"], fill=TEXT)
        y += line_h

    if subtitle:
        y += int(14 * scale)
        for ln in wrap_text(draw, subtitle, fonts["subtitle"], max_w, max_lines=2):
            draw.text((margin, y), ln, font=fonts["subtitle"], fill=MUTED)
            y += int(fonts["subtitle"].size * 1.4)

    # ফুটার + অ্যাকসেন্ট লাইন
    fy = h - int(70 * scale)
    draw.rectangle([margin, fy - int(24 * scale), margin + int(56 * scale), fy - int(20 * scale)], fill=accent)
    draw.text((margin, fy), footer, font=fonts["footer"], fill=MUTED)
    return img


def main(argv=None):
    p = argparse.ArgumentParser(description="ওজি ইমেজ মেকার — সোশ্যাল কার্ড জেনারেটর (বাংলা সাপোর্টসহ)")
    p.add_argument("--title", required=True, help="মূল টাইটেল")
    p.add_argument("--subtitle", default="", help="সাবটাইটেল (ঐচ্ছিক)")
    p.add_argument("--badge", default="", help="উপরের ছোট ব্যাজ টেক্সট")
    p.add_argument("--footer", default="@iamzahirul", help="নিচের ক্রেডিট লাইন")
    p.add_argument("--theme", default=DEFAULT_THEME, choices=list(THEMES), help="রঙের থিম")
    p.add_argument("--size", default="1200x630", help="মাপ, যেমন 1200x630")
    p.add_argument("--out", default="og-card.png", help="আউটপুট ফাইলের নাম")
    p.add_argument("--version", action="version", version=VERSION)
    args = p.parse_args(argv)

    try:
        size = parse_size(args.size)
        img = make_card(args.title, args.subtitle, args.badge, args.footer, args.theme, size)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    parent = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(parent, exist_ok=True)
    img.save(args.out)
    print(f"✅ {args.out} তৈরি হয়েছে ({size[0]}×{size[1]}, থিম: {args.theme})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
