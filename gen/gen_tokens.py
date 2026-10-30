"""Génère tout ce qui dérive de tokens.json (la source unique des couleurs et des mesures de KDX-UI) :

    python gen_tokens.py            # écrit les fichiers
    python gen_tokens.py --check    # ne modifie rien ; code de sortie 1 si un fichier généré n'est pas à jour (pour la CI)

  ../kdx-ui.css                  le bloc entre « tokens:begin » et « tokens:end » (le reste du fichier est écrit à la main)
  ../themes.css                  une rampe d'accent par thème, hors rouge (le rouge est le défaut du :root)
  ../generated/kdx-tokens.h      C++ : couleurs 0xRRGGBB, accents, mesures (AudioLinker : AppState.cpp, Switcher.cpp, Panels.cpp)
  ../generated/tokens.rs         Rust : les mêmes (kdx-frames : paint.rs ; KIRC)

Ajouter un accent à partir d'une teinte (même rampe que le rouge mesuré sur KDX) :
    python gen_tokens.py --new-theme nom TEINTE SATURATION RELEVÉ ENCRE_CHAMPS FOND_SÉLECTION TEXTE_SÉLECTION
    ex.  python gen_tokens.py --new-theme cuivre 25 0.9 1.0 "#ffcc99" "#3a1800" "#ffe090"
(le calcul est celui de l'ancien gen_themes.py, conservé pour mémoire.)
"""
import colorsys
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "tokens.json"
THEME_KEYS = ["a-edge", "a-mid", "a-dark", "a-hover", "a-title-from", "a-title-to", "bar-top", "bar-mid", "bar-bot", "a-spark", "accent", "accent-rgb", "field-ink", "sel-bg", "sel-fg", "ic-accent", "ic-accent-dark"]
BEGIN = "/* tokens:begin"
END = "/* tokens:end */"


def load():
    return json.loads(TOKENS.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- le bloc de jetons de kdx-ui.css
def css_region(t):
    g, r = t["global"], t["themes"]["rouge"]
    L = [f"  {BEGIN} -- généré par gen/gen_tokens.py depuis tokens.json : ne pas modifier à la main */",
         "  /* Gris neutres : jamais de teinte dans les gris. */"]
    L += [f"  --{k}: {g[k]};" for k in ("frame", "panel", "btn", "card-2", "ink", "line", "hi", "lo")]
    L += ["", "  /* Texte */"]
    L += [f"  --{k}: {g[k]};" for k in ("text", "muted", "faint")]
    L += [f"  --field-ink: {r['field-ink']};      /* texte des champs et des consoles (vert KDX) */"]
    L += ["", "  /* Rampe d'accent (défaut : rouge KDX, mesuré sur KDX 1.6). themes.css la remplace par thème. */",
          f"  --a-edge: {r['a-edge']}; --a-mid: {r['a-mid']}; --a-dark: {r['a-dark']}; --a-hover: {r['a-hover']};",
          f"  --a-title-from: {r['a-title-from']}; --a-title-to: {r['a-title-to']};",
          f"  --bar-top: {r['bar-top']}; --bar-mid: {r['bar-mid']}; --bar-bot: {r['bar-bot']}; --a-spark: {r['a-spark']};",
          f"  --accent: {r['accent']}; --accent-2: {g['accent-2']}; --accent-rgb: {r['accent-rgb']};",
          "  --bar: linear-gradient(var(--bar-top), var(--bar-mid) 45%, var(--bar-bot));",
          "  --title-focus: linear-gradient(var(--a-title-from), var(--a-title-to));",
          f"  --ic-accent: {r['ic-accent']}; --ic-accent-dark: {r['ic-accent-dark']};   /* le rouge des icônes pixel : suit l'accent */",
          "", "  /* Sélection et survol */",
          f"  --sel-bg: {r['sel-bg']}; --sel-fg: {r['sel-fg']};     /* sélection « marquée » (menus, texte sélectionné) */"]
    L += [f"  --{k}: {g[k]};" for k in ("row-hover", "row-sel", "row-sel-ring", "hover")]
    L += ["", "  /* États : une couleur de statut ne signifie jamais autre chose que son état. */",
          f"  --green: {g['green']};          /* ok, connecté */", f"  --warn: {g['warn']};           /* attention, occupé */",
          f"  --red: {g['red']};            /* problème */", f"  --red-frame: {g['red-frame']};", f"  {END}"]
    return "\n".join(L) + "\n"


def patch_css(t):
    p = ROOT / "kdx-ui.css"
    s = p.read_text(encoding="utf-8")
    m = re.search(r"  /\* tokens:begin.*?" + re.escape(END) + r"\n", s, re.S)
    if not m:
        raise SystemExit("kdx-ui.css : marqueurs « tokens:begin » / « tokens:end » introuvables")
    return p, s[:m.start()] + css_region(t) + s[m.end():]


# ---------------------------------------------------------------- themes.css
def themes_css(t):
    out = ["/* Généré par gen/gen_tokens.py depuis tokens.json -- ne pas modifier. Une rampe d'accent par thème ; le rouge est le défaut du :root de kdx-ui.css. */\n"]
    for tid, v in t["themes"].items():
        if tid == "rouge":
            continue
        out.append(f"""html[data-theme="{tid}"] {{
  --a-edge: {v['a-edge']}; --a-mid: {v['a-mid']}; --a-dark: {v['a-dark']}; --a-hover: {v['a-hover']};
  --a-title-from: {v['a-title-from']}; --a-title-to: {v['a-title-to']};
  --bar-top: {v['bar-top']}; --bar-mid: {v['bar-mid']}; --bar-bot: {v['bar-bot']}; --a-spark: {v['a-spark']};
  --accent: {v['accent']}; --accent-rgb: {v['accent-rgb']};
  --field-ink: {v['field-ink']}; --sel-bg: {v['sel-bg']}; --sel-fg: {v['sel-fg']};
  --ic-accent: {v['ic-accent']}; --ic-accent-dark: {v['ic-accent-dark']};
}}
""")
    return "\n".join(out)


# ---------------------------------------------------------------- C++ et Rust
def hexval(s):
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", s.strip())
    return int(m.group(1), 16) if m else None


def camel(k):
    return "k" + "".join(p.capitalize() for p in re.split(r"[-_]", k))


def upper(k):
    return re.sub(r"[-]", "_", k).upper()


ACCENT_FIELDS = [("edge", "a-edge"), ("mid", "a-mid"), ("dark", "a-dark"), ("hover", "a-hover"), ("title_from", "a-title-from"), ("title_to", "a-title-to"),
                 ("bar_top", "bar-top"), ("bar_mid", "bar-mid"), ("bar_bot", "bar-bot"), ("spark", "a-spark"), ("accent", "accent"), ("field_ink", "field-ink"),
                 ("sel_bg", "sel-bg"), ("sel_fg", "sel-fg"), ("icon_accent", "ic-accent"), ("icon_accent_dark", "ic-accent-dark")]


def cpp_header(t):
    v = t["version"]
    L = [f"// kdx-tokens.h -- généré par gen/gen_tokens.py (kdx-ui {v}) depuis tokens.json : ne pas modifier à la main.",
         "// Couleurs au format 0xRRGGBB. Pour un COLORREF Win32 (0x00BBGGRR) : kdx::Colorref(kdx::kFrame).",
         "#pragma once", "", "namespace kdx {", "",
         "constexpr unsigned Colorref(unsigned rgb) { return ((rgb & 0xFFu) << 16) | (rgb & 0xFF00u) | ((rgb >> 16) & 0xFFu); }", ""]
    for k, val in t["global"].items():
        h = hexval(val)
        if h is not None:
            L.append(f"constexpr unsigned {camel(k)} = 0x{h:06X};")
    L += ["", "struct Accent {", "    const char* id;", "    unsigned " + ", ".join(camel(a)[1:2].lower() + camel(a)[2:] for a, _ in ACCENT_FIELDS) + ";", "};", "",
          "// kAccents[0] est le défaut (rouge KDX).", "constexpr Accent kAccents[] = {"]
    for tid, th in t["themes"].items():
        L.append('    {"%s", %s},' % (tid, ", ".join("0x%06X" % hexval(th[c]) for _, c in ACCENT_FIELDS)))
    L += ["};", f"constexpr int kAccentCount = {len(t['themes'])};", ""]
    for k, val in t["measures"].items():
        L.append(f"constexpr int {camel(k)} = {val};")
    L += ["", "}  // namespace kdx", ""]
    return "\n".join(L)


def rust_module(t):
    v = t["version"]
    L = [f"//! tokens.rs -- généré par gen/gen_tokens.py (kdx-ui {v}) depuis tokens.json : ne pas modifier à la main.",
         "//! Couleurs au format 0xRRGGBB.", "#![allow(dead_code)]", ""]
    for k, val in t["global"].items():
        h = hexval(val)
        if h is not None:
            L.append(f"pub const {upper(k)}: u32 = 0x{h:06X};")
    L += ["", "pub struct Accent {", "    pub id: &'static str,"] + [f"    pub {a}: u32," for a, _ in ACCENT_FIELDS] + ["}", "",
          "/// `ACCENTS[0]` est le défaut (rouge KDX).", f"pub const ACCENTS: [Accent; {len(t['themes'])}] = ["]
    for tid, th in t["themes"].items():
        L.append('    Accent { id: "%s", %s },' % (tid, ", ".join("%s: 0x%06X" % (a, hexval(th[c])) for a, c in ACCENT_FIELDS)))
    L += ["];", ""]
    for k, val in t["measures"].items():
        L.append(f"pub const {upper(k)}: i32 = {val};")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- nouvel accent (algorithme de l'ancien gen_themes.py)
def hexcolor(h, s, v):
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, max(0, min(1, s)), max(0, min(1, v)))
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def new_theme(name, hue, sat, lift, ink, sel_bg, sel_fg):
    def c(k, v):
        return hexcolor(hue, sat * k, min(1, v * lift))
    edge, mid, dark, hover = c(1, .80), c(1, .533), c(1, .267), c(1, .40)
    top, bmid, bot = c(.74, .91), c(.92, .75), c(.99, .54)
    accent = c(.89, .83)
    return {"a-edge": edge, "a-mid": mid, "a-dark": dark, "a-hover": hover, "a-title-from": c(1, .196), "a-title-to": c(1, .765),
            "bar-top": top, "bar-mid": bmid, "bar-bot": bot, "a-spark": c(.55, 1.0), "accent": accent,
            "accent-rgb": ", ".join(str(int(accent[i:i + 2], 16)) for i in (1, 3, 5)),
            "field-ink": ink, "sel-bg": sel_bg, "sel-fg": sel_fg, "ic-accent": bmid, "ic-accent-dark": bot}


def outputs(t):
    cssp, csst = patch_css(t)
    return {cssp: csst, ROOT / "themes.css": themes_css(t), ROOT / "generated" / "kdx-tokens.h": cpp_header(t), ROOT / "generated" / "tokens.rs": rust_module(t)}


def main(argv):
    if argv[:1] == ["--new-theme"]:
        name, hue, sat, lift, ink, sb, sf = argv[1:8]
        t = load()
        t["themes"][name] = new_theme(name, float(hue), float(sat), float(lift), ink, sb, sf)
        TOKENS.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        argv = []
    t = load()
    stale = []
    for path, content in outputs(t).items():
        cur = path.read_text(encoding="utf-8") if path.exists() else None
        if cur != content:
            stale.append(path.relative_to(ROOT).as_posix())
            if "--check" not in argv:
                path.parent.mkdir(exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
    if "--check" in argv:
        print("à jour" if not stale else "PÉRIMÉ : " + ", ".join(stale))
        return 1 if stale else 0
    print("écrit :", ", ".join(stale) if stale else "rien à changer")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
