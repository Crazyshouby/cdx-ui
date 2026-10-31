"""Variante à chasse fixe de KIRC Pixel Log, pour les terminaux (une grille de cases égales n'accepte pas une police proportionnelle).

    python gen/gen_font_mono.py ../polices        écrit kirc-pixel-mono.ttf et kirc-pixel-mono-italic.ttf

Chaque glyphe de la police console (KIRC Pixel Log) est posé dans une case de 6 colonnes, centré, avec 1 pixel d'espacement : 7 pixels d'avance, comme la
plupart des lettres de la police d'origine (6 colonnes + 1). Les glyphes plus larges que la case (M, W, %, tirets longs, points de suspension, œ, æ, Æ) sont
redessinés à 6 colonnes ci-dessous. Même moteur de construction que gen_font.py (couches COLR : un pixel de police = un pixel d'écran à 14 px).
Les formes de lettres sont celles de KIRC Pixel Log : voir la note sur leur origine dans CHARTE.md avant de publier.

Volontairement hors de gen_font.FACES : gen_assets.py y prend les polices à embarquer dans fonts.css, et la charte distribuée ne doit pas changer pour une
police que seuls les terminaux utilisent.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_font as G  # noqa: E402

CELL = 6      # colonnes de glyphe ; avec 1 pixel d'espacement, la case fait 7 pixels
SPACING = 1

# Glyphes redessinés à 6 colonnes (haut de ligne, rangées) : ceux que la police console dessine plus larges que la case.
REDRAWN = {
    "M": (3, "##..## ###### ###### ##..## ##..## ##..## ##..## ##..##"),
    "W": (3, "##..## ##..## ##..## ##..## ##..## ###### ###### ##..##"),
    "%": (3, "##...# ##..#. ....#. ...#.. ..#... .#.... .#..## #...##"),
    "—": (7, "######"),
    "…": (9, "#.#.#. #.#.#."),
}
# Les ligatures œ æ Æ sont à 7 colonnes : on en retire une, au milieu.
NARROWED = {"œ": 3, "æ": 3, "Æ": 3}


def fit(top, rows, ch):
    """Un glyphe de la police console, ramené à CELL colonnes (redessiné, rétréci ou centré)."""
    rows = list(rows)
    if ch in REDRAWN:
        top, spec = REDRAWN[ch]
        rows = spec.split()
    elif ch in NARROWED:
        c = NARROWED[ch]
        rows = [r[:c] + r[c + 1:] for r in rows]
    w = len(rows[0])
    assert w <= CELL, (ch, hex(ord(ch)), w)
    left = (CELL - w) // 2
    return top, ["." * left + r + "." * (CELL - w - left) for r in rows]


MONO = {ch: fit(top, rows, ch) for ch, (top, rows) in G.LOG.items()}


def slanted(table):
    """Italique à chasse fixe : les rangées du haut (4 pixels et plus au-dessus de la ligne de base) glissent d'un pixel vers la droite. Un pixel au plus : le glyphe
    reste dans sa case de 7 pixels, qui n'a pas de marge pour davantage (une case de terminal rogne ce qui la dépasse)."""
    out = {}
    for ch, (top, rows) in table.items():
        new = []
        for i, r in enumerate(rows):
            h = G.TOP - 1 - (top + i)
            shift = 1 if h >= 4 else 0
            new.append("." * shift + r + "." * (1 - shift))
        out[ch] = (top, new)
    return out


MONO_ITALIC = slanted(MONO)

# (table, pixels d'espacement, largeur d'une espace, colonnes de marge que l'avance ignore)
G.FACES["KIRC Pixel Mono"] = (MONO, SPACING, CELL + SPACING, 0)
G.FACES["KIRC Pixel Mono Italic"] = (MONO_ITALIC, SPACING, CELL + SPACING, 1)


def mono_font(family):
    font = G.build(family)
    font["post"].isFixedPitch = 1
    font["OS/2"].panose.bProportion = 9      # monospaced
    widths = {font["hmtx"][n][0] for n in font["hmtx"].metrics if n != ".notdef"}
    assert widths == {(CELL + SPACING) * G.PX}, widths      # toutes les avances sont égales
    return font


if __name__ == "__main__":
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "polices"
    out_dir.mkdir(exist_ok=True)
    for family, name in (("KIRC Pixel Mono", "kirc-pixel-mono.ttf"), ("KIRC Pixel Mono Italic", "kirc-pixel-mono-italic.ttf")):
        mono_font(family).save(out_dir / name)
        print(family, len(G.FACES[family][0]), "glyphes ->", out_dir / name)
