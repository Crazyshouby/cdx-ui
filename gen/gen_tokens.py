"""Génère tout ce qui dérive de tokens.json (la source unique des couleurs et des mesures de CDX-UI) :

    python gen_tokens.py            # écrit les fichiers
    python gen_tokens.py --check    # ne modifie rien ; code de sortie 1 si un fichier généré n'est pas à jour (pour la CI)

  ../cdx-ui.css                  le bloc entre « tokens:begin » et « tokens:end » : les couleurs du thème par défaut (rouge) et les couleurs de statut
  ../themes.css                  la palette complète de chaque autre thème (html[data-theme="…"]), avec les anciens noms en alias
  ../generated/cdx-tokens.h      C++ : couleurs 0xRRGGBB, thèmes, mesures (AudioLinker)
  ../generated/tokens.rs         Rust : les mêmes (Messages)

Les thèmes sont les seize apparences de KDX 1.6 : mesurées par gen/kdx_reference.py (kdx-reference/kdx.json), puis écrites dans tokens.json par
gen/kdx_tokens.py. Chaque thème porte une palette complète (THEME_KEYS) : une apparence de KDX ne change pas que l'accent, mais le panneau, les boutons, le
texte, les champs, les listes, les deux barres de titre… Il n'y a plus de thème « calculé » par rotation de teinte.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "tokens.json"
BEGIN = "/* tokens:begin"
END = "/* tokens:end */"

# Les clés d'un thème, par groupe : (titre du groupe, [clés]). L'ordre est celui des blocs CSS générés.
THEME_GROUPS = [
    ("Surfaces", ["frame", "panel", "btn", "btn-hover", "card-2", "ink", "col-a", "col-b", "head", "sb-track", "sb-btn", "sb-thumb", "hl"]),
    ("Texte", ["text", "faint", "btn-text", "head-text", "list-text", "title-text", "tb-text", "hl-text", "field-ink", "own-ink", "sb-arrow"]),
    ("Contours et reliefs", ["outline", "outline-active", "btn-outline", "field-outline", "line", "hi", "hi2", "lo", "lo2", "field-hi", "field-lo",
                             "row-hover", "row-sel", "row-sel-ring"]),
    ("Cadre inactif", ["tb-edge", "tb-mid", "tb-low", "tb-from", "tb-grad-mid", "tb-to"]),
    ("Cadre actif et accent", ["a-edge", "a-mid", "a-dark", "a-hover", "a-title-from", "a-title-mid", "a-title-to", "bar-top", "bar-mid", "bar-bot",
                               "a-spark", "accent", "accent-rgb", "ic-accent", "ic-accent-dark", "def-outline", "def-edge", "def-mid"]),
    ("Sélection", ["sel-bg", "sel-fg"]),
]
THEME_KEYS = [k for _, ks in THEME_GROUPS for k in ks]
META_KEYS = ["nom", "kdx", "scheme"]


def load():
    t = json.loads(TOKENS.read_text(encoding="utf-8"))
    for tid, th in t["themes"].items():
        missing = [k for k in THEME_KEYS + META_KEYS if k not in th]
        if missing:
            raise SystemExit(f"tokens.json : le thème « {tid} » n'a pas {', '.join(missing)}")
    return t


def aliases_of(t, tid):
    return [a for a, target in t.get("aliases", {}).items() if target == tid and not a.startswith("_")]


def selector(t, tid):
    return ", ".join(f'html[data-theme="{n}"]' for n in [tid] + aliases_of(t, tid))


def css_lines(th, indent="  "):
    L = []
    for title, keys in THEME_GROUPS:
        L.append(f"{indent}/* {title} */")
        row = []
        for k in keys:
            row.append(f"--{k}: {th[k]};")
            if len(row) == 6:
                L.append(indent + " ".join(row)); row = []
        if row:
            L.append(indent + " ".join(row))
    L.append(f"{indent}--scheme: {th['scheme']};")
    L.append(f"{indent}/* Images : une image ne lit pas de jeton, ces flèches sont donc générées à la couleur du thème (texte des boutons, flèches de défilement). */")
    L.append(f"{indent}--sel-arrow: {svg(9, 5, 'M0 0h9L4.5 5z', th['btn-text'])};")
    L.append(f"{indent}--sb-up: {svg(8, 4, 'M0 4h8L4 0z', th['sb-arrow'])}; --sb-down: {svg(8, 4, 'M0 0h8L4 4z', th['sb-arrow'])};")
    L.append(f"{indent}--sb-left: {svg(4, 8, 'M4 0v8L0 4z', th['sb-arrow'])}; --sb-right: {svg(4, 8, 'M0 0v8l4-4z', th['sb-arrow'])};")
    return L


def svg(w, h, d, fill):
    return f"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'%3E%3Cpath d='{d}' fill='%23{fill[1:]}'/%3E%3C/svg%3E\")"


# ---------------------------------------------------------------- le bloc de jetons de cdx-ui.css : le thème par défaut (rouge) + les couleurs de statut
def css_region(t):
    g, r = t["global"], t["themes"]["rouge"]
    L = [f"  {BEGIN} -- généré par gen/gen_tokens.py depuis tokens.json : ne pas modifier à la main */",
         f"  /* Thème par défaut : « {r['nom']} » ({r['kdx']}), mesuré sur KDX 1.6. themes.css remplace toute cette palette pour les autres thèmes. */"]
    L += css_lines(r)
    L += ["", "  /* États : une couleur de statut ne signifie jamais autre chose que son état, et ne change pas avec le thème. */",
          f"  --green: {g['green']};          /* ok, connecté */", f"  --warn: {g['warn']};           /* attention, occupé */",
          f"  --red: {g['red']};            /* problème */", f"  {END}"]
    return "\n".join(L) + "\n"


def patch_css(t):
    p = ROOT / "cdx-ui.css"
    s = p.read_text(encoding="utf-8")
    m = re.search(r"  /\* tokens:begin.*?" + re.escape(END) + r"\n", s, re.S)
    if not m:
        raise SystemExit("cdx-ui.css : marqueurs « tokens:begin » / « tokens:end » introuvables")
    return p, s[:m.start()] + css_region(t) + s[m.end():]


# ---------------------------------------------------------------- themes.css
def themes_css(t):
    out = ["/* Généré par gen/gen_tokens.py depuis tokens.json -- ne pas modifier. La palette complète de chaque thème (les apparences de KDX 1.6) ;",
           "   le rouge est le défaut du :root de cdx-ui.css. Les anciens noms (cdx-ui 1.x) restent acceptés comme alias. */", ""]
    for tid, v in t["themes"].items():
        if tid == "rouge":
            continue
        out.append(f"/* {v['nom']} ({v['kdx']}) */")
        out.append(selector(t, tid) + " {")
        out += css_lines(v)
        out.append("}\n")
    return "\n".join(out)


# ---------------------------------------------------------------- C++ et Rust
def hexval(s):
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", s.strip())
    return int(m.group(1), 16) if m else None


def camel(k):
    return "k" + "".join(p.capitalize() for p in re.split(r"[-_]", k))


def lower_camel(k):
    c = camel(k)[1:]
    return c[0].lower() + c[1:]


def snake(k):
    return k.replace("-", "_")


def upper(k):
    return snake(k).upper()


COLOR_KEYS = [k for k in THEME_KEYS if k != "accent-rgb"]


def cpp_header(t):
    v = t["version"]
    L = [f"// cdx-tokens.h -- généré par gen/gen_tokens.py (cdx-ui {v}) depuis tokens.json : ne pas modifier à la main.",
         "// Couleurs au format 0xRRGGBB. Pour un COLORREF Win32 (0x00BBGGRR) : cdx::Colorref(cdx::kThemes[0].panel).",
         "#pragma once", "", "namespace cdx {", "",
         "constexpr unsigned Colorref(unsigned rgb) { return ((rgb & 0xFFu) << 16) | (rgb & 0xFF00u) | ((rgb >> 16) & 0xFFu); }", "",
         "// Couleurs de statut : les mêmes dans tous les thèmes."]
    for k, val in t["global"].items():
        h = hexval(val)
        if h is not None:
            L.append(f"constexpr unsigned {camel(k)} = 0x{h:06X};")
    L += ["", "// Un thème : la palette complète d'une apparence de KDX (voir THEME_GROUPS dans gen/gen_tokens.py). light : texte sombre sur fond clair.",
          "struct Theme {", "    const char* id;", "    const char* nom;", "    bool light;"]
    for title, keys in THEME_GROUPS:
        ks = [lower_camel(k) for k in keys if k != "accent-rgb"]
        L.append(f"    unsigned {', '.join(ks)};  // {title}")
    L += ["};", "", "// kThemes[0] est le défaut (rouge). Les anciens noms (bleu, vert, violet, charbon, cdx) sont dans kThemeAliases.", "constexpr Theme kThemes[] = {"]
    for tid, th in t["themes"].items():
        L.append('    {"%s", "%s", %s, %s},' % (tid, th["nom"], "true" if th["scheme"] == "light" else "false", ", ".join("0x%06X" % hexval(th[c]) for c in COLOR_KEYS)))
    L += ["};", f"constexpr int kThemeCount = {len(t['themes'])};", "",
          "struct ThemeAlias { const char* ancien; const char* id; };", "constexpr ThemeAlias kThemeAliases[] = {"]
    for a, target in t.get("aliases", {}).items():
        if not a.startswith("_"):
            L.append(f'    {{"{a}", "{target}"}},')
    L += ["};", f"constexpr int kThemeAliasCount = {len([a for a in t.get('aliases', {}) if not a.startswith('_')])};", "",
          "// Compatibilité cdx-ui 1.x : Accent = la partie « accent » d'un thème.", "using Accent = Theme;", "constexpr const Theme* kAccents = kThemes;",
          "constexpr int kAccentCount = kThemeCount;", ""]
    for k, val in t["measures"].items():
        L.append(f"constexpr int {camel(k)} = {val};")
    L += ["", "}  // namespace cdx", ""]
    return "\n".join(L)


def rust_module(t):
    v = t["version"]
    L = [f"//! tokens.rs -- généré par gen/gen_tokens.py (cdx-ui {v}) depuis tokens.json : ne pas modifier à la main.",
         "//! Couleurs au format 0xRRGGBB.", "#![allow(dead_code)]", "", "// Couleurs de statut : les mêmes dans tous les thèmes."]
    for k, val in t["global"].items():
        h = hexval(val)
        if h is not None:
            L.append(f"pub const {upper(k)}: u32 = 0x{h:06X};")
    L += ["", "/// Un thème : la palette complète d'une apparence de KDX (voir THEME_GROUPS dans gen/gen_tokens.py). `light` : texte sombre sur fond clair.",
          "pub struct Theme {", "    pub id: &'static str,", "    pub nom: &'static str,", "    pub light: bool,"]
    for title, keys in THEME_GROUPS:
        L.append(f"    // {title}")
        L += [f"    pub {snake(k)}: u32," for k in keys if k != "accent-rgb"]
    L += ["}", "", "/// `THEMES[0]` est le défaut (rouge). Les anciens noms (bleu, vert, violet, charbon, cdx) sont dans `THEME_ALIASES`.",
          f"pub const THEMES: [Theme; {len(t['themes'])}] = ["]
    for tid, th in t["themes"].items():
        L.append('    Theme { id: "%s", nom: "%s", light: %s, %s },' % (tid, th["nom"], "true" if th["scheme"] == "light" else "false",
                                                                        ", ".join("%s: 0x%06X" % (snake(c), hexval(th[c])) for c in COLOR_KEYS)))
    L += ["];", ""]
    al = [(a, x) for a, x in t.get("aliases", {}).items() if not a.startswith("_")]
    L += [f"pub const THEME_ALIASES: [(&str, &str); {len(al)}] = [" + ", ".join(f'("{a}", "{x}")' for a, x in al) + "];", "",
          "/// Le nom de thème actuel pour un nom donné (alias compris) ; `None` si inconnu.",
          "pub fn theme_id(name: &str) -> Option<&'static str> {",
          "    THEMES.iter().map(|t| t.id).find(|id| *id == name).or_else(|| THEME_ALIASES.iter().find(|(a, _)| *a == name).map(|(_, id)| *id))",
          "}", "", "/// Compatibilité cdx-ui 1.x.", "pub type Accent = Theme;", f"pub const ACCENTS: &[Theme; {len(t['themes'])}] = &THEMES;", ""]
    for k, val in t["measures"].items():
        L.append(f"pub const {upper(k)}: i32 = {val};")
    return "\n".join(L) + "\n"


def outputs(t):
    cssp, csst = patch_css(t)
    return {cssp: csst, ROOT / "themes.css": themes_css(t), ROOT / "generated" / "cdx-tokens.h": cpp_header(t), ROOT / "generated" / "tokens.rs": rust_module(t)}


def main(argv):
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
