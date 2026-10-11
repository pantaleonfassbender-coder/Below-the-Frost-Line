# Below the Frost Line

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23291691.svg)](https://doi.org/10.5281/zenodo.23291691)

Sarasota, 1884–1946: a documentary apparatus in English, built from public-domain sources read against the page images. From the Edinburgh prospectus of 1884 that offered 47,000 acres on Sarasota Bay “below the frost line”, and the Scottish colonists who saw snow in their first winter, to the vigilance murders of 1884, the village and the town of 1902, the railroad and the winter residents, the county of 1921, the boom and the bust, Newtown and the celery fields, the work-relief buildings of the 1930s, the Army air base of the war, and the town's own history of 1946.

It asks who was promised what, who came and who left, and who belonged to the town and who was kept at its edge.

Live: https://below-the-frost-line.netlify.app/

**Stage 1 is closed (October 2026).** It carries six modules with 108 passages:

- **1 The prospectus and the colony, 1884–1888** — the Edinburgh prospectus of October 1884 (“below the frost line”); the Sara Sota Vigilance Committee, the killings of Harrison T. Riley and Charles E. Abbe, the trials at Pine Level and the Supreme Court; the Scottish colony of December 1885, the promoter's letter, the snow, Dan McKinlay's diary; the verdicts of 1886, 1887 and 1946.
- **2 The village, 1886–1903** — the town drawn in Edinburgh; lumber floated ashore in January 1886; the De Soto Hotel; a farm to prove the land; weeds in Main Street; the railroad from Braidentown (1892, two dates); a Black school's teacher on the county list of 1894; the freezes of 1894–95; fifty-three voters and a jail; the Seaboard in March 1903.
- **3 Rails and patrons, 1903–1920** — J. H. Lord's advertisement in Chicago and Bertha Palmer's arrival (1910); her 75,000 to 100,000 acres, the Oaks, Meadow Sweet Pastures, the Myakka drainage and her death (1918); John Ringling's purchase (two versions) and the circus posters; the city charter with a mill for advertising (1913); lynchings at Parrish (1903) and Bradentown (1912); Newtown.
- **4 The county and the boom, 1921–1926** — the line between Manatee and Sarasota counties; the murder of Harry L. Higel and the mob; a Black prisoner killed at Salt Springs; the hurricane of October 1921; the booklets of about 1922 and 1924 (“twenty-five thousand permanent residents”); John Ringling's causeway; Booker school, “Wildcat” Morgan, the Klan's circus and advertisement, Newtown's argument over joining the city and the hotel named for Lewis Colson.
- **5 After the boom, 1926–1941** — thirty-seven “millionaires” and four banks; more than $13 million of public debt, much of it for streets in empty subdivisions; the circus winter quarters (1927), the Ringling museum (1931) and the art school; Palmer Farms' celery and the water under it; the Tin Can Tourists; the CCC at Myakka River State Park, the WPA's auditorium and Lido Beach Casino.
- **6 The airfield and the book, 1937–1946** — the WPA airport and the Army air base; Venice; 1,293 white and 433 Black men drafted; 40,000 winter visitors and a city manager; Karl H. Grismer's *Story of Sarasota*, sponsored by the Chamber of Commerce, read as a source of its time.

With 51 public-domain plates (newspaper pages, court reports, promotional booklets, a camp paper, a federal hearing, photographs from Grismer's book, the Army's map of 1944), 6 graphics, 14 comparisons setting the sources side by side, and a timeline of 53 stations linked into the texts.

What is **not carried**, and why, is listed on the Texts page (`data/modules.json`, key `missing`, 24 entries): among them the Sarasota Times of 1899–1929 and the bust in its own record (not digitized), the prisoner killed at Salt Springs (unnamed, outcome not found), Newtown in its own words, the celery workers, the beaches, and two chapters left open for later: William and Marie Selby, and the art colony.

**Companion game:** *A City of Glorified Opportunity* (free, in preparation).

## Files

- `data/modules.json`: the modules carried, and what is not carried and why.
- `data/<module>.json`: the texts (`prospectus`, `village`, `rails`, `boom`, `bust`, `airfield`).
- `data/timeline.json`, `data/compare.json`, `data/plates.json`.
- `tools/build-frame.py` (once, before the first module), `tools/build-<module>.py`, `tools/viz-<module>.py`, `tools/make-plates.py`. The plate script reads page images and PDFs from the project's source folder (`../quellen`, not in this repository), where the check log (`PRUEFUNG.md`) records for each passage the page image it was read against.

Static site without a build step: `index.html`, `app.js` (hash routes; engine adapted from *Not Practicable*), `style.css`, `legal.html`, `_headers`. Local: `python -m http.server` in the repository, then `http://localhost:8000/`.

## Citation

Fassbender, Pantaleon. *Below the Frost Line: Sarasota, 1884–1946. A Documentary Apparatus.* 2026. https://doi.org/10.5281/zenodo.23291691 (all versions; version 1.0.0: https://doi.org/10.5281/zenodo.23291692). Please also cite the printed source of any passage you quote. Metadata: `CITATION.cff`, `.zenodo.json`.

## Licences

Code MIT; editorial texts CC BY 4.0; editions CC0 1.0; plates public domain. See [LICENSES.md](LICENSES.md).
