"""L'icône de KIRC (le pictogramme « kirc » de pixel_icons.py, 16 x 16 agrandi 64 fois) en PNG RGBA.

    python gen/gen_kirc_icon.py <fichier.png>      (KIRC : src-tauri/icons/source.png, entrée de `tauri icon`)

Le fichier de sortie est versionné dans l'application ; ce générateur n'est relancé que si le dessin change.
"""
import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pixel_icons  # noqa: E402


def png(path, pixels, scale):
    """Écrit l'icône 16x16 agrandie `scale` fois (plus proche voisin) en PNG RGBA."""
    size = 16 * scale
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

    data = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))
    Path(path).write_bytes(data)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    png(sys.argv[1], pixel_icons.kirc_app().p, 64)
    print('écrit :', sys.argv[1])
