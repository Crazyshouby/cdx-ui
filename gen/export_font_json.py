"""Écrit la police d'interface (gen_font, « KIRC Pixel ») en JSON pour les programmes qui la dessinent eux-mêmes (kdx-frames).

    python gen/export_font_json.py <fichier.json>      (KIRC : kdx-frames/assets/ui-font.json)

{ "spacing": pixels between letters, "space": width of a space, "glyphs": { char: [first row, [rows of '#' and '.']] } }
"""
import json
import sys
from pathlib import Path

import gen_font

table, spacing, space, _trim = gen_font.FACES["KIRC Pixel"]
if len(sys.argv) != 2:
    sys.exit(__doc__)
out = Path(sys.argv[1])
glyphs = {ch: [top, rows] for ch, (top, rows) in sorted(table.items())}
out.write_text(json.dumps({"spacing": spacing, "space": space, "glyphs": glyphs}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(len(glyphs), "glyphes ->", out)
