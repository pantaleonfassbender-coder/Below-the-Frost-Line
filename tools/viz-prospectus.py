"""Draws assets/viz/prospectus-tracks.svg for module 1 (The prospectus and the colony): two tracks on one time axis,
August 1884 to April 1887 — the company and its colony above, the vigilance committee and the courts below.
Every date is taken from a passage of the module, read against the page image; each mark links to its passage.
Run from the site root: python tools/viz-prospectus.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/prospectus/"
# (months since January 1884, label, link)
COMPANY = [
    (9.8, "Prospectus: 47,000 acres “below the frost line”", "prospectus/6", 0),
    (23.6, "Colonists land (late December)", "colony/2", 0),
    (24.1, "Tait: “in excellent health”", "colony/2", 1),
    (24.3, "Snow (“about January 9”)", "colony/5", 2),
    (25.5, "McKinlay leaves for Tampa", "colony/7", 3),
    (39.5, "“The now notorious colony”", "verdict/2", 0),
]
COURT = [
    (7.5, "Riley killed", "vigilance/4", 0),
    (11.9, "Abbe killed, 27 Dec.", "vigilance/7", 1),
    (13.0, "Arrests reported", "vigilance/2", 2),
    (14.5, "Indictments, March", "vigilance/9", 3),
    (18.5, "Verdict, 14 July", "vigilance/9", 0),
    (24.5, "Supreme Court affirms (January term 1886)", "vigilance/11", 1),
]


def build():
    W, H = 920, 390
    x0, x1, m0, m1 = 40, 890, 6, 41
    X = lambda m: x0 + (m - m0) / (m1 - m0) * (x1 - x0)
    title = "Two stories on one bay, 1884–1887"
    desc = ("Time line from mid-1884 to April 1887. Upper track, the company and the colony: "
            + "; ".join(i[1] for i in COMPANY) + ". Lower track, the vigilance committee and the courts: "
            + "; ".join(i[1] for i in COURT) + ".")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="pt-t pt-d" font-family="var(--serif)">',
         f'<title id="pt-t">{escape(title)}</title><desc id="pt-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         '<text x="16" y="48" font-size="13" fill="var(--ink2)">The company and its colony above, the vigilance committee and the courts below. Each mark links to its passage.</text>']
    ya, yb = 175, 255
    o.append(f'<line x1="{x0}" y1="215" x2="{x1}" y2="215" stroke="var(--line)" stroke-width="2"/>')
    for yr in (1885, 1886, 1887):
        x = X((yr - 1884) * 12)
        o.append(f'<line x1="{x:.0f}" y1="70" x2="{x:.0f}" y2="345" stroke="var(--line)" stroke-dasharray="3 3"/>'
                 f'<text x="{x + 4:.0f}" y="229" font-size="12" fill="var(--ink2)">{yr}</text>')
    o.append(f'<text x="{x0}" y="78" font-size="12.5" font-weight="bold" fill="var(--promise)">The company and the colony</text>')
    o.append(f'<text x="{x0}" y="376" font-size="12.5" font-weight="bold" fill="var(--law)">The vigilance committee and the courts</text>')

    def track(items, y, up, col):
        for m, lab, link, lvl in items:
            x = X(m)
            ty = y - 18 - lvl * 19 if up else y + 28 + lvl * 19
            o.append(f'<line x1="{x:.0f}" y1="{y}" x2="{x:.0f}" y2="{ty + (6 if up else -12)}" stroke="{col}"/>'
                     f'<circle cx="{x:.0f}" cy="{y}" r="5" fill="{col}"/>')
            anchor = "end" if x > 640 else "start"
            o.append(f'<a href="{T}{link}"><text x="{x + (-4 if anchor == "end" else 4):.0f}" y="{ty}" font-size="12" text-anchor="{anchor}" '
                     f'fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></a>')

    track(COMPANY, ya, True, "var(--promise)")
    track(COURT, yb, False, "var(--law)")
    o.append(f'<line x1="{x0}" y1="{ya}" x2="{x1}" y2="{ya}" stroke="var(--promise)" stroke-width="1.5"/>'
             f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="var(--law)" stroke-width="1.5"/>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prospectus-tracks.svg").write_text(build(), encoding="utf-8")
    print("ok")
