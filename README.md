# Below the Frost Line

Sarasota, 1884–1946: a documentary apparatus in English, built from public-domain sources read against the page images. From the Edinburgh prospectus of 1884 that offered 47,000 acres on Sarasota Bay “below the frost line”, and the Scottish colonists who met snow in their first winter, to the vigilance murders of 1884, the village and the town of 1902, the railroad and the winter residents, the county of 1921, the boom and the bust, Newtown and the celery fields, the work-relief buildings of the 1930s and the Army air base of the war.

It asks who was promised what, who came and who left, and who belonged to the town and who was kept at its edge.

Live: https://below-the-frost-line.netlify.app/

**Status (October 2026):** module 1 printed (31 passages, 10 plates, one graphic, three comparisons); five to follow.

1. **The prospectus and the colony, 1884–1888** — the Edinburgh prospectus of October 1884 (“below the frost line”); the Sara Sota Vigilance Committee, the killings of Harrison T. Riley and Charles E. Abbe, the trials and the Supreme Court; the Scottish colony of December 1885, Tait's letter, the snow, Dan McKinlay's diary; the verdicts of 1886, 1887 and 1946.
2. **The village, 1887–1902**
3. **Rails and patrons, 1903–1920**
4. **The county and the boom, 1921–1926**
5. **After the boom, 1926–1941**
6. **The airfield and the book, 1942–1946**

What is **not carried**, and why, is listed on the Texts page (`data/modules.json`, key `missing`).

**Companion game:** *A City of Glorified Opportunity* (free, in preparation).

## Files

- `data/modules.json`: the modules carried and planned, and what is not carried and why.
- `data/prospectus.json`: the texts of module 1.
- `data/timeline.json`, `data/compare.json`, `data/plates.json`.
- `tools/build-frame.py` (once, before the first module), later `tools/build-<module>.py`, `tools/viz-<module>.py`, `tools/make-plates.py`. The plate script reads page images and PDFs from the project's source folder (`../quellen`, not in this repository), where the check log (`PRUEFUNG.md`) records for each passage the page image it was read against.

Static site without a build step: `index.html`, `app.js` (hash routes; engine adapted from *Not Practicable*), `style.css`, `legal.html`, `_headers`. Local: `python -m http.server` in the repository, then `http://localhost:8000/`.

## Licences

Code MIT; editorial texts CC BY 4.0; editions CC0 1.0; plates public domain. See [LICENSES.md](LICENSES.md).
