"""Builds data/airfield.json (module 6: The airfield and the book, 1938–1946) and enters the module
in modules.json, plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md, section "Modul 6"):
  Karl H. Grismer, The Story of Sarasota (1946), front matter ("Appreciation", "Prologue"), pp. 249–252
    (IA storyofsarasotah00gris; not renewed, public domain);
  Levy County Journal (Bronson), 30 March 1944, p. 1 (UFDC UF00028309/01606);
  U.S. Army Map Service / Geological Survey, Sarasota quadrangle, 1:24,000, 1944 (USGS Historical Topographic Map Collection).
Run from the site root: python tools/build-airfield.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def u(n, pg, orig, titel=None, note=None):
    x = {"n": n, "pg": pg}
    if titel:
        x["titel"] = titel
    x["orig"] = orig
    if note:
        x["note"] = note
    return x


GR = "Karl H. Grismer, The Story of Sarasota (1946)"

FIELD = [
    u(1, GR + ", p. 249",
      "Repeated efforts were made during the years which followed to interest an airline in coming to Sarasota. But all efforts failed until the summer of 1937 when the National Airlines was induced by the Chamber of Commerce to make Sarasota one of its stops. … The airline was forced to cancel many stops here because of wet grounds and late in the year officials of the company threatened to discontinue service unless concrete runways were provided. This could not be done because of the city's lack of money and soon afterward the line's planes stopped landing here. … Work on the airfield was started late in 1938 as a WPA project. In 1939, the Civil Aeronautics Authority allotted $50,000 for the project and during 1940, with war imminent, more grants followed in rapid succession. By November 20, 1940, 225 Manatee County WPA workers were engaged on the airport work and 74 Sarasota County workers, in addition to 17 non-relief supervisors and foremen.",
      "An airport the city could not pay for",
      "The airport was a joint project of Sarasota and Manatee counties, which had separated in 1921 (module 4). Grismer's opening sentence for the section: the city got its airfield “because of the Great Depression and World War II” (p. 248)."),
    u(2, GR + ", p. 250",
      "The airport authority later leased a large tract of land from Powell Crosley, Jr., and bought other adjoining tracts, so that the airfield could be made into an army air base. How much was spent by the army on the base during the war is anyone's guess but the total undoubtedly ran into millions, due to the number of hangers and barracks constructed in addition to signal towers, lighting facilities, and other improvements. The airfield was first used as a bomber base in the spring of 1942. During the following year it was made into a fighter base and at the peak of the field's operations, more than 3,000 men were stationed there. The base was inactivated January 2, 1946. In the following month, the government turned back the base to Airport Authority …",
      "Sarasota Army Air Base",
      "The Army Air Forces' own records of the base have not been read (see “What is missing”). “Hangers” as printed."),
    u(3, "Levy County Journal (Bronson), 30 March 1944, p. 1",
      "SGT. WM. TOOKE ASSIGNED AS MASTER IN RESCUE BOAT SQUADRON AT AIR BASE. The Commanding Officer of the Sarasota Army Air Base, Sarasota, Florida, today announced the promotion of Sgt. William Tooke, of Cedar Key, Florida, to the rank of Staff Sergeant. Tooke is a member of the Second AAF Emergency Rescue Boat Sq. where he is assigned as master of 35' crash boat. His brother, George F. Tooke and sister Ellen Tooke are also residents of Cedar Key.",
      "A crash boat on the bay",
      "A press release of the base, printed in a county paper a hundred miles north: the air base also kept boats to pick pilots out of the Gulf. Spelling (“Commandinfg”, “Wis brother”) corrected only where the print is plainly broken."),
    u(4, GR + ", p. 250",
      "An even larger air base was established during the war at Venice. The project there was originally planned as an anti-aircraft center for 30,000 men but it was soon changed into a service group training center, becoming activated July 7, 1942. On February 15, 1943, it was made into an army air field and pilot training became its chief business. … The top strength of the base was 6,000 men. The field was inactivated Friday, October 5, 1945.",
      "Venice",
      "Venice lay at the southern end of the lands Mrs. Palmer bought in 1910 (module 3)."),
]

WAR = [
    u(1, GR + ", pp. 250–251",
      "A total of 2389 Sarasota County men, 21 to 35 inclusive, registered for the first draft on Wednesday, October 16, 1940. Before the war ended, 6296 had signed up. This total included 2025 in the older age bracket which was never called. The number from whom the selectees were drawn totalled 4271. Of these, 1726 were inducted—1293 white and 433 colored. It is estimated that at least 400 others volunteered for service before registering. In other words, Sarasota County, with a population in 1940 of only 16,106, had more than 2,000 men in service! The army states that the exact number was 2,285, including women.",
      "1,293 white and 433 colored",
      "The only place in Grismer's history of the war years where Black Sarasotans are counted: a quarter of those drafted. Where they served and how they came home is not in his book."),
    u(2, GR + ", p. 251",
      "Throughout the entire war, and for months afterward, Sarasota was crowded with servicemen, due to the proximity of Sarasota Army Air Base and the Venice Air Base. The housing shortage in Sarasota became so acute that OPA put a ceiling on rents which was not lifted until January, 1946. Termination of the war, and the departure of the servicemen, did not mean the end of Sarasota's housing shortage. During the winter of 1945-46, more winter visitors came to Sarasota than had ever come before, and every available house and room in the city was filled.",
      "No room again",
      "Twenty years after the Herald's “People are actually leaving Sarasota because they can find no place to live” (module 4, “Selling the boom”, [4])."),
    u(3, GR + ", p. 251",
      "As early as the late summer of 1945 it became obvious that Sarasota was entering a period during which it would grow as it had never grown before. And Sarasotans decided that it would be necessary to overhaul and streamline the city's form of government to prevent a repetition of the growing-pain headaches of the Roaring Twenties. To accomplish this, a new city charter, providing for a city manager, was drafted. It was approved 1499 to 405 at a special election held on November 5, 1945. … His success or failure can be reported by the next person who attempts to record the history of Sarasota.",
      "So that the twenties should not come back",
      "The town that had borrowed for streets in empty subdivisions (module 5) votes for a professional manager. Grismer ends his narrative here and hands the next chapter to “the next person who attempts to record the history of Sarasota”."),
    u(4, GR + ", p. 252",
      "The Land of Sarasota is known throughout the nation as a winter playground for thousands of northerners who migrate south with the birds to escape the frigid blasts of their home states. During the season of 1945-46, the number of winter visitors totalled at least 40,000. Providing for the needs of these guests constitutes the major industry of the City of Sarasota, as well as all other communities of the county.",
      "Forty thousand guests",
      "The opening of Grismer's chapter “—And There Are Those Who Work”. Sixty years after the prospectus that promised vegetables for the northern markets (module 1), the town's business is the northerners themselves."),
]

BOOK = [
    u(1, GR + ", “Appreciation”, front matter",
      "The author particularly wishes to express appreciation to Mrs. C. V. S. Wilson, former editor and publisher of the Sarasota Times, and to the late George D. Lindsay, editor of the Sarasota Herald-Tribune, for permitting him to use the files of their newspapers and for reading copy on his manuscript, checking for accuracy. Thanks also are due to Mr. Edwards, Mr. Thacker and Mr. Bickel who read the entire text and to many others who read separate sections. … The author also extends thanks to the Sarasota County Chamber of Commerce, the Kiwanis Club, the Rotary Club, the Lions Club, Sarasota Bay Post No. 30 American Legion, and many public spirited individuals who sponsored publication of the history.",
      "Who made the book",
      "The history was read in manuscript by the editors of the town's two papers and by three of its leading men, among them A. B. Edwards, its first mayor, and published with the support of the Chamber of Commerce and the service clubs. The same page thanks the judge who checked the chapter on the vigilance committee and the son who lent Alex Browning's memoirs (module 1). It is a history the town commissioned of itself; this apparatus quotes it for what it preserves and reads it for what it leaves out."),
    u(2, GR + ", “Prologue”, front matter",
      "Dreams of gold, and silver, and sparkling gems brought conquistadors of Spain to the shores of Florida more than four hundred years ago. They were bitterly resisted by the people we call the Indians—men who loved Florida because of its golden sunshine, its silvery moon in velvet skies, and the sparkling sand on snow-white beaches. For three hundred years the Indians continued battling fair-skinned foes. But the once mighty tribes became weakened by endless wars, white man's diseases, and intermarriage with lesser races. … Today, Florida is loved as ardently as the Indians ever loved it—by people who came here from every state of the Union to make it their home. Not to gain riches but to enjoy the better things of life. … It is the story of this land we are going to tell; the story of its ups and downs, its trials and tribulations, its days of happiness and of sorrow. Just the story of the Land of Sarasota—and nothing more.",
      "“And nothing more”",
      "The prologue speaks of “lesser races” and gives the land to those who came “not to gain riches” — a promise in its own right, from a book that recounts sixty years of land sales. “Conquistators” in the print; the apparatus keeps the racist phrase so that the reader can see how the town's own history began."),
]

SRC = ("Karl H. Grismer, The Story of Sarasota (Sarasota: M. E. Russell, 1946; copyright not renewed): Internet Archive. Levy County Journal, 30 March 1944: Florida Digital Newspaper Library, University of Florida. "
       "Sarasota quadrangle, 1:24,000, mapped by the Army Map Service 1944: U.S. Geological Survey. All in the public domain.")

T = {
    "id": "airfield", "titel": "The airfield and the book", "jahr": "1938–1946",
    "autor": "The town historian of 1946, a county paper, and the Army's map",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. This module ends where the apparatus's main source ends: with the book of 1946, which the town's leading men read in manuscript and its Chamber of Commerce helped to publish. Its last section reads that book itself as a source of its time.",
    "sections": [
        {"id": "field", "titel": "The airfield (1937–1946)",
         "blurb": "An airline came in 1937 and left because the field turned to mud. The WPA began a joint airport with Manatee County in 1938; in the war it became an army air base, first for bombers, then for fighters, with more than 3,000 men. A larger field was built at Venice.",
         "plates": ["usgs1944_sarasota", "lcj1944_tooke"], "units": FIELD},
        {"id": "war", "titel": "The war years (1940–1946)",
         "blurb": "Of the county's men drafted, 1,293 were white and 433 Black. Servicemen filled the town; rents were frozen; after the war more winter visitors came than ever, and the city voted itself a manager so that the twenties should not return.",
         "plates": [], "viz": "airfield-numbers", "units": WAR},
        {"id": "book", "titel": "The book (1946)",
         "blurb": "In 1946 Karl H. Grismer published The Story of Sarasota, read in manuscript by the town's editors and leading men and sponsored by its Chamber of Commerce and clubs. Most of this apparatus rests on it. Its prologue shows the view it was written from.",
         "plates": ["grismer1946_appreciation", "grismer1946_prologue"], "units": BOOK},
    ],
}
for s in T["sections"]:
    s["zk"] = "The airfield and the book, " + re.sub(r" \(.*", "", s["titel"])
(D / "airfield.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
IA = "Internet Archive; public domain."
NEW = [
    {"id": "usgs1944_sarasota", "side": "town", "titel": "Sarasota in 1944",
     "caption": "The northern part of the Sarasota quadrangle, mapped by the Army Map Service from air photographs of 1942: the town in red, Booker School in the Black quarter to the north, Payne Terminal on the bay, the municipal airport of 1929 to the east (Grismer places it at the entrance of the circus winter quarters), the Ringling causeway at the foot.",
     "source": "Sarasota quadrangle, Florida, 1:24,000, 1944, detail. U.S. Geological Survey, Historical Topographic Map Collection; public domain."},
    {"id": "lcj1944_tooke", "side": "work", "titel": "The rescue boats, 1944",
     "caption": "“The Commanding Officer of the Sarasota Army Air Base … today announced the promotion of Sgt. William Tooke, of Cedar Key”, master of a 35-foot crash boat.",
     "source": "Levy County Journal, 30 March 1944, p. 1, detail. Florida Digital Newspaper Library, University of Florida; public domain."},
    {"id": "grismer1946_appreciation", "side": "town", "titel": "Appreciation, 1946",
     "caption": "Grismer's thanks: the families who supplied memories, the editors who read his manuscript “checking for accuracy”, and the Chamber of Commerce and clubs “who sponsored publication of the history.”",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), front matter. " + IA},
    {"id": "grismer1946_prologue", "side": "colour", "titel": "Prologue, 1946",
     "caption": "“Just the story of the Land of Sarasota—and nothing more.” The prologue in which the town's history begins with conquistadors, “lesser races”, and newcomers who came “not to gain riches”.",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), front matter. " + IA},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
if "Geological Survey" not in P["credit"]:
    P["credit"] = P["credit"].replace("All in the public domain.", "The Sarasota quadrangle of 1944: U.S. Geological Survey. All in the public domain.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "airfield"), None) or next(x for x in M["shipped"] if x["id"] == "airfield")
M["planned"] = [x for x in M["planned"] if x["id"] != "airfield"]
m.update({"datei": "airfield", "zk": "Airfield · War years · The book",
          "kurz": "6 · The airfield and the book",
          "warum": "A WPA airport became an army air base with more than 3,000 men; Venice had a larger one. The county's draft counted 1,293 white and 433 Black men; after the war came 40,000 winter visitors and a city manager. In 1946 the town's history appeared, read by its editors and sponsored by its Chamber of Commerce — the book on which most of this apparatus rests.",
          "quelle": "Grismer (1946); Levy County Journal 1944; USGS Sarasota quadrangle 1944."})
order = ["prospectus", "village", "rails", "boom", "bust", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "airfield"] + [m], key=lambda x: order.index(x["id"]))
ADD = [
    {"id": "aafrecords", "side": "work", "kurz": "The Army's records of the air base",
     "warum": "The histories of Sarasota Army Air Base and Venice Army Air Field kept by the Army Air Forces (Air Force Historical Research Agency, on microfilm) have not been read; the module relies on Grismer and a press notice.",
     "quelle": "Air Force Historical Research Agency, unit and base histories."},
    {"id": "blackveterans", "side": "colour", "kurz": "Sarasota's Black servicemen",
     "warum": "Grismer counts 433 Black men drafted from the county and says nothing more of them. Their service and their return to a segregated town are not documented in the public-domain sources read.",
     "quelle": "To be found (Selective Service records; Black press)."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "noroom", "titel": "No place to live",
     "frage": "What happened when the town filled up?",
     "note": "In the boom of 1925 a real estate firm warned that people were leaving Sarasota for want of rooms. In 1945–46 servicemen and winter visitors filled every house; the federal government froze rents, and the city voted for a manager to avoid “the growing-pain headaches of the Roaring Twenties”.",
     "voices": [{"text": "boom", "sec": "selling", "n": [4], "wer": "Sarasota Herald, November 1925"},
                {"text": "airfield", "sec": "war", "n": [2, 3], "wer": "Karl H. Grismer, 1946"}]},
    {"id": "nothingmore", "titel": "Whose story?",
     "frage": "How did Sarasota's first histories frame the town?",
     "note": "The prospectus of 1884 promised land “below the frost line”; the booklet of about 1924 promised “the kind of people you want them to mingle with”; Grismer's prologue of 1946 promised “just the story of the Land of Sarasota—and nothing more”, and began it with “lesser races”.",
     "voices": [{"text": "prospectus", "sec": "prospectus", "n": [6], "wer": "Prospectus, 1884"},
                {"text": "boom", "sec": "selling", "n": [1], "wer": "County booklet, about 1922"},
                {"text": "airfield", "sec": "book", "n": [2], "wer": "Karl H. Grismer, 1946"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/airfield/"
LINK = {"The air base closes": (K + "field/2", "The airfield and the book [field 2]", "usgs1944_sarasota")}
for s in TL["stations"]:
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], s["plate"] = LINK[s["titel"]]
NEWST = [
    {"d": "20 November 1940", "side": "work", "titel": "Relief workers on the airport",
     "text": "225 Manatee County and 74 Sarasota County WPA workers are building the joint airport that becomes an army air base in 1942.",
     "cite": K + "field/1", "citeLabel": "The airfield and the book [field 1]",
     "quelle": "Grismer (1946), p. 249."},
    {"d": "30 March 1944", "side": "work", "titel": "Crash boats",
     "text": "The Sarasota Army Air Base announces the promotion of a sergeant of Cedar Key, master of a 35-foot crash boat in an emergency rescue boat squadron.",
     "cite": K + "field/3", "citeLabel": "The airfield and the book [field 3]", "plate": "lcj1944_tooke",
     "quelle": "Levy County Journal, 30 March 1944, p. 1."},
    {"d": "5 November 1945", "side": "town", "titel": "A city manager",
     "text": "Voters approve a new charter with a city manager, 1,499 to 405, “to prevent a repetition of the growing-pain headaches of the Roaring Twenties”.",
     "cite": K + "war/3", "citeLabel": "The airfield and the book [war 3]",
     "quelle": "Grismer (1946), p. 251."},
    {"d": "1946", "side": "town", "titel": "The Story of Sarasota",
     "text": "Karl H. Grismer's history appears, sponsored by the Chamber of Commerce and the service clubs: “Just the story of the Land of Sarasota—and nothing more.”",
     "cite": K + "book/2", "citeLabel": "The airfield and the book [book 2]", "plate": "grismer1946_prologue",
     "quelle": "Grismer, The Story of Sarasota (1946), front matter."},
]
titles = {s["titel"] for s in NEWST}
TL["stations"] = [s for s in TL["stations"] if s["titel"] not in titles] + NEWST
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def key(s):
    d = s["d"]
    y = re.search(r"\d{4}", d)
    mon = next((i + 1 for i, x in enumerate(MONTHS) if x in d), 13)  # a year without month goes to its end
    day = re.search(r"(\d{1,2}) [A-Z][a-z]+ \d{4}", d)
    return (int(y.group()) if y else 9999, mon, int(day.group(1)) if day else 0)


TL["stations"].sort(key=key)
TL["lede"] = "Stations read against the page images of their sources only; each names its source and links to its passage."
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
