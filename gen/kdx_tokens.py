"""Écrit le bloc « themes » de tokens.json à partir des mesures de kdx-reference/kdx.json (gen/kdx_reference.py).

    python gen/kdx_tokens.py            # réécrit les thèmes de tokens.json (le reste du fichier est gardé)
    python gen/kdx_tokens.py --check    # code 1 si tokens.json ne correspond plus aux mesures et aux choix ci-dessous

Chaque apparence de KDX change une soixantaine de couleurs. La plupart sont lues directement dans les mesures ; quelques-unes se déduisent (survol, filets,
texte secondaire, rampe de la barre de jauge) par les formules ci-dessous, étalonnées pour redonner exactement les valeurs d'Evil Chiaroscuro ; et quelques-unes
ne sont pas mesurables sur les captures (texte des champs, sélection marquée) : elles sont CHOISIES ici, et dites telles.

L'ordre des clés d'un thème est celui de gen_tokens.py (THEME_KEYS) : tokens.json reste la source que lisent les générateurs ; ce script n'est que la façon
reproductible de la remplir depuis les mesures.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "kdx-reference" / "kdx.json"
TOKENS = ROOT / "tokens.json"


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def hx(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in c)


def mix(a, b, t):
    """a vers b, t de 0 à 1."""
    a, b = rgb(a), rgb(b)
    return hx(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


def lum(h):
    r, g, b = rgb(h)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


# ---------------------------------------------------------------- choix (non mesurables sur les captures : champs vides, rien de sélectionné)
# Texte des champs et des consoles. Le vert d'Evil Chiaroscuro est celui relevé sur KDX (CHARTE.md §2) ; Sunset Chiaroscuro partage ses gris et ses champs noirs.
# Ailleurs : le texte des lignes de liste mesuré s'il se lit sur le fond du champ, sinon le texte du panneau.
FIELD_INK = {"rouge": "#00ff00", "couchant": "#00ff00"}
# Sélection marquée (texte sélectionné, ligne mise en évidence d'une console) : relevée sur KDX pour le rouge ; déduite de l'accent ailleurs.
SEL = {"rouge": ("#001177", "#ff00ff"), "couchant": ("#001177", "#ff00ff")}
# Rampe d'accent du rouge, relevée sur KDX (CHARTE.md §2) : gardée telle quelle ; les autres se déduisent du bord et du milieu de leur anneau.
ROUGE_ACCENT = {"a-hover": "#660000", "bar-top": "#e83c3c", "bar-mid": "#c01010", "bar-bot": "#8a0202", "a-spark": "#ff8a74", "accent": "#d41818",
                "ic-accent": "#e02020", "ic-accent-dark": "#8a0202"}


def contrast_ok(fg, bg):
    return abs(lum(fg) - lum(bg)) > 0.35


def theme_from(tid, m):
    ta, ti = m["title_active"], m["title_inactive"]
    ra, ri = m["ring_active"], m["ring_inactive"]
    br, brr = m["button_row"], m["button_row_right"]
    ob = next(i for i, c in enumerate(br) if c != br[0])            # l'arête gauche du bouton : première couleur qui n'est pas le panneau
    btn_outline, hi, hi2 = br[ob], br[ob + 1], br[ob + 2]
    oe = len(brr) - 1 - next(i for i, c in enumerate(reversed(brr)) if c != brr[-1])   # l'arête droite : dernier pixel avant le panneau
    lo, lo2 = brr[oe - 1], brr[oe - 2]
    fe, fer = m["field_edge"], m["field_edge_right"]
    fi = next(i for i, c in enumerate(fe) if c != fe[0])            # arête gauche du champ : sombre, contour, fond
    field_lo, field_outline = fe[fi], fe[fi + 1]
    fj = next(i for i, c in enumerate(fer) if c != fer[0])          # arête droite : (contour,) clair, panneau
    if fer[fj] == field_outline:
        fj += 1
    field_hi = fer[fj]
    sr = m["save_ring"]                                             # … panneau, contour de l'anneau, bord, milieu, contour du bouton, clair 1, clair 2, face
    def_outline, def_edge, def_mid = sr[-7], sr[-6], sr[-5]
    panel, btn, text = m["panel"], m["button_face"], m["panel_text"]
    btn_text = m["button_text"] or text
    list_text = m["row_text"] or text
    ink = m["field"]
    a_edge, a_mid, a_dark = ra[1], ra[2], ra[4]
    tb_edge, tb_mid, tb_low = ri[1], ri[2], ri[4]
    outline, outline_active = ri[0], ra[0]                          # le contour de la fenêtre (noir, sauf Techno Electric et Tropical Water)
    sb_thumb = m["hsb_thumb"][0][0]
    face = m["sb_button_face"]
    arrow = next((c for c, _ in m["sb_arrow"] if c != face), None)   # le triangle : la couleur la plus fréquente après le fond du bouton
    light = lum(panel) > 0.5
    field_ink = FIELD_INK.get(tid) or (list_text if contrast_ok(list_text, ink) else text if contrast_ok(text, ink) else ("#000000" if lum(ink) > 0.5 else "#ffffff"))
    sel_bg, sel_fg = SEL.get(tid, (a_mid, "#ffffff" if lum(a_mid) < 0.5 else "#000000"))
    own_ink = "#ffffff" if lum(ink) < 0.5 else "#000000"              # ses propres lignes de console : blanc sur une console sombre, noir sur une claire
    faint = mix(text, panel, 0.5833)                                 # texte secondaire : entre le texte et le panneau (#888 sur Evil Chiaroscuro)
    if abs(lum(faint) - lum(panel)) < 0.15:                          # … sauf si cela ne se lit plus (panneau presque noir d'Amber CRT) : plus près du texte
        faint = mix(text, panel, 0.35)
    t = {
        "nom": m["nom"], "kdx": m["kdx"], "scheme": "light" if light else "dark",
        # surfaces
        "frame": lo2, "panel": panel, "btn": btn, "btn-hover": mix(btn, hi2, 0.5), "card-2": mix(btn, lo2, 0.5), "ink": ink,
        "col-a": m["col_a"], "col-b": m["col_b"], "head": m["header_face"] or btn, "sb-track": mix(btn, lo2, 0.5), "sb-btn": m["sb_button_face"], "sb-thumb": sb_thumb, "hl": m["hl_face"],
        # texte
        "text": text, "faint": faint, "btn-text": btn_text, "head-text": m["header_text"] or btn_text, "list-text": list_text,
        "title-text": m["title_text"] or "#ffffff", "tb-text": m["tb_text"] or "#ffffff", "hl-text": m["hl_text"] or btn_text, "field-ink": field_ink, "own-ink": own_ink,
        "sb-arrow": arrow or mix(text, btn, 0.5),
        # lignes et reliefs
        "outline": outline, "outline-active": outline_active, "btn-outline": btn_outline, "field-outline": field_outline, "line": mix(btn, hi, 0.66),
        "hi": hi, "hi2": hi2, "lo": lo, "lo2": lo2, "field-hi": field_hi, "field-lo": field_lo,
        "row-hover": mix(btn, hi2, 0.5), "row-sel": mix(btn, hi2, 0.75), "row-sel-ring": mix(hi, text, 0.1),
        # cadre inactif
        "tb-edge": tb_edge, "tb-mid": tb_mid, "tb-low": tb_low, "tb-from": ti[1], "tb-grad-mid": ti[9], "tb-to": ti[18],
        # cadre actif et accent
        "a-edge": a_edge, "a-mid": a_mid, "a-dark": a_dark, "a-hover": mix(a_mid, a_dark, 0.5),
        "a-title-from": ta[1], "a-title-mid": ta[9], "a-title-to": ta[18],
        "bar-top": mix(a_edge, "#ffffff", 0.2), "bar-mid": a_edge, "bar-bot": a_mid, "a-spark": mix(a_edge, "#ffffff", 0.5),
        "accent": a_edge, "accent-rgb": ", ".join(str(v) for v in rgb(a_edge)), "ic-accent": a_edge, "ic-accent-dark": a_mid,
        "def-outline": def_outline, "def-edge": def_edge, "def-mid": def_mid,
        # sélection
        "sel-bg": sel_bg, "sel-fg": sel_fg,
    }
    if tid == "rouge":
        t.update(ROUGE_ACCENT)
        t["accent-rgb"] = ", ".join(str(v) for v in rgb(t["accent"]))
    return t


def build():
    ref = json.loads(REF.read_text(encoding="utf-8"))["appearances"]
    return {tid: theme_from(tid, m) for tid, m in ref.items()}


def main(argv):
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    themes = build()
    if "--check" in argv:
        same = tokens.get("themes") == themes
        print("à jour" if same else "PÉRIMÉ : tokens.json (themes) ≠ kdx-reference/kdx.json → python gen/kdx_tokens.py")
        return 0 if same else 1
    tokens["themes"] = themes
    TOKENS.write_text(json.dumps(tokens, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"écrit : tokens.json ({len(themes)} thèmes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
