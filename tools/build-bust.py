"""Builds data/bust.json (module 5: After the boom, 1926–1941) and enters the module
in modules.json, plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md, section "Modul 5"):
  Karl H. Grismer, The Story of Sarasota (1946), pp. 213, 215, 220–221, 223, 226–228, 233, 245, 247–248, 256, 267–268 and plates
    (IA storyofsarasotah00gris; not renewed, public domain);
  Atlantic-Gulf Ship Canal, Fla.: Hearings before the Committee on Rivers and Harbors, House of Representatives (1937), p. 299
    (UFDC UF00018663);
  The Myakka Rattler, weekly paper of Company 1421, Civilian Conservation Corps, 29 March and 2 August 1935
    (IA myakkarattler2252cccc, myakkarattler2422cccc);
  National Youth Administration for Florida, Directory of Opportunities for Youth in Florida (1936), p. 434 (UFDC UF00053734);
  Fifteenth Census of the United States: 1930, Population, vol. I, Florida, table 4, p. 213.
Run from the site root: python tools/build-bust.py
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
RAT = "The Myakka Rattler (Company 1421, Civilian Conservation Corps)"

BUST = [
    u(1, GR + ", pp. 220–221",
      "One day in October, 1925, when the Florida boom was at its peak, two newspaper reporters put their heads together and began listing all the “millionaires” and “near millionaires” in Sarasota—not counting the Palmers or the Ringlings, or any winter residents. When they finished they had the names of 37 men listed as being worth anywhere from $500,000 to a million or more. Two years after the boom ended, one of the reporters ran across the list in his desk and started checking off the names of the men who had “lost their shirts” when real estate values crashed. Of the original 37, all except four were checked off as “busted.” … Many business firms went bankrupt. Scores of houses and apartments were sold at sacrifice prices to satisfy mortgages. The three leading hotels went into the hands of receivers.",
      "Thirty-seven millionaires",
      "Grismer himself calls the reporters' list “not … any too accurate”. The Sarasota Herald's digitized run ends in August 1926; the collapse is told here from his book alone (see “What is missing”)."),
    u(2, GR + ", p. 221",
      "The American National Bank closed its doors Tuesday noon May 15, 1928. … Depositors, who had $462,489 in the bank, ultimately received only 18½ cents on the dollar. … Then came the crash of the First Bank and Trust Co., on July 17, 1929. The depositors finally received approximately 18¼ cents on the dollar—and their deposits totalled $513,091.42. They lost more than $400,000. The Bank of Sarasota, which had operated on a more conservative basis, survived until the depths of the Great Depression were reached in mid-summer of 1932. It closed August 29. … The depositors eventually received 42½ cents on the dollar. The Ringling Bank and Trust Co. went into voluntary liquidation on May 1, 1933, but Mrs. Edith Ringling, widow of Charles Ringling, paid off the depositors in full, at a loss to herself of a reported $250,000.",
      "The banks",
      "Four banks in five years. Who the depositors were, Grismer does not say; the savings lost were those of people who had trusted the promises of the boom."),
    u(3, GR + ", p. 223",
      "At the end of the boom, the city and county were nearly crushed under a staggering load of bonded indebtedness. By 1928 the county had a bonded indebtedness of $5,841,000, in addition to $1,223,000 worth of school bonds, and the debts of the city totalled approximately $6,200,000. Bonds had been issued profligately, with the greatest abandon, and apparently no idea that the community might some time suffer a period of adversity. … A large part of the city's bonded indebtedness was assumed to build paved streets in subdivisions “far out in the sticks.” Also, to lay water mains in places where no houses had been built. The paved streets were nice to look at, and helped real estate salesmen in making sales, but, after the boom had burst and the streets were covered with grass they were a headache to pay for.",
      "Paved streets in the sticks",
      "The city's own borrowing had paid for the promise: streets and water mains for lots that were sold, not lived on. How the debt was settled Grismer tells only in passing, in his sketch of Mayor E. A. Smith (1931–1945, with a break), who “succeeded in refunding the city's debt, without cost to the city, and reduced the interest rate to three per cent” (p. 329). The records of the settlement with the bondholders have not been found."),
    u(4, "Fifteenth Census of the United States: 1930, Population, vol. I, Florida, table 4, p. 213",
      "Sarasota city … 1930: 8,398 … 1920: 2,149 … 1910: 840. Sarasota County … 1930: 12,440.",
      "The count of 1930",
      "The booklet of about 1924 had set the goal of 25,000 residents within five years (module 4, “Selling the boom”, [3]). The census of 1930 counted a third of that; the town had nevertheless grown fourfold in ten years."),
]

CIRCUS = [
    u(1, GR + ", pp. 226–227, quoting Dudley V. Haddock of the Florida State Chamber of Commerce, 24 April 1927",
      "“Sarasota was one of the ‘boomiest’ of the boom centers during the turbulent days of 1925 and when the bubble burst found itself with much of its assets frozen. … The season was nearing its conclusion with Sarasota's people wondering how much they would have to economize to pull through the summer when John Ringling's announcement came. It changed the situation completely. To prepare for the arrival of the circus, Ringling must spend approximately $500,000 in the erection of buildings. This assures a large payroll through the summer, and once the circus is here, it will mean the employment of mechanics in the building and repairing of circus wagons, railroad cars and other equipment.”",
      "The circus comes for the winter, 1927",
      "Ringling announced on 23 March 1927 that the winter quarters of Ringling Brothers and Barnum & Bailey would move to Sarasota (Grismer, p. 226). The grounds were opened to the public on Christmas Day 1927 (p. 227): the circus's off-season became the town's attraction."),
    u(2, GR + ", pp. 227–228",
      "The museum, which cost $2,500,000 is built around a courtyard 150 by 350 feet in size. Of Florentine design, the building has columns from Greece which are more than 1,000 years old and original wall foundations from Italy equally as old. … The museum was opened to the public in 1931. It houses the finest individual collection of Rubens in the world, artists say, besides many original Titians, Rembrandts, and other world-famous paintings. … The circus winter quarters and the Ringling museum were assets Sarasota gained after the Florida boom burst.",
      "A museum after the boom",
      "Grismer's figures and judgements; the plate's caption adds that the museum and its collection were “willed to the state by the late John Ringling” (p. 213). The art colony that grew around it is left for a chapter of its own (see “What is missing”)."),
    u(3, "National Youth Administration for Florida, Directory of Opportunities for Youth in Florida (1936), p. 434",
      "RINGLING JUNIOR COLLEGE. Verman Kimbrough, President. The Ringling Jr. College, Sarasota, Florida, consists of a School of Arts and Sciences, School of Music, and the Ringling School of Art. Admission Requirements: Graduates of accredited high schools and special students are admitted upon receipt of certificate of credit. Expenses: Minimum cost per year $500.",
      "The Ringling School of Art",
      "A federal relief agency's directory for the young. The School of Art, opened in 1931, is one line of it; $500 a year was the price of the arts in Depression Sarasota."),
]

WORK = [
    u(1, "Atlantic-Gulf Ship Canal, Fla.: Hearings, House Committee on Rivers and Harbors (1937), p. 299: J. G. Kimmel, civil engineer, Sarasota",
      "I have been connected with this agricultural development, known as Palmer Farms, at Sarasota, Fla., since 1923, when the first plans were laid for the reclomation of the lands in which these farms lie. Palmer Farms originally consisted of two level muck or peat ponds having an area of about 2 square miles each, together with a higher sandy land surrounding the ponds. These lands were first drained and a total of 133 artesian wells drilled to supply water for irrigation during the dry season. The growing of celery soon became practically the only industry. This crop requires a large volume of water and it soon became apparent that a greater volume than that supplied by free flow from the wells would be needed. Naturally, the first thought was more wells, but already, after only 2 or 3 years of use, the head on the wells which originally stood 8 to 10 feet above the ground, had decreased appreciably.",
      "Celery on the muck, and the water under it",
      "An engineer of the Palmers' farming company, testifying in Washington against a sea-level canal across Florida that might draw down the ground water (see the companion apparatus Not Practicable). “Reclomation” as printed. The celery fields, drained from 1924, were the Palmers' second promise of land: small farms for settlers."),
    u(2, GR + ", p. 256",
      "Other large growers and marketers are: Burquest & Stockbridge, F-an-Cee Farms, Muckland Celery Co., the Raoul Co., and the Sarasota Celery Co. Approximately 1,500 persons are employed in the raising and marketing of the celery crop; 70 per cent of those employed are negroes. It should be recorded here that drainage of Palmer Farms was started in 1924; that the first plantings were made in January, 1927, and that the first shipment of produce, consisting of three cars of tomatoes and one car of potatoes, was made May 3, 1927. Later, the Farms specialized on the production of celery.",
      "Who worked the fields",
      "Grismer's figures for the 1940s. The growers are named; the workers, most of them Black, are a percentage."),
    u(3, GR + ", p. 233",
      "When the Tin Can Tourists first began coming to Sarasota, back in the winter of 1919-20, the city had no place for them to stay. … During the winter of 1921-22, the Tin Canners' grounds were moved to Osprey Avenue south of Morrill and the tourists were charged $10 per season. … This site soon proved inadequate and the present Trailer Park was established at Payne Park in 1931 and the national conventions of the Tin Can Tourists were held there each year thereafter until 1937. … During the winter months, Trailer Park is a community within a community, and its population at times approaches 5,000.",
      "The Tin Can Tourists",
      "The winter visitors of the lean years came in cars and trailers. A town that had promised a “society circle” in 1910 (module 3) now rented trailer lots to thousands."),
]

RELIEF = [
    u(1, RAT + ", 29 March 1935, p. 5",
      "TELEPHONE LINE. Another task has been completed. The telephone line from Bee Ridge to camp is open now. There are twelve miles of line which were put up by about fourteen of the enrollees. Mr. Oldham has been in charge of the project and has finished it in the record time of three weeks.",
      "Twelve miles of line",
      "The camp paper of the Civilian Conservation Corps company at Myakka, typed and duplicated by the young men themselves."),
    u(2, RAT + ", 2 August 1935, p. 3",
      "RIVER RISES FIVE FEET IN TWO DAYS. The beautiful Myakka River has come back to life again, after a long period of dry weather. The rainy season has restored it's life to the point of flowing, to the joy of Company 1421.",
      "The river comes back",
      "The river Mrs. Palmer had wanted dredged in 1916 (module 3) is, nineteen years later, the camp's landscape."),
    u(3, GR + ", pp. 267–268",
      "Finally, in September, 1934, they succeeded in persuading the Internal Improvement Board of the state to purchase 17,500 acres from the estate of Adrian C. Honore, a brother of the late Mrs. Potter Palmer. Then, two weeks later, 1920 acres, comprising the most beautiful part of the whole Myakka River valley, was deeded to the state for park purposes by Honore Palmer and Potter Palmer, as an outright gift in memory of their mother. … During the winter of 1934-35, development of the park was started by CCC workers … The work continued until shortly before Pearl Harbor. Approximately 250 men were employed for over six years. They built roads and bridges, dug drainage ditches, cut out underbrush and constructed pavillions, cabins, rest rooms, barns, garages, a gate house and concession buildings. … The park was officially dedicated February 28, 1941, and was opened to the public June 1, 1942.",
      "Myakka River State Park",
      "Land bought for a ranch and for resale in 1910 became a public park in 1934: part bought by the state from the Palmers' heirs, part given by Mrs. Palmer's sons. The cattle range of the Myakka, fought over in the tick-dipping years, is now the place visitors come to see."),
    u(4, GR + ", p. 245",
      "The site was obtained by the city from the defunct Sarasota Bay Hotel Co. Taxes amounting to about $15,000 had accumulated on the property and the city secured it by purchasing the tax certificates … The federal government put $131,000 into the project in two grants, the first for $114,000 and the second for $17,000. Skilled labor was paid for by the city out of its general fund; common labor was paid by WPA. Work was started in July, 1937. The auditorium was opened February 24, 1938, for the Sara de Soto celebration. More than 3,000 persons attended.",
      "Bayfront Park and the Municipal Auditorium",
      "Grismer lists the citizens who agreed in March 1937 to advance the money needed to obtain the federal grant; among them is William G. Selby, whose name comes back in the gardens of a later Sarasota (see “What is missing”). The land came from a hotel company the bust had ruined."),
    u(5, GR + ", p. 248",
      "Early in 1938, a tract of land on Lido Beach with 1300 feet of beach frontage was secured from the Ringling Estate in a tax settlement arrangement. Construction of the casino as a WPA project was approved by the government June 13, 1938. The city was required to pay $40,000 in cash, in addition to donating the land. To secure the money, a $40,000 special revenue bond issue was approved 890 to 97 at an election held Tuesday, July 19, 1938. … The casino was formally opened December 27, 1940, with more than a thousand persons attending by special invitation.",
      "Lido Beach Casino",
      "A public beach with a pavilion, built with federal relief money on land the Ringling estate gave up for its taxes. Who was allowed on that beach in 1940 the sources read do not say (see “What is missing”)."),
]

SRC = ("Karl H. Grismer, The Story of Sarasota (1946; copyright not renewed); The Myakka Rattler, 1935; Fifteenth Census of the United States, 1930: Internet Archive. "
       "Atlantic-Gulf Ship Canal, Fla.: Hearings (1937); National Youth Administration, Directory of Opportunities for Youth in Florida (1936): University of Florida Digital Collections. "
       "All in the public domain (federal publications, a federal camp paper, and a book not renewed).")

T = {
    "id": "bust", "titel": "After the boom", "jahr": "1926–1941",
    "autor": "The town historian of 1946, a CCC camp paper, a federal hearing and a federal directory",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. For these years the town's own papers are not digitized, and the collapse is told mainly by Grismer, who wrote as the town's historian and favoured its leading men; his figures are given as his. What carried Sarasota through the Depression is documented better than what it cost: the federal programmes left publications, the people who lost their savings and the labourers in the celery fields did not.",
    "sections": [
        {"id": "bust", "titel": "The bust (1926–1933)",
         "blurb": "The boom ended in 1926. Of thirty-seven local “millionaires”, a reporter later counted thirty-three “busted”; four banks failed or closed between 1928 and 1933, and the city and county owed more than thirteen million dollars, much of it for paved streets in subdivisions where no one lived.",
         "plates": ["grismer1946_museum"], "viz": "bust-banks", "units": BUST},
        {"id": "circus", "titel": "The circus and the museum (1927–1936)",
         "blurb": "In March 1927 John Ringling brought the winter quarters of his circus to Sarasota; the grounds opened to visitors at Christmas. His museum opened in 1931, and an art school with it.",
         "plates": ["grismer1946_quarters", "nya1936_ringling"], "units": CIRCUS},
        {"id": "work", "titel": "Celery and trailers (1924–1937)",
         "blurb": "Palmer Farms drained two muck ponds, drilled 133 artesian wells and turned to celery, worked mostly by Black labourers. The winter visitors of the lean years came in trailers; from 1931 the Tin Can Tourists held their conventions at Payne Park.",
         "plates": ["hearing1937_kimmel"], "units": WORK},
        {"id": "relief", "titel": "Relief (1934–1941)",
         "blurb": "The federal government built what the town could no longer pay for. The Civilian Conservation Corps made a state park on the Myakka out of Palmer land; the Works Progress Administration built an auditorium on the bayfront and a casino on Lido Beach.",
         "plates": ["rattler1935_mast", "rattler1935_tel", "rattler1935_river", "grismer1946_auditorium", "grismer1946_casino"], "units": RELIEF},
    ],
}
for s in T["sections"]:
    s["zk"] = "After the boom, " + re.sub(r" \(.*", "", s["titel"])
(D / "bust.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
IA = "Internet Archive; public domain."
UFD = "University of Florida Digital Collections; public domain (federal publication)."
NEW = [
    {"id": "grismer1946_museum", "side": "colony", "titel": "The Ringling museum",
     "caption": "The loggia of the John and Mable Ringling Museum of Art (photograph by Burnell): “willed to the state by the late John Ringling.”",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 213. " + IA},
    {"id": "grismer1946_quarters", "side": "work", "titel": "The winter quarters",
     "caption": "Elephants in the ring at the winter quarters (photograph by Burnell): the quarters of Ringling Brothers and Barnum & Bailey, “the biggest show on earth”, “attract tourists to Sarasota from all parts of Florida.”",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 215. " + IA},
    {"id": "nya1936_ringling", "side": "town", "titel": "Ringling Junior College, 1936",
     "caption": "The National Youth Administration's directory: “a School of Arts and Sciences, School of Music, and the Ringling School of Art. … Minimum cost per year $500.”",
     "source": "Directory of Opportunities for Youth in Florida (1936), p. 434. " + UFD},
    {"id": "hearing1937_kimmel", "side": "work", "titel": "Palmer Farms in Congress, 1937",
     "caption": "J. G. Kimmel of Sarasota before the House Committee on Rivers and Harbors: two muck ponds, 133 artesian wells, and celery as “practically the only industry”.",
     "source": "Atlantic-Gulf Ship Canal, Fla.: Hearings (1937), p. 299. " + UFD},
    {"id": "rattler1935_mast", "side": "work", "titel": "The Myakka Rattler",
     "caption": "The masthead of the weekly paper of Company 1421, Civilian Conservation Corps, Sarasota, 2 August 1935, drawn by the enrollees.",
     "source": "The Myakka Rattler, vol. 2, no. 42, 2 August 1935, cover, detail. " + IA},
    {"id": "rattler1935_tel", "side": "work", "titel": "“Another task has been completed”",
     "caption": "Twelve miles of telephone line from Bee Ridge to the camp, put up by about fourteen enrollees in three weeks.",
     "source": "The Myakka Rattler, 29 March 1935, p. 5, detail. " + IA},
    {"id": "rattler1935_river", "side": "work", "titel": "The river comes back, 1935",
     "caption": "“The beautiful Myakka River has come back to life again, after a long period of dry weather.”",
     "source": "The Myakka Rattler, 2 August 1935, p. 3, detail. " + IA},
    {"id": "grismer1946_auditorium", "side": "town", "titel": "Where tourists meet and play",
     "caption": "The Municipal Auditorium in Bayfront Park, built with WPA labour and opened in February 1938; below, lawn bowling and shuffleboard (photographs by Burnell).",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), plate facing p. 246. " + IA},
    {"id": "grismer1946_casino", "side": "town", "titel": "Lido Beach Casino",
     "caption": "“The municipally owned Lido Beach Casino”, opened in December 1940 (photograph by Burnell).",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 247. " + IA},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = P["credit"].replace("All in the public domain.", "Federal hearings and directories: University of Florida Digital Collections. The Myakka Rattler: Internet Archive. All in the public domain.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "bust"), None) or next(x for x in M["shipped"] if x["id"] == "bust")
M["planned"] = [x for x in M["planned"] if x["id"] != "bust"]
m.update({"datei": "bust", "zk": "Bust · Circus and museum · Celery and trailers · Relief",
          "kurz": "5 · After the boom",
          "warum": "After 1926 most of the boom's fortunes and four banks were gone, and the city and county owed more than thirteen million dollars. The circus came for the winter, a museum and an art school opened, celery was grown on drained muck by Black labourers, trailer tourists filled Payne Park, and federal relief built Myakka River State Park, an auditorium and a beach casino.",
          "quelle": "Grismer (1946); census 1930; ship-canal hearings 1937; Myakka Rattler 1935; NYA directory 1936."})
order = ["prospectus", "village", "rails", "boom", "bust", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "bust"] + [m], key=lambda x: order.index(x["id"]))
for x in M["missing"]:
    if x["id"] == "bust":
        x["kurz"] = "The bust in its own record"
        x["warum"] = ("The digitized Sarasota Herald ends in August 1926. The collapse, the hurricane of September 1926, the bank failures and the town's debts are told in module 5 only from Grismer's history of 1946. "
                      "The Herald of 1926–1938 (catalogued at the University of Florida but not online), the records of the bondholders' settlement and Florida's banking reports would be needed.")
ADD = [
    {"id": "celeryworkers", "side": "colour", "kurz": "The celery workers",
     "warum": "Grismer counts those employed in the celery crop in the 1940s as “70 per cent … negroes”. Their wages, housing and camps in the 1920s and 1930s, and any labour dispute, have not been found in public-domain sources.",
     "quelle": "To be found (farm labour reports, Florida Department of Agriculture)."},
    {"id": "cccsegregation", "side": "colour", "kurz": "Who served in the CCC at Myakka",
     "warum": "Company 1421's paper names its enrollees but nowhere states their colour. Whether Black young men served at Myakka, in this company or another, has not been found in the sources read.",
     "quelle": "Florida CCC records; Myakka Rattler, full run."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "myakka", "titel": "The Myakka, three times",
     "frage": "What was the Myakka valley for?",
     "note": "In 1910 Mrs. Palmer bought it for a ranch and resale; in 1916 she asked Washington to drain the river; in 1934 her heirs sold and gave it to the state for a park, on which the Civilian Conservation Corps worked for six years.",
     "voices": [{"text": "rails", "sec": "palmer", "n": [4, 5], "wer": "Grismer, 1946; Manatee River Journal, 1916"},
                {"text": "bust", "sec": "relief", "n": [3], "wer": "Karl H. Grismer, 1946"},
                {"text": "bust", "sec": "relief", "n": [2], "wer": "The Myakka Rattler, 1935"}]},
    {"id": "goal", "titel": "Twenty-five thousand",
     "frage": "How did the boom's goal compare with the count?",
     "note": "A booklet of about 1924 set the goal of twenty-five thousand permanent residents within five years. The census of 1930 counted 8,398 in the city; the city owed about $6,200,000, much of it for streets in empty subdivisions.",
     "voices": [{"text": "boom", "sec": "selling", "n": [3], "wer": "Booklet, about 1924"},
                {"text": "bust", "sec": "bust", "n": [4, 3], "wer": "Census, 1930; Grismer, 1946"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/bust/"
LINK = {
    "Palmer Farms ships": (K + "work/2", "After the boom [work 2]", "hearing1937_kimmel"),
    "8,398": (K + "bust/4", "After the boom [bust 4]", None),
}
for s in TL["stations"]:
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], pl = LINK[s["titel"]]
        if pl:
            s["plate"] = pl
NEWST = [
    {"d": "23 March 1927", "side": "work", "titel": "The circus comes for the winter",
     "text": "John Ringling announces that the winter quarters of Ringling Brothers and Barnum & Bailey will move to Sarasota; the grounds open to visitors on Christmas Day.",
     "cite": K + "circus/1", "citeLabel": "After the boom [circus 1]", "plate": "grismer1946_quarters",
     "quelle": "Grismer (1946), pp. 226–227."},
    {"d": "15 May 1928", "side": "promise", "titel": "The first bank closes",
     "text": "The American National Bank closes; its depositors get back 18½ cents on the dollar. Three more banks follow by 1933.",
     "cite": K + "bust/2", "citeLabel": "After the boom [bust 2]",
     "quelle": "Grismer (1946), p. 221."},
    {"d": "1931", "side": "colony", "titel": "Museum and trailer park",
     "text": "The Ringling museum opens to the public; the city's Trailer Park at Payne Park opens and hosts the national conventions of the Tin Can Tourists until 1937.",
     "cite": K + "circus/2", "citeLabel": "After the boom [circus 2]", "plate": "grismer1946_museum",
     "quelle": "Grismer (1946), pp. 228, 233."},
    {"d": "September 1934", "side": "work", "titel": "A park on the Myakka",
     "text": "The state buys 17,500 acres from the estate of Mrs. Palmer's brother; her sons give 1,920 acres of the valley. The CCC begins work that winter.",
     "cite": K + "relief/3", "citeLabel": "After the boom [relief 3]", "plate": "rattler1935_mast",
     "quelle": "Grismer (1946), pp. 267–268; Myakka Rattler 1935."},
    {"d": "24 February 1938", "side": "town", "titel": "The auditorium opens",
     "text": "The Municipal Auditorium in Bayfront Park, built with WPA labour on land taken for back taxes, opens for the Sara de Soto celebration.",
     "cite": K + "relief/4", "citeLabel": "After the boom [relief 4]", "plate": "grismer1946_auditorium",
     "quelle": "Grismer (1946), p. 245."},
    {"d": "27 December 1940", "side": "town", "titel": "Lido Beach Casino",
     "text": "The WPA's beach casino on Lido Beach opens, on land the Ringling estate gave up in a tax settlement.",
     "cite": K + "relief/5", "citeLabel": "After the boom [relief 5]", "plate": "grismer1946_casino",
     "quelle": "Grismer (1946), p. 248."},
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
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
