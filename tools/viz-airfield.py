"""Draws assets/viz/airfield-numbers.svg for module 6 (The airfield and the book): the numbers of the war years as
Grismer gives them (The Story of Sarasota, 1946, pp. 250–252, read against the page image).
Run from the site root: python tools/viz-airfield.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
ROWS = [
    ("Winter visitors, season 1945–46", 40000, "war/4", "var(--colony)", None),
    ("Sarasota County, census 1940", 16106, "war/1", "var(--town)", None),
    ("Venice Army Air Field, top strength", 6000, "field/4", "var(--work)", None),
    ("Sarasota Army Air Base, peak", 3000, "field/2", "var(--work)", None),
    ("County men and women in service", 2285, "war/1", "var(--law)", None),
    ("Inducted by the draft", 1726, "war/1", "var(--law)", (1293, 433)),
]


def build():
    W, H = 900, 380
    x0, x1 = 300, 860
    sc = (x1 - x0) / 40000
    title = "The war years in numbers"
    desc = "; ".join(f"{t}: {v:,}" for t, v, *_ in ROWS) + ". Of those inducted, 1,293 white and 433 Black."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="an-t an-d" font-family="var(--serif)">',
         f'<title id="an-t">{escape(title)}</title><desc id="an-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">As Grismer gives them in 1946. Each label links to its passage.</text>']
    y = 70
    for t, v, link, col, split in ROWS:
        o.append(f'<a href="#/text/airfield/{link}"><text x="16" y="{y + 17}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(t)}</text></a>')
        if split:
            a, b = split
            o.append(f'<rect x="{x0}" y="{y}" width="{a * sc:.1f}" height="24" fill="{col}"/><rect x="{x0 + a * sc:.1f}" y="{y}" width="{b * sc:.1f}" height="24" fill="var(--colour)"/>'
                     f'<text x="{x0 + v * sc + 6:.0f}" y="{y + 17}" font-size="12.5" fill="var(--ink)">{v:,} — {a:,} white, {b} Black</text>')
        else:
            o.append(f'<rect x="{x0}" y="{y}" width="{v * sc:.1f}" height="24" fill="{col}"/>'
                     f'<text x="{x0 + v * sc + 6 if v < 30000 else x0 + v * sc - 6:.0f}" y="{y + 17}" font-size="12.5" text-anchor="{"start" if v < 30000 else "end"}" fill="{"var(--ink)" if v < 30000 else "var(--panel)"}">{v:,}</text>')
        y += 46
    o.append('<text x="16" y="358" font-size="12" fill="var(--ink2)">The 433 are the only place in Grismer\'s account of the war where Black Sarasotans are counted.</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "airfield-numbers.svg").write_text(build(), encoding="utf-8")
    print("ok")
