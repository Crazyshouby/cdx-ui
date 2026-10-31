"""Mesure les 16 apparences de KDX 1.6 sur des captures d'écran et écrit la fiche de référence :

    python gen/kdx_reference.py <dossier des captures>        # écrit kdx-reference/kdx.json et kdx-reference/<id>/*.png
    python gen/kdx_reference.py <dossier des captures> --check  # ne modifie rien ; code 1 si kdx.json n'est pas à jour

Les captures (une par apparence, prises dans le même ordre que la liste « Appearance » de KDX Settings) montrent toujours les mêmes fenêtres :
KDX (menu principal), Connect, Address Book, File Transfers, Chat, Settings (active), Private Messages. Chaque fenêtre est retrouvée par son contour noir
(une colonne de pixels noirs d'au moins 180 px dans une bande connue), puis tout se mesure à des positions relatives à son coin haut gauche.

Ce qui est mesuré, par apparence : panneau, face et relief des boutons, texte, champ, colonnes de liste, barre de défilement, dégradé des titres actif et
inactif, anneau actif et inactif, bouton enclenché (« Chat List »), anneau du bouton par défaut. Les champs étant vides sur les captures, la couleur de leur
texte n'est pas mesurable : tokens.json la choisit (voir CHARTE.md §2). kdx.json est une mesure brute ; tokens.json en est la lecture, à la main.

Dépend de Pillow (pip install pillow). Les captures ne sont pas dans le dépôt (10 Mo) : seules les découpes de fenêtres y sont, en kdx-reference/<id>/.
"""
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow manque : pip install pillow")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "kdx-reference"

# Ordre de la liste « Appearance » de KDX Settings = ordre des captures (noms de fichier croissants). id : le nom français du thème dans tokens.json.
APPEARANCES = [
    ("rouge", "Evil Chiaroscuro", "Clair-obscur rouge"),
    ("marine", "Alternate Romp", "Marine et rose"),
    ("ambre", "Amber CRT", "Ambre CRT"),
    ("jean", "Blue Jeans", "Bleu jean"),
    ("tramway", "Blue Tram Café", "Tramway"),
    ("sarcelle", "Bubblegum Crisis", "Sarcelle"),
    ("chocolat", "Chocolate Raspberry", "Chocolat framboise"),
    ("lavande", "Mach Lavender", "Lavande"),
    ("oxygene", "Oxygen", "Oxygène"),
    ("couchant", "Sunset Chiaroscuro", "Clair-obscur couchant"),
    ("techno", "Techno Electric", "Techno électrique"),
    ("reve-bleu", "The Dream Scheme (Blue)", "Rêve bleu"),
    ("reve-vert", "The Dream Scheme (Green)", "Rêve vert"),
    ("reve-violet", "The Dream Scheme (Purple)", "Rêve violet"),
    ("lagon", "Tropical Water", "Lagon"),
    ("turquoise", "Turquoise Hilites", "Turquoise"),
]

# Où chercher le coin haut gauche de chaque fenêtre : (x min, x max, y min, y max, hauteur minimale du bord gauche). Les captures sont décalées de quelques
# pixels les unes par rapport aux autres ; la bande est large.
WINDOWS = {
    "menu": (2, 60, 10, 60, 250),
    "connect": (170, 240, 10, 60, 180),
    "addressbook": (590, 660, 10, 60, 180),
    "chat": (170, 240, 240, 300, 300),
    "settings": (590, 660, 240, 300, 300),
    "pm": (170, 240, 610, 670, 400),
}
# Taille des fenêtres (largeur, hauteur, contour compris), pour les découpes.
SIZES = {"menu": (170, 318), "connect": (402, 220), "addressbook": (326, 222), "chat": (402, 350), "settings": (462, 352), "pm": (766, 476)}


def hx(c):
    return "#%02x%02x%02x" % tuple(c[:3])


def is_black(c):
    return c[0] < 8 and c[1] < 8 and c[2] < 8


def flat_col(px, x, y0, n):
    c = px[x, y0]
    return all(px[x, y] == c for y in range(y0, y0 + n))


def flat_row(px, x0, y, n):
    c = px[x0, y]
    return all(px[x, y] == c for x in range(x0, x0 + n))


def find_window(px, w, h, band):
    """Le coin haut gauche du contour de la fenêtre. Le fond d'écran (une nébuleuse) n'est jamais plat ; la fenêtre l'est : le bord gauche est la première
    colonne de la bande dont 100 pixels de suite sont identiques (la colonne juste à gauche ne l'étant pas) ; on remonte cette colonne tant qu'elle garde sa
    couleur : le haut de la suite est le coin, confirmé par une ligne plate de 50 px (le contour du haut) juste sous une ligne qui ne l'est pas."""
    x0, x1, y0, y1, run = band
    yp = y1 + 40                                                   # une ligne qui traverse la fenêtre sous sa barre de titre
    run = min(run, 100)                                            # le bord gauche est une ligne continue : au moins 100 px plats
    for x in range(x0, x1):
        # un contour : une colonne plate, bordée à gauche par le fond (pas plat) et à droite par la première ligne de l'anneau (plate, d'une autre couleur)
        if not (flat_col(px, x, yp, run) and not flat_col(px, x - 1, yp, 30) and flat_col(px, x + 1, yp, run) and px[x + 1, yp] != px[x, yp]):
            continue
        y = yp
        while y > 0 and px[x, y - 1] == px[x, yp]:
            y -= 1
        if y < y0 - 10 or y > y1 + 10:
            continue
        for dy in (0, -1, 1, -2, 2):
            if flat_row(px, x + 10, y + dy, 50) and not flat_row(px, x + 10, y + dy - 1, 50):
                return x, y + dy
        return x, y
    return None


def dominant(px, box, skip=()):
    c = Counter()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            v = px[x, y]
            if hx(v) not in skip:
                c[v] += 1
    return hx(c.most_common(1)[0][0]) if c else None


def row(px, x0, x1, y):
    return [hx(px[x, y]) for x in range(x0, x1)]


def col(px, x, y0, y1):
    return [hx(px[x, y]) for y in range(y0, y1)]


def text_colour(px, box, bg):
    """La couleur du texte dans une zone : la plus fréquente qui n'est ni le fond ni le noir du contour des glyphes."""
    c = Counter()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            v = hx(px[x, y])
            if v != bg:
                c[v] += 1
    return c.most_common(1)[0][0] if c else None


def bevel(seq):
    """Dans une suite de pixels qui traverse une arête de bouton de gauche à droite : [contour, clair 1, clair 2] à gauche, [sombre 2, sombre 1, contour] à droite."""
    i = next((k for k, c in enumerate(seq) if c == "#000000"), None)
    if i is None:
        return None
    return seq[i:i + 3]


def measure(im, origins=None):
    """Toutes les mesures d'une capture. `origins` : les coins des fenêtres s'ils sont connus (la maquette de tools/kdx-compare.py), sinon ils sont cherchés."""
    px = im.load()
    w, h = im.size
    o = dict(origins) if origins else {k: find_window(px, w, h, b) for k, b in WINDOWS.items()}
    missing = [k for k, v in o.items() if v is None]
    if missing:
        raise SystemExit("fenêtre(s) introuvable(s) : " + ", ".join(missing))
    sx, sy = o["settings"]
    cx, cy = o["connect"]
    hx_, hy = o["chat"]
    ax, ay = o["addressbook"]
    mx, my = o["menu"]
    m = {}
    # --- fenêtre active (Settings) : titre, anneau, panneau
    m["title_active"] = col(px, sx + 60, sy + 1, sy + 21)                  # 20 lignes : 1 filet clair, 18 de dégradé, 1 filet sombre (loin du texte)
    m["title_button_active"] = row(px, sx + 1, sx + 20, sy + 10)           # bouton « fermer » : contour, arête claire, fond, glyphe…
    m["ring_active"] = row(px, sx, sx + 7, sy + 150)                      # contour, 5 lignes d'anneau, contour intérieur
    m["panel"] = dominant(px, (sx + 60, sy + 300, sx + 400, sy + 340))
    m["title_text"] = text_colour(px, (sx + 170, sy + 5, sx + 290, sy + 17), None)
    m["title_text_candidates"] = Counter(hx(px[x, y]) for y in range(sy + 5, sy + 17) for x in range(sx + 170, sx + 290)).most_common(4)
    # boutons Cancel / Apply / Save de Settings (y = milieu du bouton). Cancel : x ≈ +200..+280 ; l'arête gauche vers +203.
    yb = sy + 39
    m["button_row"] = row(px, sx + 196, sx + 216, yb)                      # arête gauche de Cancel : contour, clair 1, clair 2, face…
    m["button_row_right"] = row(px, sx + 268, sx + 288, yb)                # arête droite : face…, sombre 2, sombre 1, contour
    m["button_face"] = dominant(px, (sx + 215, yb - 3, sx + 240, yb + 3), skip=())
    m["button_text"] = text_colour(px, (sx + 212, yb - 6, sx + 270, yb + 6), m["button_face"])
    m["save_ring"] = row(px, sx + 348, sx + 372, yb)                       # anneau du bouton par défaut (Save) : panneau, contour, clair, sombre, contour, face
    m["label_text"] = text_colour(px, (sx + 16, sy + 80, sx + 110, sy + 92), m["panel"])   # « Appearance: »
    m["checkbox_row"] = row(px, sx + 16, sx + 34, sy + 123)                # case à cocher vide : contour, relief, face
    m["separator_col"] = col(px, sx + 200, sy + 50, sy + 60)              # filet gravé sous la rangée de boutons
    # --- fenêtre inactive (Connect) : titre, anneau, champ, liste déroulante, libellé, boutons
    m["title_inactive"] = col(px, cx + 60, cy + 1, cy + 21)
    m["title_button_inactive"] = row(px, cx + 1, cx + 20, cy + 10)
    grad = set(m["title_inactive"])
    m["tb_text"] = next((c for c, _ in Counter(hx(px[x, y]) for y in range(cy + 6, cy + 15) for x in range(cx + 150, cx + 200)).most_common() if c not in grad), None)
    m["ring_inactive"] = row(px, cx, cx + 7, cy + 120)
    m["field"] = dominant(px, (cx + 120, cy + 62, cx + 370, cy + 76))
    m["field_edge"] = row(px, cx + 100, cx + 112, cy + 69)                 # panneau…, arêtes creuses, fond du champ
    m["field_edge_right"] = row(px, cx + 375, cx + 388, cy + 69)
    m["dropdown_face"] = dominant(px, (cx + 120, cy + 36, cx + 200, cy + 46))
    m["dropdown_text"] = text_colour(px, (cx + 120, cy + 34, cx + 180, cy + 46), m["dropdown_face"])
    m["panel_text"] = text_colour(px, (cx + 14, cy + 62, cx + 70, cy + 76), m["panel"])   # « Name: »
    m["cancel_face"] = dominant(px, (cx + 160, cy + 186, cx + 230, cy + 196))
    m["connect_ring"] = row(px, cx + 258, cx + 280, cy + 191)
    m["grip"] = Counter(hx(px[x, y]) for y in range(cy + 203, cy + 215) for x in range(cx + 384, cx + 398)).most_common(4)
    # --- Address Book : en-tête, colonnes, barre de défilement, ligne
    m["header_face"] = dominant(px, (ax + 10, ay + 26, ax + 190, ay + 36))
    m["header_text"] = text_colour(px, (ax + 10, ay + 24, ax + 60, ay + 38), m["header_face"])
    m["col_a"] = dominant(px, (ax + 10, ay + 80, ax + 190, ay + 180))
    m["col_b"] = dominant(px, (ax + 215, ay + 80, ax + 290, ay + 180))
    m["row_text"] = text_colour(px, (ax + 10, ay + 43, ax + 100, ay + 55), m["col_a"])     # « stickytack »
    m["sb_track_col"] = col(px, ax + 304, ay + 70, ay + 120)
    m["sb_track"] = dominant(px, (ax + 300, ay + 100, ax + 312, ay + 160))
    m["sb_button_row"] = row(px, ax + 296, ax + 316, ay + 45)             # bouton de flèche du haut : arêtes et fond
    m["sb_button_face"] = dominant(px, (ax + 305, ay + 42, ax + 316, ay + 45))                 # le fond du bouton de flèche du haut
    m["sb_arrow"] = Counter(hx(px[x, y]) for y in range(ay + 45, ay + 50) for x in range(ax + 305, ax + 316)).most_common(4)   # les 4 lignes du triangle
    m["hsb_thumb"] = Counter(hx(px[x, y]) for y in range(ay + 204, ay + 212) for x in range(ax + 70, ax + 115)).most_common(4)
    # --- Chat : bouton enclenché « Chat List »
    m["hl_face"] = dominant(px, (hx_ + 12, hy + 28, hx_ + 110, hy + 40), skip=())
    m["hl_counts"] = Counter(hx(px[x, y]) for y in range(hy + 26, hy + 42) for x in range(hx_ + 10, hx_ + 112)).most_common(5)
    m["hl_text"] = text_colour(px, (hx_ + 40, hy + 29, hx_ + 108, hy + 41), m["hl_face"])
    # --- menu principal : pile de boutons, compteurs
    m["stack_face"] = dominant(px, (mx + 90, my + 86, mx + 160, my + 96))
    m["stack_text"] = text_colour(px, (mx + 60, my + 76, mx + 130, my + 84), m["stack_face"])   # le texte du premier bouton, à droite de son icône (contour noir)
    m["stack_row"] = row(px, mx + 8, mx + 22, my + 90)
    m["counter_text"] = text_colour(px, (mx + 36, my + 292, mx + 60, my + 304), m["panel"])
    m["origins"] = o
    return m


def crops(im, o, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    for k, (x, y) in o.items():
        cw, ch = SIZES[k]
        im.crop((x, y, x + cw, y + ch)).save(outdir / f"{k}.png", optimize=True)


def main(argv):
    if not argv or argv[0].startswith("--"):
        sys.exit(__doc__)
    folder = Path(argv[0])
    check = "--check" in argv
    files = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".png" and p.name.lower().startswith("capture"))
    if len(files) != len(APPEARANCES):
        sys.exit(f"{len(files)} capture(s) trouvée(s), {len(APPEARANCES)} attendues (une par apparence, dans l'ordre de la liste de KDX)")
    ref = {"_note": "Mesures brutes des apparences de KDX 1.6 (gen/kdx_reference.py). tokens.json en est la lecture : ne pas copier sans comprendre.",
           "appearances": {}}
    for f, (tid, kdx, fr) in zip(files, APPEARANCES):
        im = Image.open(f).convert("RGB")
        m = measure(im)
        o = m.pop("origins")
        ref["appearances"][tid] = {"kdx": kdx, "nom": fr, "capture": f.name, **m}
        if not check:
            crops(im, o, OUT / tid)
        if "--dump" in argv and (len(argv) < 3 or tid in argv):
            for k, v in m.items():
                print(f"   {k}: {v}")
        print(f"{tid:12} {kdx:28} panneau {m['panel']} bouton {m['button_face']} texte {m['panel_text']} champ {m['field']} "
              f"colonnes {m['col_a']}/{m['col_b']} titre {m['title_active'][1]}->{m['title_active'][-2]} inactif {m['title_inactive'][1]}->{m['title_inactive'][-2]}")
    text = json.dumps(ref, indent=1, ensure_ascii=False) + "\n"
    target = OUT / "kdx.json"
    if check:
        cur = target.read_text(encoding="utf-8") if target.exists() else None
        print("à jour" if cur == text else "PÉRIMÉ : kdx-reference/kdx.json")
        return 0 if cur == text else 1
    OUT.mkdir(exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    print("écrit :", target.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
