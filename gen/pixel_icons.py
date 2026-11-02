"""Pixel-art icon set (16x16, black outline, flat colours) of the KDX-style UI.

The drawing engine is pixel_engine.py (shared with AudioLinker), here are the icons of an IRC client.
Each icon is drawn from a few primitives, outlined automatically and exported
as a compact SVG (one <path> per colour). Imported by gen_assets.py, which
writes them into ui/icons.js (and the application icon).
"""
import math

from pixel_engine import ACCENT_FILL, C, PAL  # noqa: F401


def server():
    """A globe: blue ball, green continents, white glint."""
    c = C()
    c.circ(7.5, 7.5, 7, 'B')
    c.pat(3, 3, ['.LLL.', 'LLLL.', '.LL..', '..L..'])
    c.pat(9, 6, ['.LL.', 'LLLL', '.LL.'])
    c.pat(5, 11, ['.LLL'])
    for y in range(16):
        for x in range(16):
            if math.hypot(x - 7.5, y - 7.5) > 5.8 and (x + y) > 15:
                if (x, y) in c.p:
                    c.p[(x, y)] = 'N'
    c.set(4, 3, 'b'); c.set(5, 2, 'b'); c.set(3, 4, 'b')
    return c.outline()


def channel():
    """A hash sign on a coloured tile."""
    c = C()
    c.rect(1, 1, 14, 14, 'N'); c.rect(1, 1, 14, 1, 'B'); c.rect(1, 1, 1, 14, 'B')
    c.rect(5, 3, 6, 12, 'w'); c.rect(9, 3, 10, 12, 'w')
    c.rect(3, 6, 12, 7, 'w'); c.rect(3, 9, 12, 10, 'w')
    return c.outline()


def users():
    """Two heads and shoulders."""
    c = C()
    c.circ(10.2, 4.8, 2.6, 'O'); c.rect(7, 8, 14, 14, 'y'); c.rect(8, 8, 13, 9, 'o')
    c.circ(5.2, 5.6, 2.9, 'Y'); c.rect(1, 9, 9, 14, 'R'); c.rect(2, 9, 8, 10, 'r')
    c.set(4, 5, 'W'); c.set(5, 4, 'W')
    return c.outline()


def bubble():
    """A speech bubble with three dots."""
    c = C()
    c.rect(1, 2, 14, 10, 'w'); c.rect(1, 2, 14, 2, 'W'); c.rect(14, 3, 14, 10, 'g'); c.rect(1, 10, 14, 10, 'g')
    c.rect(3, 11, 6, 11, 'g'); c.rect(3, 12, 4, 12, 'g'); c.set(3, 13, 'g')
    for x in (4, 7, 10):
        c.rect(x, 5, x + 1, 6, 'R')
    return c.outline()


def book():
    """The address book: red cover, page edge, a tab."""
    c = C()
    c.rect(2, 0, 13, 14, 'R'); c.rect(2, 0, 2, 14, 'r'); c.rect(13, 1, 13, 14, 'r'); c.rect(2, 14, 13, 14, 'r')
    c.rect(4, 2, 11, 12, 'W'); c.rect(4, 2, 4, 12, 'g')
    c.rect(6, 4, 10, 4, 'd'); c.rect(6, 6, 10, 6, 'd'); c.rect(6, 8, 9, 8, 'd'); c.rect(6, 10, 10, 10, 'd')
    c.rect(14, 3, 15, 5, 'Y'); c.rect(14, 8, 15, 10, 'O')
    return c.outline()


def terminal():
    """Console screen: black, green prompt."""
    c = C()
    c.rect(0, 1, 15, 14, 'g'); c.rect(0, 13, 15, 14, 'G')
    c.rect(2, 3, 13, 11, 'K'); c.rect(2, 3, 13, 3, 'D')
    c.line(3, 5, 5, 7, 'L'); c.line(5, 7, 3, 9, 'L'); c.rect(7, 9, 10, 9, 'L')
    return c.outline()


def plug():
    """A plug: connect."""
    c = C()
    c.rect(3, 0, 3, 4, 'g'); c.rect(8, 0, 8, 4, 'g')
    c.rect(1, 5, 10, 9, 'G'); c.rect(1, 5, 10, 5, 'g'); c.rect(1, 9, 10, 9, 'd')
    c.rect(4, 10, 7, 11, 'd'); c.rect(5, 12, 6, 15, 'D')
    c.rect(11, 6, 14, 8, 'L'); c.set(14, 7, 'l')
    return c.outline()


def unplug():
    """A plug broken in two halves: disconnect."""
    c = C()
    c.rect(1, 1, 1, 4, 'g'); c.rect(5, 1, 5, 4, 'g')
    c.rect(0, 5, 6, 8, 'G'); c.rect(0, 5, 6, 5, 'g'); c.rect(2, 9, 4, 10, 'd')
    c.rect(9, 7, 15, 9, 'G'); c.rect(9, 7, 15, 7, 'g'); c.rect(10, 10, 11, 12, 'd')
    c.line(7, 12, 9, 14, 'R'); c.line(8, 12, 10, 14, 'R')
    return c.outline()


def door():
    """Quit: an open door."""
    c = C()
    c.rect(2, 1, 9, 14, 'o'); c.rect(2, 1, 2, 14, 'O'); c.rect(3, 2, 8, 13, 'y')
    c.rect(4, 3, 7, 6, 'o'); c.rect(4, 8, 7, 12, 'o'); c.set(7, 8, 'Y')
    c.rect(10, 6, 14, 8, 'R'); c.set(13, 5, 'R'); c.set(13, 9, 'R'); c.set(12, 4, 'R'); c.set(12, 10, 'R')
    return c.outline()


def info():
    """About: a blue disc with an 'i'."""
    c = C()
    c.circ(7.5, 7.5, 7, 'B'); c.circ(7.5, 7.5, 6, 'B')
    c.rect(7, 3, 8, 4, 'w'); c.rect(6, 6, 8, 6, 'w'); c.rect(7, 7, 8, 11, 'w'); c.rect(6, 11, 9, 11, 'w')
    c.set(4, 4, 'b'); c.set(5, 3, 'b')
    return c.outline()


def gear():
    c = C()
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            r = math.hypot(dx, dy)
            a = math.degrees(math.atan2(dy, dx)) % 45
            tooth = r <= 7.4 and (a <= 14 or a >= 31)
            if r <= 5.4 or tooth:
                c.set(x, y, 'Y' if (x + y) < 15 else 'O')
            if r <= 2.4:
                c.p.pop((x, y), None)
    return c.outline()


def key():
    """Authentication: a key."""
    c = C()
    c.circ(4.5, 4.5, 3.6, 'Y'); c.circ(4.5, 4.5, 1.4, 'K')
    c.rect(7, 7, 14, 8, 'Y'); c.rect(7, 7, 14, 7, 'W'); c.rect(11, 9, 12, 11, 'y'); c.rect(14, 9, 14, 12, 'y')
    return c.outline()


def moon():
    """Away: a crescent."""
    c = C()
    c.circ(7.5, 7.5, 6.5, 'Y')
    c.circ(10.5, 5.5, 5.2, 'K')
    for k in list(c.p):
        if c.p[k] == 'K':
            del c.p[k]
    c.set(3, 5, 'W'); c.set(2, 7, 'W'); c.set(3, 9, 'W'); c.set(4, 11, 'W')
    return c.outline()


def journal():
    c = C()
    c.rect(3, 0, 12, 14, 'w')
    for x, y in ((10, 0), (11, 0), (12, 0), (11, 1), (12, 1), (12, 2)):
        c.p.pop((x, y), None)
    c.rect(9, 1, 10, 3, 'g'); c.rect(11, 3, 12, 3, 'g')
    c.rect(4, 5, 10, 5, 'd'); c.rect(4, 7, 11, 7, 'd'); c.rect(4, 9, 9, 9, 'd'); c.rect(4, 11, 11, 11, 'd')
    c.rect(12, 4, 12, 14, 'g'); c.rect(3, 14, 12, 14, 'G')
    return c.outline()


def bell():
    """Notifications."""
    c = C()
    c.rect(7, 0, 8, 1, 'y')
    c.rect(5, 2, 10, 3, 'Y'); c.rect(4, 4, 11, 8, 'Y'); c.rect(3, 9, 12, 11, 'Y'); c.rect(1, 11, 14, 12, 'Y')
    c.rect(5, 3, 5, 9, 'W'); c.rect(11, 5, 11, 11, 'y'); c.rect(1, 12, 14, 12, 'y')
    c.rect(6, 13, 9, 14, 'o')
    return c.outline()


def pencil():
    """Edit."""
    c = C()
    c.line(2, 13, 11, 4, 'Y'); c.line(3, 13, 12, 4, 'Y'); c.line(2, 12, 11, 3, 'y'); c.line(4, 13, 13, 4, 'y')
    c.rect(12, 2, 14, 4, 'R'); c.set(11, 4, 'R'); c.set(13, 5, 'r')
    c.set(1, 14, 'K'); c.set(2, 14, 'd'); c.set(1, 13, 'd'); c.set(2, 13, 'W')
    return c.outline()


def trash():
    """Delete."""
    c = C()
    c.rect(2, 2, 13, 3, 'g'); c.rect(6, 0, 9, 1, 'G')
    c.rect(3, 4, 12, 14, 'g'); c.rect(3, 4, 3, 14, 'w'); c.rect(12, 5, 12, 14, 'G'); c.rect(3, 14, 12, 14, 'G')
    for x in (5, 8, 10):
        c.rect(x, 6, x, 12, 'd')
    return c.outline()


def listing():
    """The channel list: a sheet with ruled rows and a hash on each."""
    c = C()
    c.rect(2, 0, 13, 14, 'w'); c.rect(13, 1, 13, 14, 'g'); c.rect(2, 14, 13, 14, 'G'); c.rect(2, 0, 2, 14, 'W')
    for y in (2, 6, 10):
        c.rect(4, y, 5, y + 2, 'B'); c.set(4, y + 1, 'b'); c.rect(7, y + 1, 11, y + 1, 'd')
    return c.outline()


def messages_app():
    """The application icon: a red chat bubble holding a hash sign."""
    c = C()
    c.rect(1, 1, 14, 11, 'R'); c.rect(1, 1, 14, 1, 'O'); c.rect(1, 1, 1, 11, 'O')
    c.rect(14, 2, 14, 11, 'r'); c.rect(2, 11, 14, 11, 'r')
    c.rect(3, 12, 6, 12, 'r'); c.rect(3, 13, 4, 13, 'r'); c.set(3, 14, 'r')
    c.rect(5, 3, 5, 9, 'w'); c.rect(9, 3, 9, 9, 'w'); c.rect(3, 5, 12, 5, 'w'); c.rect(3, 7, 12, 7, 'w')
    return c.outline()


# ---- Icônes du système (maquette Windows) : dossiers, disques, réseau, état -------------------------------------------

def folder():
    """A manila folder with its tab."""
    c = C()
    c.rect(1, 2, 6, 4, 'y'); c.rect(1, 3, 14, 13, 'y')
    c.rect(1, 5, 14, 13, 'Y'); c.rect(1, 5, 14, 5, 'W'); c.rect(1, 13, 14, 13, 'o'); c.rect(14, 6, 14, 13, 'y')
    return c.outline()


def sheet():
    """A plain document: white page, folded corner, ruled lines."""
    c = C()
    c.rect(3, 1, 12, 14, 'w'); c.rect(3, 1, 3, 14, 'W'); c.rect(12, 5, 12, 14, 'g'); c.rect(3, 14, 12, 14, 'G')
    for a in range(4):
        for b in range(4):
            if a > b:
                c.p.pop((9 + a, 1 + b), None)
            else:
                c.set(9 + a, 1 + b, 'G' if a == b else 'g')
    for y in (6, 8, 10, 12):
        c.rect(5, y, 10, y, 'G')
    return c.outline()


def picture():
    """A framed picture: sky, sun, green hills."""
    c = C()
    c.rect(0, 2, 15, 13, 'w'); c.rect(0, 13, 15, 13, 'g')
    c.rect(2, 4, 13, 11, 'b'); c.rect(10, 5, 11, 6, 'Y')
    c.rect(2, 10, 13, 11, 'L'); c.rect(2, 11, 13, 11, 'l')
    c.rect(2, 9, 7, 9, 'L'); c.rect(3, 8, 5, 8, 'L'); c.rect(9, 9, 13, 9, 'L'); c.rect(11, 8, 12, 8, 'L')
    return c.outline()


def drive():
    """A hard drive: grey case, activity light."""
    c = C()
    c.rect(0, 4, 15, 12, 'g'); c.rect(0, 4, 15, 4, 'w'); c.rect(0, 12, 15, 12, 'G'); c.rect(15, 5, 15, 12, 'G')
    c.rect(2, 7, 8, 8, 'D'); c.rect(11, 7, 13, 8, 'l'); c.rect(12, 7, 12, 8, 'L')
    return c.outline()


def computer():
    """A monitor on its stand."""
    c = C()
    c.rect(1, 0, 14, 10, 'g'); c.rect(1, 0, 14, 0, 'w'); c.rect(1, 10, 14, 10, 'G')
    c.rect(3, 2, 12, 8, 'B'); c.rect(3, 2, 12, 2, 'b'); c.rect(4, 3, 6, 3, 'b')
    c.rect(6, 11, 9, 12, 'G'); c.rect(3, 13, 12, 14, 'g'); c.rect(3, 14, 12, 14, 'G')
    return c.outline()


def wifi():
    """Three arcs and a dot."""
    c = C()
    for r_in, r_out in ((8.5, 11), (5.5, 7.5), (2.5, 4.5)):
        for y in range(16):
            for x in range(16):
                dx, dy = x - 7.5, 13 - y
                if r_in <= math.hypot(dx, dy) < r_out and dy >= abs(dx) * 0.8:
                    c.set(x, y, 'B')
    c.rect(7, 12, 8, 13, 'B')
    return c.outline()


def speaker():
    """A loudspeaker with two sound bars."""
    c = C()
    c.rect(1, 5, 3, 10, 'g'); c.rect(1, 5, 3, 5, 'w'); c.rect(4, 4, 5, 11, 'g'); c.rect(6, 2, 7, 13, 'G'); c.rect(4, 4, 4, 4, 'w')
    c.rect(10, 5, 10, 10, 'B'); c.rect(13, 3, 13, 12, 'B')
    return c.outline()


def magnifier():
    """Search."""
    c = C()
    c.circ(6, 6, 5.2, 'd'); c.circ(6, 6, 3.4, 'b'); c.set(4, 4, 'w'); c.set(5, 4, 'w'); c.set(4, 5, 'w')
    c.line(10, 10, 14, 14, 'O'); c.line(11, 10, 14, 13, 'O'); c.line(10, 11, 13, 14, 'o')
    return c.outline()


def panes():
    """Start: four red panes."""
    c = C()
    for x0, y0 in ((1, 1), (9, 1), (1, 9), (9, 9)):
        c.rect(x0, y0, x0 + 5, y0 + 5, 'R'); c.rect(x0, y0, x0 + 5, y0, 'O'); c.rect(x0, y0, x0, y0 + 5, 'O')
        c.rect(x0 + 5, y0 + 1, x0 + 5, y0 + 5, 'r'); c.rect(x0 + 1, y0 + 5, x0 + 5, y0 + 5, 'r')
    return c.outline()


def note():
    """Music: two joined eighth notes."""
    c = C()
    c.rect(5, 1, 13, 3, 'D'); c.rect(5, 1, 13, 1, 'd'); c.rect(5, 3, 5, 11, 'D'); c.rect(13, 3, 13, 10, 'D')
    c.circ(3, 12, 2.2, 'B'); c.circ(11, 11, 2.2, 'B')
    return c.outline()


def film():
    """Video: a film strip with a play triangle."""
    c = C()
    c.rect(1, 2, 14, 13, 'D')
    for y in (3, 5, 7, 9, 11):
        c.rect(2, y, 3, y, 'w'); c.rect(12, y, 13, y, 'w')
    c.rect(5, 3, 10, 12, 'B'); c.rect(5, 3, 10, 3, 'b')
    c.pat(7, 5, ['w..', 'ww.', 'www', 'ww.', 'w..'])
    return c.outline()


def download():
    """Downloads: a green arrow into a tray."""
    c = C()
    c.rect(6, 0, 9, 4, 'L'); c.rect(6, 0, 6, 4, 'l')
    for i, (x0, x1) in enumerate(((3, 12), (4, 11), (5, 10), (6, 9))):
        c.rect(x0, 5 + i, x1, 5 + i, 'L')
    c.rect(1, 11, 2, 14, 'g'); c.rect(13, 11, 14, 14, 'g'); c.rect(1, 13, 14, 14, 'g'); c.rect(1, 14, 14, 14, 'G')
    return c.outline()


def shield():
    """Security: a blue shield with a tick."""
    c = C()
    rows = {1: (2, 13), 2: (2, 13), 3: (2, 13), 4: (2, 13), 5: (2, 13), 6: (2, 13), 7: (2, 13), 8: (3, 12), 9: (3, 12),
            10: (4, 11), 11: (5, 10), 12: (6, 9), 13: (7, 8)}
    for y, (a, b) in rows.items():
        c.rect(a, y, 7, y, 'B'); c.rect(8, y, b, y, 'N')
    c.rect(2, 1, 13, 1, 'b')
    c.line(5, 7, 7, 9, 'w'); c.line(5, 8, 7, 10, 'w'); c.line(7, 9, 11, 4, 'w'); c.line(7, 10, 11, 5, 'w')
    return c.outline()


def clock():
    """Time: a white dial, a dark minute hand, a red hour hand."""
    c = C()
    c.circ(7.5, 7.5, 7.2, 'D'); c.circ(7.5, 7.5, 6, 'w')
    c.rect(7, 3, 8, 8, 'D'); c.rect(9, 7, 11, 8, 'R')
    return c.outline()


def person():
    """Account: head and shoulders."""
    c = C()
    c.circ(7.5, 4.5, 3.4, 'Y')
    c.rect(4, 9, 11, 9, 'B'); c.rect(3, 10, 12, 10, 'B'); c.rect(2, 11, 13, 14, 'B'); c.rect(2, 11, 2, 14, 'b'); c.rect(3, 10, 3, 10, 'b')
    return c.outline()


def palette():
    """Personalisation: a painter's palette."""
    c = C()
    c.circ(7.5, 8, 7, 'Y')
    c.rect(4, 4, 5, 5, 'R'); c.rect(8, 3, 9, 4, 'B'); c.rect(11, 6, 12, 7, 'L'); c.rect(3, 9, 4, 10, 'P')
    c.circ(10.5, 11.5, 1.8, 'K')
    return c.outline()


def apps():
    """Applications: a 3 x 3 grid of coloured squares."""
    c = C()
    for i, col in enumerate('ROYLBbPpg'):
        x, y = 1 + (i % 3) * 5, 1 + (i // 3) * 5
        c.rect(x, y, x + 3, y + 3, col)
    return c.outline()


def refresh():
    """Update: a green circular arrow."""
    c = C()
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 7.5)
            if 4 <= d <= 6.6 and not (-80 < math.degrees(math.atan2(y - 7.5, x - 7.5)) < -15):
                c.set(x, y, 'L')
    c.rect(9, 1, 14, 1, 'L'); c.rect(10, 2, 14, 2, 'L'); c.rect(11, 3, 14, 3, 'L'); c.rect(12, 4, 14, 4, 'L'); c.rect(13, 5, 14, 5, 'L')
    return c.outline()


def warning():
    """Attention: an amber triangle with an exclamation mark."""
    c = C()
    for y in range(1, 14):
        h = int(y * 0.6)
        c.rect(7 - h, y, 8 + h, y, 'Y')
    c.rect(0, 13, 15, 13, 'y'); c.rect(7, 5, 8, 9, 'D'); c.rect(7, 11, 8, 12, 'D')
    return c.outline()


def failure():
    """Error: a red disc crossed by a white X."""
    c = C()
    c.circ(7.5, 7.5, 7.2, 'E')
    for y in range(16):
        for x in range(16):
            if (x, y) in c.p and (x - 7.5) + (y - 7.5) > 6:
                c.set(x, y, 'e')
    for dx in (0, 1):
        c.line(4 + dx, 5, 10 + dx, 11, 'w'); c.line(10 + dx, 5, 4 + dx, 11, 'w')
    return c.outline()


def padlock():
    """Locked: a steel shackle on a yellow body."""
    c = C()
    c.rect(4, 1, 11, 7, 'G')
    for y in range(3, 8):
        for x in range(6, 10):
            c.p.pop((x, y), None)
    c.rect(2, 7, 13, 14, 'Y'); c.rect(2, 7, 13, 7, 'W'); c.rect(13, 8, 13, 14, 'y'); c.rect(2, 14, 13, 14, 'y')
    c.rect(7, 10, 8, 12, 'D')
    return c.outline()


def chip():
    """Processor: a dark chip with pins."""
    c = C()
    for i in (4, 7, 10):
        c.rect(i, 1, i, 3, 'G'); c.rect(i, 12, i, 14, 'G'); c.rect(1, i, 3, i, 'G'); c.rect(12, i, 14, i, 'G')
    c.rect(3, 3, 12, 12, 'D'); c.rect(5, 5, 10, 10, 'G'); c.rect(6, 6, 9, 9, 'L')
    return c.outline()


ICONS = dict(serveur=server, salon=channel, membres=users, message=bubble, carnet=book, console=terminal,
             connecter=plug, deconnecter=unplug, quitter=door, info=info, reglages=gear, cle=key, absent=moon,
             journal=journal, messages=messages_app, liste=listing, cloche=bell, editer=pencil, supprimer=trash,
             dossier=folder, fichier=sheet, image=picture, disque=drive, pc=computer, wifi=wifi, volume=speaker,
             recherche=magnifier, demarrer=panes, musique=note, video=film, telecharger=download, bouclier=shield,
             horloge=clock, utilisateur=person, palette=palette, apps=apps, maj=refresh, avertissement=warning,
             erreur=failure, cadenas=padlock, processeur=chip)


# ---- Icônes d'application de la suite (01/11/2026) : une famille ------------------------------------------------------------
# Chaque application porte son objet, dans les couleurs de l'objet (choix de Valentin du 01/11/2026 : pas le même rouge partout) ; la même lumière
# que l'icône de Messages (arête claire en haut et à gauche, ombre en bas et à droite, contour noir). « cdx » est la suite elle-même (barre,
# installeur) et garde le rouge de l'accent. L'Explorateur garde le dossier jaune (« dossier »).

def _card(c, x0, y0, x1, y1, body='R', light='O', dark='r'):
    """Un corps éclairé : couleur, arête claire en haut et à gauche, ombre en bas et à droite."""
    c.rect(x0, y0, x1, y1, body); c.rect(x0, y0, x1, y0, light); c.rect(x0, y0, x0, y1, light)
    c.rect(x1, y0 + 1, x1, y1, dark); c.rect(x0 + 1, y1, x1, y1, dark)


def _ring(c, cx, cy, r_out, r_in, col):
    for y in range(16):
        for x in range(16):
            d = (x - cx) ** 2 + (y - cy) ** 2
            if r_in * r_in < d <= r_out * r_out:
                c.set(x, y, col)


def app_repos():
    """Dépôts : un classeur gris à deux tiroirs, poignées sombres (l'Explorateur garde le dossier)."""
    c = C()
    _card(c, 2, 1, 13, 14, 'g', 'w', 'G')
    c.rect(3, 7, 12, 7, 'G'); c.rect(3, 8, 12, 8, 'w')
    c.rect(6, 4, 9, 4, 'D'); c.rect(6, 11, 9, 11, 'D')
    return c.outline()


def app_browser():
    """Navigateur : le globe terrestre, océan bleu, continents verts."""
    c = C()
    c.circ(7.5, 7.5, 6.6, 'B')
    for (x, y), col in list(c.p.items()):
        d = (x - 7.5) ** 2 + (y - 7.5) ** 2
        if d > 30 and x + y > 16:
            c.set(x, y, 'N')
        elif d > 30 and x + y < 8:
            c.set(x, y, 'b')
    c.pat(2, 3, ['..LL.', '.LLLL', 'LLLLl', '.LLl.', '..Ll.'])
    c.pat(8, 6, ['LLL..', 'LLLL.', '.LLl.', '..Ll.', '..L..'])
    c.pat(5, 11, ['.LL', 'LLl'])
    return c.outline()


def app_notes():
    """Notes : un carnet à spirale, page blanche aux lignes bleues."""
    c = C()
    _card(c, 3, 1, 13, 14, 'W', 'w', 'g')
    for y in (3, 6, 9, 12):
        c.rect(2, y, 4, y, 'G'); c.set(2, y, 'd')
    c.rect(6, 4, 11, 4, 'b'); c.rect(6, 7, 11, 7, 'b'); c.rect(6, 10, 10, 10, 'b')
    return c.outline()


def app_terminal():
    """Terminal : un écran noir dans un cadre gris, invite verte."""
    c = C()
    _card(c, 1, 1, 14, 14, 'g', 'w', 'G')
    c.rect(3, 3, 12, 12, 'K'); c.rect(3, 3, 12, 3, 'D')
    c.set(5, 6, 'L'); c.set(6, 7, 'L'); c.set(5, 8, 'L'); c.rect(8, 9, 10, 9, 'L')
    return c.outline()


def app_agenda():
    """Agenda : une page de calendrier, bandeau rouge, le jour marqué."""
    c = C()
    c.rect(1, 2, 14, 14, 'W'); c.rect(1, 2, 14, 4, 'R'); c.rect(1, 2, 14, 2, 'O'); c.rect(1, 3, 1, 4, 'O'); c.rect(14, 3, 14, 4, 'r')
    c.rect(14, 5, 14, 14, 'g'); c.rect(2, 14, 14, 14, 'g')
    c.rect(4, 0, 4, 3, 'G'); c.rect(11, 0, 11, 3, 'G')
    for y in (7, 10):
        for x in (3, 6, 9, 12):
            c.set(x, y, 'G')
    c.rect(8, 9, 10, 11, 'R'); c.set(8, 9, 'O'); c.set(10, 11, 'r')
    return c.outline()


def app_mail():
    """Courrier : une enveloppe beige, le rabat marqué."""
    c = C()
    _card(c, 1, 3, 14, 12, 'W', 'w', 'g')
    c.line(1, 4, 6, 9, 'G'); c.line(14, 4, 9, 9, 'G'); c.rect(7, 9, 8, 9, 'G')
    c.line(2, 4, 6, 8, 'g'); c.line(13, 4, 9, 8, 'g')
    return c.outline()


def app_pilot():
    """Pilote : un volant noir, trois rayons gris, le klaxon rouge au centre."""
    c = C()
    _ring(c, 7.5, 7.5, 7.0, 4.9, 'd')
    for (x, y), col in list(c.p.items()):
        far = (x - 7.5) ** 2 + (y - 7.5) ** 2 > 36
        if col == 'd' and far and x + y > 16:
            c.set(x, y, 'D')
        elif col == 'd' and far and x + y < 8:
            c.set(x, y, 'G')
    c.rect(7, 3, 8, 7, 'g')
    c.line(6, 8, 3, 11, 'g'); c.line(7, 8, 4, 11, 'g'); c.line(8, 8, 11, 11, 'g'); c.line(9, 8, 12, 11, 'g')
    c.rect(6, 6, 9, 9, 'G'); c.rect(7, 7, 8, 8, 'R')
    return c.outline()


def app_transfers():
    """Transferts : deux flèches qui se croisent sur une carte blanche, verte (envoi) et bleue (réception)."""
    c = C()
    _card(c, 1, 1, 14, 14, 'W', 'w', 'g')
    c.rect(3, 5, 10, 5, 'L'); c.set(10, 4, 'L'); c.set(10, 6, 'L'); c.set(11, 5, 'L'); c.set(9, 3, 'L'); c.set(9, 7, 'L')
    c.rect(5, 10, 12, 10, 'B'); c.set(5, 9, 'B'); c.set(5, 11, 'B'); c.set(4, 10, 'B'); c.set(6, 8, 'B'); c.set(6, 12, 'B')
    return c.outline()


def app_cdx():
    """La suite : un carré rouge et son C blanc (barre, installeur)."""
    c = C()
    _card(c, 1, 1, 14, 14)
    c.rect(5, 4, 10, 5, 'W'); c.rect(4, 5, 5, 10, 'W'); c.rect(5, 10, 10, 11, 'W'); c.rect(10, 5, 11, 6, 'W'); c.rect(10, 9, 11, 10, 'W')
    return c.outline()


APPS = dict(explorateur=folder, navigateur=app_browser, depots=app_repos, notes=app_notes, terminal=app_terminal,
            agenda=app_agenda, courrier=app_mail, pilote=app_pilot, transferts=app_transfers, cdx=app_cdx)
ICONS.update(APPS)


# ---- Icônes des applications tierces de la zone de notification (02/11/2026) ------------------------------------------------
# Demande de Valentin : la barre CDX montre les icônes des autres programmes (Discord, NVIDIA, AMD…) avec nos propres pictogrammes
# pixel, rendus en un seul ton dans la case de l'heure. Dessinées ici en couleurs d'objet (lisibles aussi en couleur) ; la barre
# recolore tout ce qui n'est pas le contour noir. Une forme pleine et simple : à 16 px et en un ton, le détail ne se voit pas.

def _pat(rows, dx=0, dy=0):
    c = C(); c.pat(dx, dy, rows); return c.outline()


def tray_discord():
    """Discord : le visage de manette, deux yeux en creux."""
    return _pat(['....BBBBBBBB....', '...BBBBBBBBBB...', '..BBBBBBBBBBBB..', '..BBBBBBBBBBBB..', '..BB..BBBB..BB..', '..BB..BBBB..BB..',
                 '..BBBBBBBBBBBB..', '..BBBBBBBBBBBB..', '..BBBBBBBBBBBB..', '.BBBB......BBBB.', '.BB..........BB.'], 0, 2)


def tray_steam():
    """Steam : le piston, un anneau et son bras."""
    return _pat(['........wwww....', '.......wwwwww...', '......ww....ww..', '......w......w..', '......ww....ww..', '.......wwwwww...',
                 '......www.......', '.....www........', '...wwww.........', '..ww.ww.........', '..ww............', '...ww...........'], 0, 2)


def tray_nvidia():
    """NVIDIA : l'œil vert."""
    return _pat(['.....LLLLLL.....', '...LLL....LLL...', '.LLL...LL...LLL.', 'LL....LLLL....LL', 'LL....LLLL....LL', '.LLL...LL...LLL.',
                 '...LLL....LLL...', '.....LLLLLL.....'], 0, 4)


def tray_amd():
    """AMD : le carré à l'angle coupé et sa flèche."""
    return _pat(['..EEEEEEEEEEEE..', '...EEEEEEEEEEE..', '....EEEEEEEEEE..', '.....EE.....EE..', '......E.....EE..', '............EE..',
                 '..E.........EE..', '..EE........EE..', '..EEE.......EE..', '..EEEEEEEEEEEE..', '..EEEEEEEEEEEE..'], 0, 2)


def tray_localsend():
    """LocalSend : l'avion en papier."""
    return _pat(['..............BB', '............BBBB', '..........BBBBB.', '........BBBBBB..', '......BBBBBBB...', '....BBBBBBBB....',
                 '..BBBBBBBBB.....', 'BBBBBBBBBB......', '......BBB.......', '......BBB.......', '......BB........', '......B.........'], 0, 2)


def tray_tailscale():
    """Tailscale : la grille de neuf points."""
    return _pat(['.dd...dd...dd...', '.dd...dd...dd...', '................', '.ww...ww...ww...', '.ww...ww...ww...', '................',
                 '.ww...ww...ww...', '.ww...ww...ww...'], 1, 3)


def tray_obs():
    """OBS : l'anneau et ses trois pales."""
    c = C()
    _ring(c, 7.5, 7.5, 7.2, 5.6, 'D')
    for ax, ay in ((7, 4), (4, 10), (11, 10)):
        c.rect(ax, ay, ax + 1, ay + 1, 'w')
    c.set(8, 6, 'w'); c.set(6, 9, 'w'); c.set(10, 9, 'w')
    return c.outline()


def tray_whatsapp():
    """WhatsApp : la bulle verte et le combiné en creux."""
    return _pat(['....LLLLLLLL....', '..LLLLLLLLLLLL..', '.LLLLLLLLLLLLLL.', '.LLLL..LLLLLLLL.', 'LLLL...LLLLLLLLL', 'LLLLL...LLLLLLLL',
                 'LLLLLL...LLLLLLL', 'LLLLLLL...LLLLLL', 'LLLLLLLL...LLLLL', '.LLLLLLLL..LLLL.', '.LLLLLLLLLLLLLL.', '..L.LLLLLLLLLL..',
                 '.LL..LLLLLLLL...', 'LL..............'], 0, 1)


def tray_vlc():
    """VLC : le cône de chantier."""
    return _pat(['.......OO.......', '......OOOO......', '......OOOO......', '.....OOOOOO.....', '.....wwwwww.....', '.....wwwwww.....',
                 '....OOOOOOOO....', '....OOOOOOOO....', '...wwwwwwwwww...', '...wwwwwwwwww...', '..OOOOOOOOOOOO..', '.OOOOOOOOOOOOOO.',
                 'OOOOOOOOOOOOOOOO'], 0, 1)


def tray_epic():
    """Epic Games : l'écusson et son E."""
    return _pat(['...wwwwwwwwww...', '...w........w...', '...w.wwwwww.w...', '...w.ww.....w...', '...w.ww.....w...', '...w.wwwww..w...',
                 '...w.ww.....w...', '...w.ww.....w...', '...w.wwwwww.w...', '...w........w...', '....w......w....', '.....w....w.....',
                 '......wwww......'], 0, 1)


def tray_battlenet():
    """Battle.net : l'éclair."""
    return _pat(['.........BBB....', '........BBB.....', '.......BBB......', '......BBB.......', '.....BBBBBBB....', '....BBBBBBB.....',
                 '.......BBB......', '......BBB.......', '.....BBB........', '....BBB.........'], 0, 3)


def tray_temperature():
    """Core Temp, HWiNFO : le thermomètre."""
    return _pat(['.......ww.......', '......w..w......', '......w..w......', '......wEEw......', '......wEEw......', '......wEEw......',
                 '......wEEw......', '......wEEw......', '.....wEEEEw.....', '....wEEEEEEw....', '....wEEEEEEw....', '....wEEEEEEw....',
                 '.....wEEEEw.....', '......wwww......'], 0, 1)


def tray_telephone():
    """Mobile connecté (Phone Link) : le combiné."""
    return _pat(['..gg............', '.gggg...........', '.gggg...........', '..ggg...........', '...ggg..........', '....ggg.........',
                 '.....ggg........', '......ggg.......', '.......gggg..gg.', '........gggggggg', '.........gggggg.', '..........gggg..'], 0, 2)


def tray_camera():
    """Webcam (Iriun, DroidCam) : l'objectif sur son pied."""
    return _pat(['....gggggggg....', '..gggggggggggg..', '.ggggg....ggggg.', '.ggg..gggg..ggg.', 'gggg.gg..gg.gggg', 'ggg..g....g..ggg',
                 'ggg..g....g..ggg', 'gggg.gg..gg.gggg', '.ggg..gggg..ggg.', '.ggggg....ggggg.', '..gggggggggggg..', '......gggg......',
                 '....gggggggg....'], 0, 2)


def tray_adobe():
    """Creative Cloud : le A."""
    return _pat(['......EEEE......', '.....EEEEEE.....', '.....EE..EE.....', '....EEE..EEE....', '....EE....EE....', '...EEE....EEE...',
                 '...EEEEEEEEEE...', '..EEEEEEEEEEEE..', '..EEE......EEE..', '.EEE........EEE.', '.EE..........EE.', 'EEE..........EEE'], 0, 2)


def tray_medal():
    """Medal : la médaille et son ruban."""
    return _pat(['...BB......BB...', '....BB....BB....', '.....BB..BB.....', '......BBBB......', '.....YYYYYY.....', '....YYYYYYYY....',
                 '...YYYYYYYYYY...', '...YYYY..YYYY...', '...YYYY..YYYY...', '...YYYYYYYYYY...', '....YYYYYYYY....', '.....YYYYYY.....'], 0, 2)


def tray_ecran_distant():
    """AnyDesk, TeamViewer, Barrier : l'écran et le curseur."""
    return _pat(['gggggggggggggggg', 'g..............g', 'g..............g', 'g.....ww.......g', 'g.....www......g', 'g.....wwww.....g',
                 'g.....wwwww....g', 'g.....www......g', 'g.....w.ww.....g', 'gggggggggggggggg', '.......gg.......', '.....gggggg.....'], 0, 2)


def tray_ia():
    """LM Studio et les assistants : l'étincelle à quatre pointes."""
    return _pat(['.......PP.......', '.......PP.......', '......PPPP......', '......PPPP......', '.....PPPPPP.....', 'PPPPPPPPPPPPPPPP',
                 'PPPPPPPPPPPPPPPP', '.....PPPPPP.....', '......PPPP......', '......PPPP......', '.......PP.......', '.......PP.......'], 0, 2)


def tray_tennis():
    """Tennis (l'agent local) : la raquette et la balle."""
    return _pat(['......LLLL......', '.....L....L.....', '....L..L...L....', '....L.L.L..L....', '....L..L...L....', '.....L....L.....',
                 '......LLLL......', '.......LL.......', '.......LL.......', '.......LL.......', '......LL........', '.....LL....YY...',
                 '....LL.....YY...'], 0, 1)


def tray_appli():
    """Toute autre application : une petite fenêtre."""
    return _pat(['.gggggggggggggg.', '.gDDDDDDDDDDDDg.', '.gggggggggggggg.', '.g............g.', '.g............g.', '.g............g.',
                 '.g............g.', '.g............g.', '.g............g.', '.g............g.', '.gggggggggggggg.'], 0, 2)


TRAY = {'discord': tray_discord, 'steam': tray_steam, 'nvidia': tray_nvidia, 'amd': tray_amd, 'localsend': tray_localsend,
        'tailscale': tray_tailscale, 'obs': tray_obs, 'whatsapp': tray_whatsapp, 'vlc': tray_vlc, 'epic': tray_epic,
        'battlenet': tray_battlenet, 'temperature': tray_temperature, 'telephone': tray_telephone, 'camera': tray_camera,
        'adobe': tray_adobe, 'medal': tray_medal, 'distant': tray_ecran_distant, 'ia': tray_ia, 'tennis': tray_tennis,
        'appli': tray_appli}
ICONS.update(TRAY)


def all_svgs():
    return {name: draw().svg() for name, draw in ICONS.items()}
