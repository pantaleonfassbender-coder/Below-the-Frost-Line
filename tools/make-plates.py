"""Lädt und skaliert (Below the Frost Line) die Tafeln nach assets/plates/<id>.jpg (1400 px) und <id>_t.jpg (Vorschau).

    python tools/make-plates.py              # alle Tafeln
    python tools/make-plates.py gillmore1880_map

Quellen: "ia" = Seitenbild des Internet Archive mit Ausschnitt in Promille (x0, y0, x1, y1);
"commons" = Datei auf Wikimedia Commons (2400 px; "commonsfull" in voller Größe); "ufdc" = Seitenbild (JPEG 2000) der University of Florida Digital Collections; "local" = Datei im Ordner ../quellen (etwa von Florida Memory,
dessen Seiten keine automatischen Abrufe zulassen und die deshalb von Hand geladen werden); "pdf" = Seite eines
lokalen PDF ("pfad::seite", 1-basiert, mit PyMuPDF bei 200 dpi gerendert), etwa Bände des Congressional Serial Set
von govinfo.gov oder Ausgaben-PDFs der University of Florida.
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "plates"
UA = {"User-Agent": "BelowTheFrostLineResearch/1.0 (pantaleonfassbender@gmail.com)"}
IAP = "https://archive.org/download/{}/page/n{}.jpg"

Q = "../quellen/"
M1 = Q + "m1/"

PLATES = {
    # filled module by module: id -> (kind, source, crop in per mille [, rotation])
    # Modul 1: The prospectus and the colony
    "econ1884_head": ("ia", IAP.format("sim_economist_1884-10-25_42_2148", 28), (70, 95, 590, 305)),
    "econ1884_frostline": ("ia", IAP.format("sim_economist_1884-10-25_42_2148", 28), (70, 440, 590, 500)),
    "bacon1886_p64": ("pdf", M1 + "bacon_22fla51.pdf::14", (60, 40, 960, 960)),
    "pens1885_victory": ("local", M1 + "pens1885_victory.png", None),   # S. 4, Spalte 2 unten + Spalte 3 oben, nebeneinander
    "grismer1946_bidwell": ("ia", IAP.format("storyofsarasotah00gris", 82), (30, 470, 980, 1000)),
    "atl1885_greer": ("local", M1 + "atl1885_greer.png", None),
    "trib1886_tait": ("local", M1 + "trib1886_tait.png", None),
    "grismer1946_whitaker": ("ia", IAP.format("storyofsarasotah00gris", 46), (30, 430, 980, 960)),
    "gaz1886_sarasota": ("local", M1 + "gaz1886_sarasota.png", None),
    "time1887_notorious": ("local", M1 + "time1887_notorious.png", None),
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()


def commons(title, full=False):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 2400, "format": "json"})
    ii = next(iter(json.loads(fetch(u))["query"]["pages"].values()))["imageinfo"][0]
    return Image.open(io.BytesIO(fetch(ii["url"] if full else (ii.get("thumburl") or ii["url"]))))


def save(pid, im):
    im = im.convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    DEST.mkdir(parents=True, exist_ok=True)
    im.save(DEST / f"{pid}.jpg", quality=86)
    t = im.copy()
    t.thumbnail((420, 420))
    t.save(DEST / f"{pid}_t.jpg", quality=82)
    print(pid, im.size)


def main(ids):
    for pid in ids or PLATES:
        kind, src, arg = PLATES[pid]
        if kind == "local":
            path = ROOT / src
            if not path.exists():
                print(pid, "fehlt noch:", path)
                continue
            im = Image.open(path)
        elif kind == "pdf":
            import pymupdf
            path, page = src.rsplit("::", 1)
            pix = pymupdf.open(ROOT / path)[int(page) - 1].get_pixmap(dpi=200)
            im = Image.open(io.BytesIO(pix.tobytes("png")))
        elif kind == "ufdc":
            b, v, f = src.split("/")
            im = Image.open(io.BytesIO(fetch("https://ufdcimages.uflib.ufl.edu/" + "/".join(b[i:i + 2] for i in range(0, 10, 2)) + f"/{v}/{f}")))
        elif kind in ("commons", "commonsfull"):
            im = commons(src, kind == "commonsfull")
        else:
            im = Image.open(io.BytesIO(fetch(src)))
        if arg:
            if len(arg) == 5:
                im = im.rotate(arg[4], expand=True)
            w, h = im.size
            x0, y0, x1, y1 = arg[:4]
            im = im.crop((w * x0 // 1000, h * y0 // 1000, w * x1 // 1000, h * y1 // 1000))
        save(pid, im)


if __name__ == "__main__":
    main(sys.argv[1:])
