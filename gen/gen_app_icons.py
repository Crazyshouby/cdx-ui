"""Les icônes d'application de la suite CDX (pictogrammes `APPS` de pixel_icons.py) en fichiers .ico pour les exécutables et l'installeur.
    python gen/gen_app_icons.py <dossier de sortie>      (cdx-windows : icons\\<nom>.ico, versionnés ; relancé seulement si un dessin change)
Chaque .ico contient le pictogramme 16 x 16 agrandi au plus proche voisin en 16, 32, 48 et 256 px (images PNG dans l'ICO, lues par Windows
depuis Vista). Le rouge est fixe (#e02020 / #8a0202) : un fichier ne suit pas l'accent du thème.
"""
import struct
import sys
import zlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pixel_icons  # noqa: E402

SIZES = (16, 32, 48, 256)


def png_bytes(pixels, size):
    scale = size // 16
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            c = pixels.get((x // scale, y // scale))
            if c is None:
                raw += b'\0\0\0\0'
            else:
                h = pixel_icons.PAL[c].lstrip('#')
                raw += bytes(int(h[i:i + 2], 16) for i in (0, 2, 4)) + b'\xff'

    def chunk(tag, data):
        body = tag + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


def ico_bytes(pixels):
    images = [png_bytes(pixels, s) for s in SIZES]
    head = struct.pack('<HHH', 0, 1, len(images))
    offset = 6 + 16 * len(images)
    entries = b''
    for s, img in zip(SIZES, images):
        entries += struct.pack('<BBBBHHII', s % 256, s % 256, 0, 0, 1, 32, len(img), offset)
        offset += len(img)
    return head + entries + b''.join(images)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for name, draw in pixel_icons.APPS.items():
        f = out / (name + '.ico')
        f.write_bytes(ico_bytes(draw().p))
        print('écrit :', f)
