"""Builds the frame of the apparatus: data/modules.json (planned and missing), data/timeline.json,
and empty data/compare.json and data/plates.json. Module builds (tools/build-<id>.py) later move
modules from "planned" to "shipped" and add their stations, pairs and plates.

Every station below was read against the page image of its source (check log: ../quellen/PRUEFUNG.md).

    python tools/build-frame.py      (once, before the first module)
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

PLANNED = [
    ("prospectus", "promise", "1 · The prospectus and the colony",
     "In October 1884 the Florida Mortgage and Investment Company of Edinburgh announced the purchase of 47,000 acres on Sarasota Bay, “below the frost line”. In December 1885 its Scottish colonists landed at a settlement that had no town; that winter snow fell, and most of them left. Meanwhile the trials of a vigilance committee that had killed two men in 1884 were in the newspapers of half the country.",
     "Prospectus, The Economist, 25 October 1884; Bacon v. State, 22 Fla. 51 (1886) and Anderson v. State, 24 Fla. 139 (1888); Chicago Daily Tribune, 6 February 1886; W. R. Lawson in Time (London), April 1887; colonists' memoirs as quoted in Grismer (1946)."),
    ("village", "colony", "2 · The village",
     "After the colony: a hotel for winter guests, a golf course laid out by the company's Scottish manager, the freeze of 1895, a directory of 1897 that lists six Black residents beside the white ones, and the mass meeting of October 1902 that made the village a town.",
     "Florida gazetteers 1886–87 and 1895; Manatee River Journal 1888–1902; Grismer (1946)."),
    ("rails", "town", "3 · Rails and patrons",
     "The railroad reached Sarasota in 1903. Winter residents with great fortunes followed: Bertha Palmer of Chicago from 1910, John Ringling of the circus from 1911. From about 1914 Black families built homes in Newtown, outside the town.",
     "Manatee River Journal 1903–1921; Bradentown City Directory 1916 (with Sarasota); census 1910 and 1920; Grismer (1946)."),
    ("boom", "promise", "4 · The county and the boom",
     "In 1921 Sarasota became the seat of its own county. In the same year a hurricane struck the waterfront and a former convict guard was held for the murder of a Black prisoner. In the boom of 1925–26 lots, hotels and islands were sold, the causeway to the keys opened, the Klan paraded, and a hotel for Black tourists was planned.",
     "Manatee River Journal 1921; Monthly Weather Review, October 1921; promotional booklets of about 1922 and 1924; Sarasota Herald, October 1925 to August 1926."),
    ("bust", "work", "5 · After the boom",
     "The boom ended in 1926. In the years that followed the celery fields of Palmer Farms, worked mostly by Black labourers, the trailer camps of winter visitors, the Civilian Conservation Corps at Myakka, and the Works Progress Administration's auditorium and beach casino carried the town; the Ringling museum and art school opened.",
     "Census 1930; Ship-canal hearings 1937; Myakka Rattler (CCC camp paper) 1934–35; Florida state park reports; National Youth Administration directory 1936; Grismer (1946)."),
    ("airfield", "town", "6 · The airfield and the book",
     "From 1942 an Army air base stood east of the town, with more than 3,000 men at its peak; it closed on 2 January 1946. In the same year Karl H. Grismer published The Story of Sarasota: the history a town tells about itself, and what it leaves out.",
     "Florida newspapers 1942–45; USGS Sarasota quadrangle 1944; Grismer (1946)."),
]

MISSING = [
    ("times", "town", "The Sarasota Times, 1899–1929",
     "The town's own weekly is not digitized. A survey of 1995 lists two issues at the University of South Florida and a run from 1910 to 1924 with the city's historical resources department. Until it can be read, the apparatus relies on the newspaper of Bradentown and on papers elsewhere."),
    ("bust", "promise", "The bust in its own record",
     "The digitized Sarasota Herald ends in August 1926. For the collapse of the boom, the hurricane of September 1926, the Depression and the town's debts, no public-domain local source has been found yet; Grismer speaks only of a mayor who “succeeded in refunding the city's debt”."),
    ("scotland", "colony", "The colony in the Scottish press",
     "The company's pamphlet of 1885 and the Scottish newspapers that reported the colonists' complaints (the North British Mail, January 1886) are not reachable here; the British Newspaper Archive is paid. They are known through American reprints."),
    ("browning", "colony", "Alex Browning's memoirs",
     "The colonist's memoirs were lent to Grismer as a family manuscript. Only the passages Grismer printed in 1946 are used; a part printed in 1999 is protected."),
    ("bunkley", "law", "The prisoner killed at Salt Springs, 1921",
     "A newspaper of June 1921 reports that a former convict guard, J. R. Bunkley, was held for the murder of a Black prisoner at Salt Springs and bound over to the grand jury of Sarasota County. The prisoner is not named and the outcome has not been found."),
    ("beach", "colour", "The beaches",
     "No public-domain source before 1946 has been found on who was allowed on Sarasota's beaches. Later reports (1955–56) are named only as pointers."),
    ("selby", "colony", "William and Marie Selby",
     "The Sarasota Herald of 1925–26 records William Selby and his wife as winter residents from Marietta, Ohio. Their arrival, their house on the bay and the gardens that bear Marie Selby's name lie outside what the sources read so far can carry; a chapter of its own is left open."),
    ("art", "colony", "The art colony",
     "The Ringling museum (opened 1931) and the art school are documented here only in passing. The painters, classes and exhibitions of the 1930s and 1940s are left open for a chapter of their own."),
    ("wpaguide", "town", "The WPA guide to Florida (1939)",
     "The Federal Writers' Project guide has a long entry on Sarasota, but its copyright was renewed in 1967. It is not quoted here."),
]

STATIONS = [
    ("25 October 1884", "promise", "47,000 acres below the frost line",
     "The Florida Mortgage and Investment Company announces “a provisional contract … for the purchase of 47,000 acres of freehold land, situate on Sarasota Bay, Manatee County, Florida”; the most delicate vegetables grown there go to the northern markets in January and February, “as the lands are below the frost line”.",
     "Prospectus, The Economist, 25 October 1884, p. 1313."),
    ("1884", "law", "The Sara Sota Vigilance Committee",
     "A witness at the trial for the murder of Harrison T. Riley tells of a meeting in Jason Alford's house on the Saturday night before the killing: “That was a meeting of an organization known as the Sara Sota Vigilance Committee, styled S. S. V. C.”",
     "Bacon, Andrews and Bidwell v. State, 22 Fla. 51 (January term 1886), p. 64."),
    ("27 December 1884", "law", "The postmaster is shot",
     "Charles E. Abbe is killed by a shotgun shot to the head; Florida's Supreme Court later finds the killing premeditated and upholds the conviction of Joseph C. Anderson as present, aiding and abetting.",
     "Anderson v. State, 24 Fla. 139 (1888), p. 140."),
    ("January 1886", "colony", "Snow",
     "A colonist remembers: “About January 9 it became much colder and snow began to fall, greatly to the surprise of the natives who thought at first the woods were afire and that the ashes were being carried by the wind.”",
     "Memoirs of Alex Browning, as quoted in Karl H. Grismer, The Story of Sarasota (1946), p. 97."),
    ("1897", "colour", "Six names apart",
     "A directory of the people living in what became Sarasota County lists the residents of Sarasota by name. “Six colored persons also were listed: J. Coleman, Lewis Colson, E. Justice, John Mays, and I. P. and W. S. Washington.”",
     "Grismer, The Story of Sarasota (1946), p. 131, after a directory of 1897."),
    ("14 October 1902", "town", "A town",
     "At a mass meeting in Harry L. Higel's office on the wharf the village votes to incorporate as a town. “Practically every qualified voter in the village attended—53 of them.”",
     "Grismer, The Story of Sarasota (1946), p. 136."),
    ("August 1911", "colony", "The circus man buys a home",
     "John Ringling, fishing in the Sarasota section, buys the winter home of C. N. Thompson, “said to be one of the finest places in that section of the State”.",
     "Tampa Times, 28 August 1911, reprinted in the Manatee River Journal, 31 August 1911, p. 1."),
    ("1914", "colour", "Newtown",
     "On 33rd Street, outside the town, Black families build “tiny homes” in Newtown, opened by Charles N. Thompson. “Previously, their principal living quarters had been at Black Bottom, in the vicinity of 12th and Lemon.”",
     "Grismer, The Story of Sarasota (1946), p. 179."),
    ("June 1921", "law", "A guard held for murder",
     "J. R. Bunkley, “former convict guard, who is being held for the murder of a negro prisoner at Salt Springs”, is bound over on a bond of $5,000 until the grand jury of Sarasota County meets. In the same week the Governor appoints the officials of the new county.",
     "Manatee River Journal, 23 June 1921, p. 1."),
    ("17 November 1925", "law", "The Klan at the circus",
     "“Approximately 150 local Klansmen attended the circus in full Klan regalia. A huge Klan parade was held immediately before the start of the evening's program.”",
     "Sarasota Herald, 17 November 1925, p. 7."),
    ("18 August 1926", "colour", "A hotel for the colored tourist trade",
     "E. O. Burns announces a $15,000 hotel on Central near Fourteenth Street that “will cater to the colored tourist trade”, to be named for Louis Colson, who had worked in the home of J. H. Gillespie and died about two years before.",
     "Sarasota Herald, 18 August 1926, p. 5."),
    ("3 May 1927", "work", "Palmer Farms ships",
     "Drained from 1924 and first planted in January 1927, Palmer Farms sends its first shipment: three cars of tomatoes and one of potatoes. It later turns to celery; by 1946 “70 per cent of those employed are negroes”.",
     "Grismer, The Story of Sarasota (1946), p. 256."),
    ("1930", "town", "8,398",
     "The census counts 8,398 people in the city of Sarasota, against 2,149 in 1920 and 840 in 1910, and 12,440 in Sarasota County.",
     "Fifteenth Census of the United States: 1930, Population, vol. I, Florida, table 4, p. 213."),
    ("2 January 1946", "town", "The air base closes",
     "The Army air base, a bomber base from the spring of 1942 and then a fighter base with more than 3,000 men at its peak, is inactivated; the following month the government turns it back to the Airport Authority.",
     "Grismer, The Story of Sarasota (1946), p. 250."),
]


def dump(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import sys
    DATA.mkdir(exist_ok=True)
    cur = json.loads((DATA / "modules.json").read_text(encoding="utf-8")) if (DATA / "modules.json").exists() else {}
    if cur.get("shipped") and "--force" not in sys.argv:
        sys.exit("modules are already shipped; the frame would overwrite them (use --force only to start over)")
    dump("modules.json", {
        "shipped": [],
        "planned": [dict(id=i, side=s, kurz=k, warum=w, quelle=q) for i, s, k, w, q in PLANNED],
        "missing": [dict(id=i, side=s, kurz=k, warum=w, quelle="—") for i, s, k, w in MISSING]})
    dump("timeline.json", {
        "lede": "Stations read against the page images of their sources only; each names its source. Links into the modules follow as the modules are printed.",
        "stations": [dict(d=d, side=s, titel=t, text=x, quelle=q) for d, s, t, x, q in STATIONS]})
    dump("compare.json", {"lede": "Where the sources speak about the same thing, their voices stand side by side.", "pairs": []})
    dump("plates.json", {"lede": "Public-domain maps, photographs, prints and newspaper pages, each with its source. Plates follow with the modules.", "credit": "", "plates": []})
    print("frame written")
