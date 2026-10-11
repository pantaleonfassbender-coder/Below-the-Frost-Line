"""Draws assets/viz/bust-banks.svg for module 5 (After the boom): Sarasota's four banks that closed or liquidated,
1928–1933, with their deposits and what the depositors got back, as Grismer gives them (The Story of Sarasota,
1946, p. 221, read against the page image).
Run from the site root: python tools/viz-bust.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
BANKS = [  # name, date, deposits (None = not given), cents returned per dollar
    ("American National Bank", "15 May 1928", 462489, 18.5),
    ("First Bank and Trust Co.", "17 July 1929", 513091.42, 18.25),
    ("Bank of Sarasota", "29 August 1932", 719518.95, 42.5),
    ("Ringling Bank and Trust Co.", "1 May 1933", None, 100),
]


def build():
    W, H = 900, 330
    x0, x1 = 330, 860
    title = "What the depositors got back"
    desc = "; ".join(f"{n}, closed {d}: deposits {'$' + format(v, ',.0f') if v else 'not given'}, {c} cents on the dollar returned" for n, d, v, c in BANKS) + ". The Ringling bank's depositors were paid in full by Edith Ringling."
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bb-t bb-d" font-family="var(--serif)">',
         f'<title id="bb-t">{escape(title)}</title><desc id="bb-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<a href="#/text/bust/bust/2"><text x="16" y="48" font-size="13" fill="var(--ink2)" text-decoration="underline">Cents returned on each dollar deposited, Sarasota banks closed 1928–1933, as Grismer gives them. Link to the passage.</text></a>']
    for c in (0, 25, 50, 75, 100):
        x = x0 + c / 100 * (x1 - x0)
        o.append(f'<line x1="{x:.0f}" y1="66" x2="{x:.0f}" y2="262" stroke="var(--line)"/><text x="{x:.0f}" y="280" font-size="12" text-anchor="middle" fill="var(--ink2)">{c}¢</text>')
    y = 76
    for n, d, v, c in BANKS:
        col = "var(--promise)" if c < 100 else "var(--colony)"
        o.append(f'<text x="16" y="{y + 13}" font-size="13" fill="var(--ink)">{escape(n)}</text>'
                 f'<text x="16" y="{y + 29}" font-size="11.5" fill="var(--ink2)">{escape(d)} · deposits {("$" + format(v, ",.0f")) if v else "not given"}</text>'
                 f'<rect x="{x0}" y="{y + 4}" width="{c / 100 * (x1 - x0):.1f}" height="24" fill="{col}"/>'
                 f'<text x="{x0 + c / 100 * (x1 - x0) + 6 if c < 100 else x1 - 6:.0f}" y="{y + 21}" font-size="12.5" text-anchor="{"start" if c < 100 else "end"}" fill="{"var(--ink)" if c < 100 else "var(--panel)"}">{c:g}¢{" — paid by Edith Ringling" if c == 100 else ""}</text>')
        y += 46
    o.append('<text x="16" y="310" font-size="12" fill="var(--ink2)">The Palmer National Bank, opened in 1929, closed only during the national bank holiday of 1933 and reopened.</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "bust-banks.svg").write_text(build(), encoding="utf-8")
    print("ok")
