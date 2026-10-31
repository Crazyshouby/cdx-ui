"""Compare la charte à KDX, thème par thème : capture tests/kdx-maquette.html dans Chrome headless pour chaque thème, mesure les mêmes points que
gen/kdx_reference.py sur les captures de KDX (kdx-reference/kdx.json) et compte les couleurs qui diffèrent.

    python tools/kdx-compare.py            # toutes les apparences ; code 1 s'il reste un écart
    python tools/kdx-compare.py jean lagon # quelques-unes
    python tools/kdx-compare.py --keep     # garde les captures et écrit les planches côte à côte dans build/kdx-compare/

Ce qui est comparé (CHECKS) : panneau, face et relief des boutons, texte des boutons et des libellés, champ et ses arêtes, colonnes de liste, en-tête,
pouce et flèche de défilement, dégradé et texte de la barre de titre active et inactive, anneaux des deux cadres, bouton enclenché, anneau du bouton
par défaut, pile du menu principal. Les dégradés de titre sont comparés sur trois lignes (haut, milieu, bas).
Dépend de Pillow et de Chrome (ou Edge). Les fenêtres de la maquette sont aux positions des captures de KDX : pas de détection, des origines fixes.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "gen"))
try:
    from PIL import Image
    import kdx_reference as K
except ImportError as e:  # pragma: no cover
    print("kdx-compare : ignoré,", e, "(pip install pillow)")
    sys.exit(0)

CHROME = next((p for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(p)), None)
ORIGINS = {"menu": (38, 29), "connect": (214, 27), "addressbook": (632, 27), "chat": (216, 259), "settings": (632, 261), "pm": (216, 631)}
OUT = ROOT / "build" / "kdx-compare"

# (libellé, extracteur) : ce qu'on compare entre la mesure de KDX et celle de la maquette.
CHECKS = [
    ("panneau", lambda m: m["panel"]),
    ("bouton : face", lambda m: m["button_face"]), ("bouton : texte", lambda m: m["button_text"]),
    ("bouton : contour et arêtes claires", lambda m: edge(m["button_row"])),
    ("bouton : arête sombre", lambda m: m["button_row_right"][12:15]),
    ("libellé", lambda m: m["panel_text"]), ("libellé (Settings)", lambda m: m["label_text"]),
    ("liste déroulante : face", lambda m: m["dropdown_face"]), ("liste déroulante : texte", lambda m: m["dropdown_text"]),
    ("champ", lambda m: m["field"]), ("champ : arête gauche", lambda m: m["field_edge"][7:10]), ("champ : arête droite", lambda m: m["field_edge_right"][8:11]),
    ("case à cocher", lambda m: m["checkbox_row"][2:5]),
    ("liste : colonne A", lambda m: m["col_a"]), ("liste : colonne B", lambda m: m["col_b"]), ("liste : texte", lambda m: m["row_text"]),
    ("en-tête : face", lambda m: m["header_face"]), ("en-tête : texte", lambda m: m["header_text"]),
    ("défilement : bouton", lambda m: m["sb_button_face"]), ("défilement : flèche", lambda m: next((c for c, _ in m["sb_arrow"] if c != m["sb_button_face"]), None)),
    ("défilement : pouce", lambda m: m["hsb_thumb"][0][0]),
    ("titre actif : filet haut", lambda m: m["title_active"][0]), ("titre actif : début", lambda m: m["title_active"][1]), ("titre actif : milieu", lambda m: m["title_active"][9]),
    ("titre actif : fin", lambda m: m["title_active"][18]), ("titre actif : filet bas", lambda m: m["title_active"][19]), ("titre actif : texte", lambda m: m["title_text"]),
    ("anneau actif", lambda m: m["ring_active"][:6]), ("bouton de titre actif", lambda m: m["title_button_active"][4:8]), ("cadre sous le titre actif", lambda m: m["title_button_active"][0]),
    ("titre inactif : filet haut", lambda m: m["title_inactive"][0]), ("titre inactif : début", lambda m: m["title_inactive"][1]), ("titre inactif : milieu", lambda m: m["title_inactive"][9]),
    ("titre inactif : fin", lambda m: m["title_inactive"][18]), ("titre inactif : filet bas", lambda m: m["title_inactive"][19]), ("titre inactif : texte", lambda m: m["tb_text"]),
    ("anneau inactif", lambda m: m["ring_inactive"][:6]), ("bouton de titre inactif", lambda m: m["title_button_inactive"][4:8]), ("cadre sous le titre inactif", lambda m: m["title_button_inactive"][0]),
    ("enclenché : face", lambda m: m["hl_face"]), ("enclenché : texte", lambda m: m["hl_text"]),
    ("bouton par défaut : anneau", lambda m: m["save_ring"][-7:-4]), ("bouton par défaut (Connect) : anneau", lambda m: m["connect_ring"][6:12]),
    ("menu : pile", lambda m: m["stack_face"]), ("menu : texte", lambda m: m["stack_text"]), ("menu : compteurs", lambda m: m["counter_text"]),
    ("séparateur", lambda m: m["separator_col"][-1]),
]


def edge(row):
    """[contour, arête claire 1, arête claire 2] : à partir du premier pixel qui n'est pas le panneau."""
    i = next((k for k, c in enumerate(row) if c != row[0]), None)
    return None if i is None else row[i:i + 3]


def capture(theme, png):
    prof = tempfile.mkdtemp(prefix="cdx-kdx-")
    try:
        subprocess.run([CHROME, "--headless=new", "--no-first-run", "--disable-gpu", "--disable-lcd-text", "--force-device-scale-factor=1",
                        f"--user-data-dir={prof}", "--window-size=1400,1130", "--virtual-time-budget=3000", f"--screenshot={png}",
                        (ROOT / "tests" / "kdx-maquette.html").as_uri() + f"?theme={theme}"], check=True, capture_output=True, timeout=90)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def board(theme, ours, outdir):
    """La planche : pour chaque fenêtre, KDX à gauche, la charte à droite, agrandi deux fois."""
    rows = []
    for k, (x, y) in ORIGINS.items():
        w, h = K.SIZES[k]
        a = Image.open(ROOT / "kdx-reference" / theme / f"{k}.png").convert("RGB")
        b = ours.crop((x, y, x + w, y + h))
        rows.append((a, b))
    W = max(a.width for a, _ in rows) * 2 + 20
    H = sum(a.height for a, _ in rows) + 10 * len(rows)
    out = Image.new("RGB", (W * 2, H * 2), "black")
    yy = 0
    for a, b in rows:
        out.paste(a.resize((a.width * 2, a.height * 2), Image.NEAREST), (0, yy))
        out.paste(b.resize((b.width * 2, b.height * 2), Image.NEAREST), ((a.width + 10) * 2, yy))
        yy += (a.height + 10) * 2
    outdir.mkdir(parents=True, exist_ok=True)
    out.save(outdir / f"{theme}.png", optimize=True)


def main(argv):
    keep = "--keep" in argv
    themes = [a for a in argv if not a.startswith("--")]
    ref = json.loads((ROOT / "kdx-reference" / "kdx.json").read_text(encoding="utf-8"))["appearances"]
    if not CHROME:
        print("kdx-compare : ignoré, ni Chrome ni Edge")
        return 0
    themes = themes or list(ref)
    total_bad = 0
    tmp = Path(tempfile.mkdtemp(prefix="cdx-kdx-shots-"))
    try:
        for tid in themes:
            png = tmp / f"{tid}.png"
            capture(tid, png)
            im = Image.open(png).convert("RGB")
            m = K.measure(im, origins=ORIGINS)
            m.pop("origins", None)
            bad = []
            for label, get in CHECKS:
                try:
                    a, b = get(ref[tid]), get(m)
                except Exception as e:  # une mesure absente : c'est un écart
                    a, b = "?", f"erreur {e}"
                if a != b:
                    bad.append((label, a, b))
            total_bad += len(bad)
            print(f"{tid:12} {len(CHECKS) - len(bad):2}/{len(CHECKS)} concordants" + ("" if not bad else " ; écarts : " + " · ".join(f"{l} (KDX {a} / charte {b})" for l, a, b in bad)))
            if keep:
                board(tid, im, OUT)
                shutil.copy(png, OUT / f"{tid}-maquette.png")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(("aucun écart" if not total_bad else f"{total_bad} écart(s)") + (f" ; planches dans {OUT.relative_to(ROOT).as_posix()}/" if keep else ""))
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
