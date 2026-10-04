# -*- coding: utf-8 -*-
"""ওজি ইমেজ মেকার — টেস্ট (pytest -q)"""
import io
import sys
from contextlib import redirect_stdout

import pytest
from PIL import Image

import og_maker as og


def test_parse_size_ok():
    assert og.parse_size("1200x630") == (1200, 630)
    assert og.parse_size("800×418") == (800, 418)


def test_parse_size_bad():
    for bad in ("abc", "1200", "50x630", "9999x630", "1200x10"):
        with pytest.raises(ValueError):
            og.parse_size(bad)


def test_unknown_theme():
    with pytest.raises(ValueError):
        og.make_card("টাইটেল", theme="nope")


@pytest.mark.parametrize("theme", list(og.THEMES))
def test_make_card_themes(tmp_path, theme):
    img = og.make_card("বাংলা টাইটেল", "সাবটাইটেল", "ব্যাজ", theme=theme)
    assert img.size == og.DEFAULT_SIZE
    assert img.mode == "RGB"


def test_make_card_custom_size():
    img = og.make_card("টেস্ট", size=(800, 418))
    assert img.size == (800, 418)


def test_wrap_text():
    img = Image.new("RGB", (100, 50))
    d = og.ImageDraw.Draw(img)
    font = og.load_fonts(1.0)["subtitle"]
    lines = og.wrap_text(d, "এক দুই তিন চার পাঁচ ছয় সাত আট নয় দশ", font, 150, max_lines=5)
    assert len(lines) >= 2
    assert all(d.textlength(ln, font=font) <= 160 for ln in lines)


def test_wrap_text_truncates():
    img = Image.new("RGB", (100, 50))
    d = og.ImageDraw.Draw(img)
    font = og.load_fonts(1.0)["subtitle"]
    lines = og.wrap_text(d, " ".join(["শব্দ"] * 50), font, 200, max_lines=2)
    assert len(lines) == 2
    assert lines[-1].endswith("…")


def test_theme_pixels_differ():
    a = og.make_card("একই টেক্সট", theme="green")
    b = og.make_card("একই টেক্সট", theme="blue")
    assert a.getpixel((10, 10)) != b.getpixel((10, 10))


def test_cli_creates_file(tmp_path):
    out = tmp_path / "card.png"
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = og.main(["--title", "সিএলআই টেস্ট", "--badge", "টেস্ট", "--out", str(out)])
    assert rc == 0
    assert out.exists()
    assert Image.open(out).size == og.DEFAULT_SIZE
    assert "তৈরি হয়েছে" in buf.getvalue()


def test_cli_all_themes(tmp_path):
    for theme in og.THEMES:
        out = tmp_path / f"{theme}.png"
        rc = og.main(["--title", "থিম", "--theme", theme, "--out", str(out)])
        assert rc == 0 and out.exists()


def test_cli_bad_size(tmp_path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = og.main(["--title", "x", "--size", "abc", "--out", str(tmp_path / "y.png")])
    assert rc == 1
    assert "সাইজ বোঝা গেল না" in buf.getvalue()


def test_cli_auto_creates_dir(tmp_path):
    out = tmp_path / "sub" / "dir" / "card.png"
    rc = og.main(["--title", "ফোল্ডার টেস্ট", "--out", str(out)])
    assert rc == 0
    assert out.exists()


def test_bangla_renders_nonblank():
    img = og.make_card("বাংলা লেখা এখানে আছে")
    # টেক্সট এলাকায় কিছু আলাদা রঙের পিক্সেল থাকতে হবে
    colors = set()
    for y in range(60, 400, 8):
        for x in range(70, 1130, 8):
            colors.add(img.getpixel((x, y)))
    assert len(colors) > 2


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
