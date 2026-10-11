"""Draws assets/viz/boom-promise.svg for module 4 (The county and the boom): the population of the city of Sarasota
as counted by the census in 1910, 1920 and 1930 (Fifteenth Census, Population vol. I, Florida, table 4, p. 213,
read against the page image), against the goal of a booklet of about 1924: "twenty-five thousand permanent
residents within the next five years" (p. [4], read against the page image).
Run from the site root: python tools/viz-boom.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
COUNT = [(1910, 840), (1920, 2149), (1930, 8398)]
GOAL = 25000


def build():
    W, H = 900, 380
    x0, y0, y1 = 90, 330, 80
    sc = (y0 - y1) / 26000
    title = "Promised and counted"
    desc = ("Population of the city of Sarasota by the census: 840 in 1910, 2,149 in 1920, 8,398 in 1930. "
            "A booklet of about 1924 set the goal of 25,000 permanent residents within five years.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bp-t bp-d" font-family="var(--serif)">',
         f'<title id="bp-t">{escape(title)}</title><desc id="bp-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<a href="#/text/boom/selling/3"><text x="16" y="48" font-size="13" fill="var(--ink2)" text-decoration="underline">The city of Sarasota in the census, and the goal of a booklet of about 1924. Link to the passage.</text></a>']
    for v in (0, 5000, 10000, 15000, 20000, 25000):
        y = y0 - v * sc
        o.append(f'<line x1="{x0}" y1="{y:.0f}" x2="860" y2="{y:.0f}" stroke="var(--line)"/>'
                 f'<text x="{x0 - 8}" y="{y + 4:.0f}" font-size="12" text-anchor="end" fill="var(--ink2)">{v:,}</text>')
    gy = y0 - GOAL * sc
    o.append(f'<rect x="560" y="{gy:.0f}" width="120" height="{GOAL * sc:.0f}" fill="none" stroke="var(--promise)" stroke-width="2.5" stroke-dasharray="7 5"/>'
             f'<text x="620" y="{gy - 10:.0f}" font-size="13" text-anchor="middle" fill="var(--promise)" font-weight="bold">25,000 by about 1929</text>'
             f'<text x="620" y="{gy + 22:.0f}" font-size="12" text-anchor="middle" fill="var(--promise)">the booklet’s “great goal”</text>')
    for i, (yr, n) in enumerate(COUNT):
        x = 150 + i * 205 if yr != 1930 else 580
        h = n * sc
        o.append(f'<rect x="{x}" y="{y0 - h:.1f}" width="80" height="{h:.1f}" fill="var(--town)"/>'
                 f'<text x="{x + 40}" y="{y0 - h - 8:.0f}" font-size="13" text-anchor="middle" fill="var(--ink)">{n:,}</text>'
                 f'<text x="{x + 40}" y="{y0 + 20}" font-size="13" text-anchor="middle" fill="var(--ink)">{yr}</text>')
    o.append(f'<text x="16" y="{y0 + 44}" font-size="12" fill="var(--ink2)">Census counts: Fifteenth Census of the United States, 1930, Population vol. I, Florida, table 4, p. 213. In 1930 Sarasota County counted 12,440.</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "boom-promise.svg").write_text(build(), encoding="utf-8")
    print("ok")
