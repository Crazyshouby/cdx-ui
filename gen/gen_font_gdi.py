"""Variante « contours simples » des polices KIRC Pixel, pour GDI (Win32 classique).

Les polices du kit sont en couches COLR avec des glyphes de base vides (voir gen_font.py) : GDI ne sait pas les
dessiner. Ici les contours sont dans les glyphes de base. Familles « KIRC Pixel GDI » et « KIRC Pixel Log GDI ».
À 14 px, avec le lissage coupé (GDI+ SingleBitPerPixelGridFit, ou GDI sans ClearType), chaque pixel tombe sur un
pixel d'écran : testé le 30/10/2026.

    python gen_font_gdi.py ../polices
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_font as G  # noqa: E402
from fontTools.fontBuilder import FontBuilder  # noqa: E402
from fontTools.pens.ttGlyphPen import TTGlyphPen  # noqa: E402


def plain(family):
    table, spacing, space, trim = G.FACES[family]
    chars = sorted(table)
    names = ["uni%04X" % ord(c) for c in chars]
    fb = FontBuilder(G.EM * G.PX, isTTF=True)
    fb.setupGlyphOrder([".notdef"] + names)
    cmap = {ord(c): "uni%04X" % ord(c) for c in chars}
    cmap[0xA0] = "uni0020"
    fb.setupCharacterMap(cmap)
    glyphs, metrics = {".notdef": TTGlyphPen(None).glyph()}, {".notdef": (700, 0)}
    for c in chars:
        top, rows = table[c]
        name = "uni%04X" % ord(c)
        pen = TTGlyphPen(None)
        for x0, x1, r0, r1 in G.rects(top, rows):
            xa, xb = x0 * G.PX, x1 * G.PX
            yt, yb = (G.TOP - r0) * G.PX, (G.TOP - r1) * G.PX
            pen.moveTo((xa, yb)); pen.lineTo((xa, yt)); pen.lineTo((xb, yt)); pen.lineTo((xb, yb)); pen.closePath()
        glyphs[name] = pen.glyph()
        metrics[name] = ((space if c == " " else len(rows[0]) - trim + spacing) * G.PX, 0)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=G.TOP * G.PX, descent=-(G.EM - G.TOP) * G.PX)
    fb.setupNameTable({"familyName": family + " GDI", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=G.TOP * G.PX, sTypoDescender=-(G.EM - G.TOP) * G.PX, sTypoLineGap=0,
                usWinAscent=G.TOP * G.PX, usWinDescent=(G.EM - G.TOP) * G.PX, fsType=0)
    fb.setupPost(isFixedPitch=0)
    return fb.font


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "polices"
    for fam in ("KIRC Pixel", "KIRC Pixel Log"):
        p = out / (fam.lower().replace(" ", "-") + "-gdi.ttf")
        plain(fam).save(str(p))
        print(p.name, p.stat().st_size)
