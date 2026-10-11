"""Draws assets/viz/rails-acre.svg for module 3 (Rails and patrons): what an acre of land at Sarasota cost, as the
sources of modules 1–3 state it (each read against the page image): the prospectus of 1884 ($3.40), the company's
asking price after 1887 (“$10 or more”, Grismer p. 113), Mrs. Palmer's floor for resale in 1910 ($100, Manatee River
Journal 30 June 1910) and her price for the Jones home and 13 acres at Osprey ($11,000, Grismer p. 159).
Run from the site root: python tools/viz-rails.py
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
ROWS = [
    ("1884", "The Edinburgh company buys 47,000 acres", 3.40, "#/text/prospectus/prospectus/6", "var(--promise)"),
    ("after 1887", "The company asks “$10 or more” and finds no buyers", 10, "#/text/village/lean/1", "var(--town)"),
    ("1910", "Mrs. Palmer: none sold to colonists below", 100, "#/text/rails/palmer/3", "var(--promise)"),
    ("1910", "Mrs. Palmer pays for a home and 13 acres at Osprey", 11000 / 13, "#/text/rails/palmer/4", "var(--colony)"),
]


def build():
    W, H = 900, 330
    x0, x1 = 360, 870
    lo, hi = math.log10(1), math.log10(1000)
    X = lambda v: x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)
    title = "What an acre cost"
    desc = "; ".join(f"{y}: {t}, ${v:,.2f} an acre" for y, t, v, *_ in ROWS) + ". Logarithmic scale."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ra-t ra-d" font-family="var(--serif)">',
         f'<title id="ra-t">{escape(title)}</title><desc id="ra-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">Dollars per acre at Sarasota, as the sources give them; each scale step is ten times the last. Each bar links to its passage.</text>']
    for v in (1, 10, 100, 1000):
        x = X(v)
        o.append(f'<line x1="{x:.0f}" y1="64" x2="{x:.0f}" y2="270" stroke="var(--line)"/>'
                 f'<text x="{x:.0f}" y="288" font-size="12" text-anchor="middle" fill="var(--ink2)">${v:,}</text>')
    y = 76
    for yr, t, v, link, col in ROWS:
        o.append(f'<a href="{link}"><text x="16" y="{y + 15}" font-size="12.5" fill="var(--ink)" text-decoration="underline">{escape(yr)} · {escape(t)}</text></a>'
                 f'<rect x="{x0}" y="{y}" width="{X(v) - x0:.1f}" height="24" fill="{col}"/>'
                 f'<text x="{X(v) + 6:.0f}" y="{y + 17}" font-size="12.5" fill="var(--ink)">${v:,.2f}</text>')
        y += 46
    o.append('<text x="16" y="314" font-size="12" fill="var(--ink2)">Not prices paid by the same buyers for the same land: what was offered, asked and paid, by those whose words survive.</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rails-acre.svg").write_text(build(), encoding="utf-8")
    print("ok")
