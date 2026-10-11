"""Builds data/village.json (module 2: The village, 1886–1903) and enters the module
in modules.json, plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md, section "Modul 2"):
  Karl H. Grismer, The Story of Sarasota (1946), pp. 101–103, 106, 109–111, 113–114, 120–121, 135–136, 138
    (IA storyofsarasotah00gris; not renewed, public domain);
  Manatee River Journal (Braidentown): 5 December 1889, p. 3; 25 February 1892, p. 2; 11 October 1894, p. 3;
    14 March 1895, p. 2; 24 April 1903, p. 4 (UFDC AA00083378, AA00083046).
Run from the site root: python tools/build-village.py
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
MRJ = "Manatee River Journal (Braidentown)"

BUILD = [
    u(1, GR + ", p. 101",
      "From Edinburgh, Scotland, they sent orders— weeks before the colonists landed here— to their local manager, A. C. Acton, to erect portable houses in which the colonists could stay until they moved into their permanent homes. Acton also got orders to build a large rooming house for people of moderate means and a “fine hotel” where people of wealth and influence could be properly accommodated. In addition, Acton was instructed to build a wharf, where ships could dock, and to open up the streets and avenues shown on the town plat which had been drafted in Scotland.",
      "A town drawn in Scotland",
      "Grismer's account; the orders themselves have not been found. The company's prospectus of 1884 (module 1) offered mortgages, not a town; the plat “drafted in Scotland” is the town Sarasota grew from."),
    u(2, GR + ", p. 102",
      "Construction of the dock and rooming house was started early in January, 1886. A number of colonists were employed to do the work, all who were able or willing to tackle such jobs. A few carpenters from Manatee also were hired. The needed lumber was brought here in schooners from Cedar Keys, Pensacola and Appalachicola. The boats were anchored as close to shore as possible and then the lumber was thrown overboard. While it floated in the water, it was picked up by the workmen and loaded onto wagons which had been pulled out into the bay by mules. Alex Browning, who helped on the job, said in his memoirs it was the worst task he ever had. “The water was mighty cold and we all became badly chilled,” he wrote, “but we stuck to the work until it was finished.”",
      "Lumber in the bay",
      "January 1886 is the month of the snow (module 1, “The colony”, [5]). The colonists who stayed earned wages building the town the company had promised them."),
    u(3, GR + ", p. 103",
      "Before the Sarasota House was finished, seven portable houses, brought here on the schooner Lone Star, were erected by John R. Scott three blocks north of the “business district.” These were intended for use by the colonists but by the time they were erected, most of the colonists had left. They were later occupied by negroes.",
      "The portable houses",
      "One sentence for the first Black residents of the village Grismer mentions: they lived in the colonists' leftover houses, north of the business district. Who they were, he does not say."),
    u(4, GR + ", p. 106",
      "The De Soto was opened with a grand ball Friday night, February 25, 1887. The celebration was the biggest social event ever held south of Manatee. More than two hundred persons attended and the party lasted until daybreak the next morning.",
      "The De Soto Hotel",
      "The company's “fine hotel for people of wealth and influence” (Grismer, p. 106): three stories, an observation tower, thirty rooms. John Hamilton Gillespie, son of Sir John Gillespie, had been sent out to represent the company “shortly after word was received in Scotland that the Scotch colony had collapsed” (p. 105)."),
    u(5, GR + ", pp. 109–110",
      "To speed the work along, Gillespie sent out word that good jobs were available in Sarasota and craftsmen and laborers flocked here from other towns, some coming from as far away as Jacksonville. The boom was on. Every room in the Sarasota House was filled, two to six persons in each room. The overflow lived in tents and shacks scattered along Main Street and the waterfront. Some of the workmen bunked in schooners anchored in the bay. Big wages for those days were paid by Gillespie's company— $2 a day for craftsmen and $1.25 for common laborers. In cash.",
      "The first boom, 1886–1887",
      "Grismer calls it a boom; it lasted as long as the company built. The wages are his figures."),
    u(6, GR + ", p. 111",
      "The Scotch company set forth, early in 1887, to prove to all skeptics that its land was the most fertile in the entire state—and would grow anything. To accomplish this, Gillespie ordered work started on a 40-acre experimental farm on the Fruitville road. A gang of negroes cleared about ten acres and cultivated the soil. … Unfortunately, Gillespie selected as the site of the experimental farm one of the most sterile tracts in the entire region. He knew nothing about the spotty nature of Florida soil—and he wouldn't listen to advice. “Any Florida cracker could have told Gillespie that nothing would grow well in that locality—and nothing did grow,” says A. B. Edwards. “It was the sorriest ground you ever saw and the farm was a complete failure.”",
      "A farm to prove the land",
      "The farm was a promise in the form of a field: proof that the land “would grow anything”. The men who cleared it are named only as “a gang of negroes”."),
]

LEAN = [
    u(1, GR + ", p. 113",
      "Lower Main Street in 1888. The weeds seen in the street grew higher and thicker during the lean years which followed.",
      "Weeds in Main Street",
      "Caption of the photograph (plate). Above it Grismer writes that the company “could not induce other people to pay the $10 or more per acre which it then demanded for its land”. The prospectus of 1884 had put the cost of the land at $3.40 an acre (module 1)."),
    u(2, MRJ + ", 5 December 1889, p. 3",
      "The DeSoto Hotel at Sarasota opened this week for the season.",
      "For the season",
      "One line among the local notes of the county paper. The hotel lived on winter guests; the town had not yet any other business."),
    u(3, MRJ + ", 25 February 1892, p. 2",
      "A PART COMPLETED. Sunday afternoon, the 21st inst., about four o'clock the last rail was laid on the Sarasota Division of the A., G. C. & L. R. R., and the engine stood before the depot in that town. On Monday the road was formally opened. The two passenger coaches which have been some time on the road not having arrived, several of our local carpenters fitted a top, seat, etc., to a flat car and the engine Anthony Peters carried down the line quite a noted gathering, about forty in all … The party left Braidentown at half past three and reached Sarasota after a very pleasant run of an hour and nine minutes. … Reaching Sarasota the party visited the DeSoto Hotel, which is still in the hands of the painters, etc., being rapidly fitted up in the finest style, and will soon be open to tourists who wish to enjoy the beauties of Sarasota bay.",
      "The last rail, February 1892",
      "Grismer (p. 114, [4]) dates the first train from Bradenton to 16 May 1892; the county paper reports the line opened on Monday, 22 February 1892. Regular service may have begun later; the two dates are set side by side on the Compare page."),
    u(4, GR + ", p. 114",
      "Sarasotans called it the “Slow and Wobbly”—that so-called railroad which ran its first train from Bradenton to Sarasota on May 16, 1892. It was a comic strip railroad if there ever was one. The engine was a dilapidated, second-hand wood burner, with a huge fire-box and a towering smokestack which poured forth soot and sparks. The “train” consisted of two flat cars, one of which was covered with a canvas canopy to protect the passengers from sun, and rain, and smoke.",
      "The “Slow and Wobbly”",
      "The town's memory of its first railroad, fifty years later. The flat car with a canopy agrees with the report of 1892 ([3])."),
    u(5, MRJ + ", 11 October 1894, p. 3: Proceedings of the Board of Public Instruction",
      "Teachers were assigned to schools as follows: Prof. T. C. Walton, with Miss Gonce, Assistant, County High School. Mr. C. A. Brush, Sarasota. … A. C. Hudson, Sarasota, colored. — — Manywether, Manatee, colored. Other schools to be supplied.",
      "A teacher for a Black school",
      "From the county school board's list of teachers assigned for the year: at Sarasota a school with a white teacher and a school marked “colored”, each with its own teacher. It is the earliest trace found so far of a Black school at Sarasota."),
]

FREEZE = [
    u(1, GR + ", p. 120",
      "The entire Sarasota region suffered a staggering blow during the winter of 1894-95, the coldest in the history of the state. During the night of December 27, 1894, the temperature fell to 17 degrees above zero. All vegetables were killed and the citrus crop was ruined. The extreme cold was followed by six weeks of unusually warm weather. New crops of vegetables were just getting started. Citrus trees took on new life. But then an even worse freeze occurred, on the night of February 8, 1895. The mercury plummeted to 14, the lowest in the memory of man. The new vegetable crops were killed. Young citrus trees were frozen to the ground.",
      "Fourteen degrees",
      "Ten years after the prospectus of “lands … below the frost line” (module 1). Grismer's temperatures are not attributed to a station."),
    u(2, MRJ + ", 14 March 1895, p. 2, after the Jacksonville Citizen",
      "WHERE THE FREEZE CAME NOT. Products from Manatee County That Were Not Injured by the Cold. … “I noticed a few days ago a statement in one of the papers that there were no vegetables in Florida, not even cabbages. This is a mistake, and does not apply to this section. I send you a second box, with a cabbage well headed, several beets, a sprig of Irish potato of good growth, a turnip of sufficient size to show that it grew through the freeze, and a few bunches of strawberries in all stages of fruitage, and in which I have also added a few oranges and grapefruit.”",
      "“Where the freeze came not”",
      "A grower at Manatee, J. C. Pelot, sends a box of produce to a railroad's passenger agent in Jacksonville, who displays it in a shop window. The freeze is turned into an advertisement: here, it did not reach."),
    u(3, GR + ", p. 120",
      "Strangely enough, however, the two cold spells ultimately helped the Land of Sarasota more than they harmed it. South of the broad Manatee River, the frosts were by no means as severe as they were farther north where practically all the groves were completely destroyed. … The fact that groves in this area escaped being killed by the devastating cold weather of 1894-95 brought a number of new settlers to this locality from farther north in Florida. They wanted a spot where the work of years would not be wiped out in a few nights—and here they found what they wanted.",
      "A frost that sold land",
      "The promise of 1884 returns, smaller and truer: not “below the frost line”, but less frost than elsewhere."),
    u(4, GR + ", pp. 120–121",
      "During 1895, Sarasota first began to be called “a fishing village.” And with good reason. The fishing industry here began to flourish as it had never flourished before. True enough, there had been fishermen here for at least a century before 1895. First, itinerant Cuban and Spanish fishermen, like Alzartie and Phillippi, who lived in palmetto shacks along the bay or on the keys. Then Bill Whitaker, who got his start by selling dry salt mullet and roe to Cuban traders.",
      "A fishing village",
      "In 1895 a federal dredge cut channels in upper Sarasota Bay, and from 7 October a fish dealer's steamer from Tampa called three times a week (Grismer, p. 121): fresh fish on ice could now reach the railroad at Tampa. The Cuban and Spanish fishermen of the earlier century appear here only by surname."),
]

TOWN = [
    u(1, GR + ", p. 135",
      "The first train, consisting of a day coach, a Pullman, a baggage car and the engine, arrived here at 8 p.m., March 22, 1903. The engine was an old wood-burner, No. 52. … The railroad tracks were extended through the town and west on Strawberry Avenue to a dock built out to eight feet of water. Several fish warehouses soon were erected on the dock.",
      "The Seaboard arrives, March 1903",
      "The line was built under the name of the United States & West Indies Railroad & Steamship Co., a subsidiary of the Seaboard Air Line, and renamed Florida West Shore Railway on 9 May 1903 (Grismer, p. 135). The news that it would come brought the vote to incorporate ([2]); the story of the railroad and the winter residents it brought continues in module 3."),
    u(2, GR + ", p. 136",
      "So enthused were the Sarasotans regarding the prospects for the future that they decided the village must be incorporated as a town. A mass meeting was called. It was held Tuesday night, October 14, 1902, in Harry L. Higel's office on the wharf. Practically every qualified voter in the village attended—53 of them. … The vote to incorporate was unanimous. Then the first town officials were elected: John Hamilton Gillespie, mayor; J. B. Turner, Dr. J. O. Brown, George W. Blackburn, W. J. Hill and Harry L. Higel, aldermen; B. D. Gullett, clerk, and T. F. Blair, marshall.",
      "Fifty-three voters",
      "Grismer adds speeches by Higel and Gillespie in quotation marks; they are his dramatization and are omitted here. Who counted as a “qualified voter” in 1902 he does not say, nor whether any Black man voted; the directory of 1897 had listed six Black residents by name ([3])."),
    u(3, GR + ", p. 131",
      "… Hamlin Whitaker, Luke Wood, C. N. Thompson, and E. Woolley. Six colored persons also were listed: J. Coleman, Lewis Colson, E. Justice, John Mays, and I. P. and W. S. Washington. NOTE: More than three-fourths of the above persons lived outside the town limits of Sarasota but received their mail at the Sarasota post office.",
      "Six names in 1897",
      "The end of Grismer's list of the people “known to be living in the present Sarasota County in 1897, as shown by a directory carefully preserved by Mrs. Guy Shepard”. Lewis Colson appears again in 1926, when a hotel for Black tourists is to be named for him (module 4)."),
    u(4, GR + ", p. 138",
      "Sarasota's first gain from incorporation was a calaboose, erected during November on the north side of Cedar Point. To build and equip it, Mayor Gillespie advanced $200. But before he paid out the money he secured a note—canny Scotsman that he was—from the council members for the entire amount, and made sure the loan would pay eight per cent interest.",
      "The first public work: a jail",
      "Grismer tells it as an anecdote of a careful Scot. The town's first building was a lock-up; its first improvement, he writes, the repair of a bridge."),
    u(5, MRJ + ", 24 April 1903, p. 4",
      "Mr. Parrish has introduced a bill making the playing of foot ball illegal, and has secured the passage of his bill legalizing the incorporation of the town of Sarasota.",
      "Made legal",
      "The incorporation of October 1902 was confirmed by the legislature the following spring. Grismer writes that it was made under the state's general law and recorded on 14 November 1902 (p. 136)."),
]

SRC = ("Karl H. Grismer, The Story of Sarasota (Sarasota: M. E. Russell, 1946; copyright not renewed): Internet Archive. "
       "Manatee River Journal, 1889, 1892, 1894, 1895 and 1903: Florida Digital Newspaper Library, University of Florida. All in the public domain.")

T = {
    "id": "village", "titel": "The village", "jahr": "1886–1903",
    "autor": "The town historian of 1946, quoting a colonist's memoirs, and the county paper at Braidentown",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. For these years the town's own newspaper is lost; the apparatus relies on Grismer's history, written in 1946 from interviews, family papers and town records, and on the county paper fifteen miles away. Grismer's invented dialogue is omitted. Black residents appear in these sources in single sentences: as occupants of leftover houses, as a work gang, as six names in a directory, as a teacher on a school board's list.",
    "sections": [
        {"id": "build", "titel": "Building a village (1886–1887)",
         "blurb": "While the colony broke up, the company began the town it had drawn in Edinburgh: a wharf, a rooming house, streets cut through the woods, and a hotel for people “of wealth and influence”. For a year there were wages and a boom; a farm was meant to prove that the land would grow anything.",
         "plates": ["grismer1946_sarasotahouse"], "units": BUILD},
        {"id": "lean", "titel": "The lean years (1887–1894)",
         "blurb": "When the building stopped, the workmen left and weeds grew in Main Street. The hotel opened for winter guests; in 1892 a short railroad reached the village from Braidentown. The county's school board appointed a teacher for a Black school at Sarasota.",
         "plates": ["grismer1946_mainstreet", "mrj1889_desoto", "mrj1892_rail", "mrj1894_teachers"], "units": LEAN},
        {"id": "freeze", "titel": "The freeze (1894–1895)",
         "blurb": "Ten years after the prospectus, two freezes killed the crops of Florida. South of the Manatee River the groves survived better than elsewhere, and the cold became an argument: here the freeze came less.",
         "plates": ["mrj1895_freeze"], "viz": "village-ways", "units": FREEZE},
        {"id": "town", "titel": "A town (1897–1903)",
         "blurb": "In 1902 the news that the Seaboard would come brought fifty-three voters to a meeting on the wharf, and the village became a town, with Gillespie as mayor and a jail as its first building. The first train arrived in March 1903.",
         "plates": ["mrj1903_legal"], "units": TOWN},
    ],
}
for s in T["sections"]:
    s["zk"] = "The village, " + re.sub(r" \(.*", "", s["titel"])
(D / "village.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UF = "Florida Digital Newspaper Library, University of Florida; public domain."
IA = "Internet Archive; public domain."
NEW = [
    {"id": "grismer1946_sarasotahouse", "side": "colony", "titel": "The Sarasota House",
     "caption": "The rooming house of 1886, “as it looked just before it was razed in 1924” (Grismer's caption). Built by the company for “people of moderate means”.",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 103. " + IA},
    {"id": "grismer1946_mainstreet", "side": "town", "titel": "Lower Main Street, 1888",
     "caption": "“The weeds seen in the street grew higher and thicker during the lean years which followed.” The De Soto Hotel with its tower on the left, the bay and the wharf at the end of the street.",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 113. " + IA},
    {"id": "mrj1889_desoto", "side": "colony", "titel": "Open for the season, 1889",
     "caption": "“The DeSoto Hotel at Sarasota opened this week for the season.” Next to it, the engineers are expected for the Manatee and Sarasota railroad.",
     "source": "Manatee River Journal, 5 December 1889, p. 3, detail. " + UF},
    {"id": "mrj1892_rail", "side": "town", "titel": "“A Part Completed”, 1892",
     "caption": "The last rail laid on the Sarasota division on 21 February 1892, and a flat car fitted with a top for the first party: “an hour and nine minutes” from Braidentown.",
     "source": "Manatee River Journal, 25 February 1892, p. 2, detail. " + UF},
    {"id": "mrj1894_teachers", "side": "colour", "titel": "Teachers appointed, 1894",
     "caption": "The county school board's list of teachers, among them “A. C. Hudson, Sarasota, colored.”",
     "source": "Manatee River Journal, 11 October 1894, p. 3, detail. " + UF},
    {"id": "mrj1895_freeze", "side": "work", "titel": "“Where the Freeze Came Not”, 1895",
     "caption": "A box of oranges, cabbages, beets and strawberries from Manatee, shown in a Jacksonville window after the freeze of February 1895.",
     "source": "Manatee River Journal, 14 March 1895, p. 2, detail. " + UF},
    {"id": "mrj1903_legal", "side": "town", "titel": "Incorporation legalized, 1903",
     "caption": "The county's representative “has secured the passage of his bill legalizing the incorporation of the town of Sarasota.”",
     "source": "Manatee River Journal, 24 April 1903, p. 4, detail. " + UF},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "village"), None) or next(x for x in M["shipped"] if x["id"] == "village")
M["planned"] = [x for x in M["planned"] if x["id"] != "village"]
m.update({"datei": "village", "zk": "Building · Lean years · Freeze · Town",
          "kurz": "2 · The village",
          "warum": "After the colony the company built the town it had drawn in Edinburgh: a wharf, a rooming house and the De Soto Hotel. The work ended and weeds grew in Main Street; a railroad came in 1892, the freezes of 1894–95 hit the groves less than elsewhere, and in 1902 fifty-three voters made the village a town.",
          "quelle": "Grismer (1946); Manatee River Journal 1889, 1892, 1894, 1895, 1903."})
order = ["prospectus", "village", "rails", "boom", "bust", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "village"] + [m], key=lambda x: order.index(x["id"]))
ADD = [
    {"id": "blackschool", "side": "colour", "kurz": "The Black school and church before 1914",
     "warum": "A teacher for a Black school at Sarasota is listed in 1894; where the school stood, who attended it, and the Black churches of the village before Newtown have not been found in the public-domain sources read. The county school board's minutes would be the next source.",
     "quelle": "Manatee County Board of Public Instruction, minutes."},
    {"id": "gazetteer1895", "side": "town", "kurz": "The village in the gazetteers of the 1890s",
     "warum": "The Florida railroad gazetteer of 1895 lists Sarasota with a population of 100, the De Soto Hotel and J. H. Gillespie as justice of the peace (OCR only); it has not yet been read against the page image.",
     "quelle": "Florida Railroad Gazetteer 1895."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "firsttrain", "titel": "The first train",
     "frage": "When did the railroad from Braidentown reach Sarasota?",
     "note": "The county paper of 25 February 1892 reports the last rail laid on Sunday, 21 February, and the road “formally opened” the next day with a flat car fitted with a top. Grismer, fifty years later, dates the first train to 16 May 1892. Both describe the same improvised car; the difference may lie between an opening excursion and regular service.",
     "voices": [{"text": "village", "sec": "lean", "n": [3], "wer": "Manatee River Journal, February 1892"},
                {"text": "village", "sec": "lean", "n": [4], "wer": "Karl H. Grismer, 1946"}]},
    {"id": "frostline2", "titel": "Ten years after “below the frost line”",
     "frage": "What became of the promise of 1884 in the freeze of 1895?",
     "note": "The prospectus of 1884 sold land “below the frost line”. In February 1895 the thermometer fell to 14 degrees. A grower at Manatee sent a box of vegetables to Jacksonville to show that the freeze had not come there; Grismer saw the freeze as the making of the district's reputation.",
     "voices": [{"text": "prospectus", "sec": "prospectus", "n": [6], "wer": "Prospectus, 1884"},
                {"text": "village", "sec": "freeze", "n": [1, 3], "wer": "Karl H. Grismer, 1946"},
                {"text": "village", "sec": "freeze", "n": [2], "wer": "J. C. Pelot, Manatee, March 1895"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/village/"
LINK = {
    "Six names apart": (K + "town/3", "The village, 1897 [3]", None),
    "A town": (K + "town/2", "The village, 1902 [2]", None),
}
for s in TL["stations"]:
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], pl = LINK[s["titel"]]
        if pl:
            s["plate"] = pl
NEWST = [
    {"d": "25 February 1887", "side": "colony", "titel": "The De Soto opens",
     "text": "The company's hotel opens with a ball: “More than two hundred persons attended and the party lasted until daybreak the next morning.”",
     "cite": K + "build/4", "citeLabel": "The village, 1887 [4]",
     "quelle": "Grismer, The Story of Sarasota (1946), p. 106."},
    {"d": "1888", "side": "town", "titel": "Weeds in Main Street",
     "text": "The building boom is over; the company asks $10 or more an acre and finds no buyers.",
     "cite": K + "lean/1", "citeLabel": "The village [lean 1]", "plate": "grismer1946_mainstreet",
     "quelle": "Grismer (1946), p. 113."},
    {"d": "21 February 1892", "side": "town", "titel": "The last rail",
     "text": "The last rail is laid on the Sarasota division of the railroad from Braidentown; the next day a flat car with a top carries the first party down the line.",
     "cite": K + "lean/3", "citeLabel": "The village [lean 3]", "plate": "mrj1892_rail",
     "quelle": "Manatee River Journal, 25 February 1892, p. 2."},
    {"d": "11 October 1894", "side": "colour", "titel": "A Black school",
     "text": "The county school board lists “A. C. Hudson, Sarasota, colored” among its teachers.",
     "cite": K + "lean/5", "citeLabel": "The village [lean 5]", "plate": "mrj1894_teachers",
     "quelle": "Manatee River Journal, 11 October 1894, p. 3."},
    {"d": "8 February 1895", "side": "work", "titel": "Fourteen degrees",
     "text": "The second freeze of the winter: “The mercury plummeted to 14.” Groves south of the Manatee River survive better than those farther north.",
     "cite": K + "freeze/1", "citeLabel": "The village [freeze 1]", "plate": "mrj1895_freeze",
     "quelle": "Grismer (1946), p. 120; Manatee River Journal, 14 March 1895."},
    {"d": "22 March 1903", "side": "town", "titel": "The Seaboard arrives",
     "text": "The first train of the Seaboard's subsidiary arrives at 8 p.m.; the tracks run on to a dock where fish houses are built.",
     "cite": K + "town/1", "citeLabel": "The village, 1903 [1]",
     "quelle": "Grismer (1946), p. 135."},
    {"d": "April 1903", "side": "town", "titel": "Incorporation legalized",
     "text": "The legislature passes a bill “legalizing the incorporation of the town of Sarasota”.",
     "cite": K + "town/5", "citeLabel": "The village, 1903 [5]", "plate": "mrj1903_legal",
     "quelle": "Manatee River Journal, 24 April 1903, p. 4."},
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
