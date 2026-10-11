"""Draws assets/viz/village-ways.svg for module 2 (The village): the ways into and out of Sarasota, 1886–1903,
on one time axis, each from a passage of the module read against the page image.
Run from the site root: python tools/viz-village.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/village/"
# (year as decimal, label, link, lane, level)
EV = [
    (1886.3, "Company wharf; steamer Erie to Tampa", "build/2", 0, 0),
    (1887.15, "De Soto Hotel opens", "build/4", 2, 0),
    (1888.0, "Weeds in Main Street", "lean/1", 2, 3),
    (1889.9, "De Soto open “for the season”", "lean/2", 2, 1),
    (1892.15, "Rail from Braidentown (“Slow and Wobbly”)", "lean/3", 1, 0),
    (1894.98, "Freeze, 27 Dec.", "freeze/1", 2, 1),
    (1895.1, "Freeze, 8 Feb.: 14 degrees", "freeze/1", 2, 2),
    (1895.77, "Channel dredged; Mistletoe calls", "freeze/4", 0, 1),
    (1902.79, "Town incorporated: 53 voters", "town/2", 2, 0),
    (1903.22, "Seaboard train, 22 March", "town/1", 1, 1),
]
LANES = [("By water", "var(--colony)"), ("By rail", "var(--town)"), ("The village", "var(--promise)")]


def build():
    W, H = 920, 400
    x0, x1, a, b = 130, 890, 1885.5, 1904
    X = lambda t: x0 + (t - a) / (b - a) * (x1 - x0)
    title = "Ways in and out, 1886–1903"
    desc = "Water, rail and the village on one time line: " + "; ".join(f"{int(t)} {l}" for t, l, *_ in EV) + "."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="vw-t vw-d" font-family="var(--serif)">',
         f'<title id="vw-t">{escape(title)}</title><desc id="vw-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">How a village with no road worth the name was reached, and what happened while it waited. Each mark links to its passage.</text>']
    for yr in range(1886, 1905, 2):
        x = X(yr)
        o.append(f'<line x1="{x:.0f}" y1="70" x2="{x:.0f}" y2="360" stroke="var(--line)" stroke-dasharray="2 4"/>'
                 f'<text x="{x:.0f}" y="378" font-size="12" text-anchor="middle" fill="var(--ink2)">{yr}</text>')
    ys = [120, 210, 300]
    for i, (lab, col) in enumerate(LANES):
        o.append(f'<line x1="{x0}" y1="{ys[i]}" x2="{x1}" y2="{ys[i]}" stroke="{col}" stroke-width="2"/>'
                 f'<text x="16" y="{ys[i] + 5}" font-size="13" font-weight="bold" fill="{col}">{lab}</text>')
    for t, lab, link, lane, lvl in EV:
        x = X(t); y = ys[lane]
        ty = y - 14 - lvl * 18
        anchor = "end" if x > 700 else "start"
        col = LANES[lane][1]
        o.append(f'<circle cx="{x:.0f}" cy="{y}" r="5" fill="{col}"/><line x1="{x:.0f}" y1="{y}" x2="{x:.0f}" y2="{ty + 4}" stroke="{col}"/>'
                 f'<a href="{T}{link}"><text x="{x + (-4 if anchor == "end" else 4):.0f}" y="{ty}" font-size="12" text-anchor="{anchor}" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></a>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "village-ways.svg").write_text(build(), encoding="utf-8")
    print("ok")
