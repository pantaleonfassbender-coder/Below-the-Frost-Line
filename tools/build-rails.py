"""Builds data/rails.json (module 3: Rails and patrons, 1903–1920) and enters the module
in modules.json, plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md, section "Modul 3"):
  Chicago Sunday Tribune, 23 January 1910, part X, p. 13 (IA per_chicago-daily-tribune_1910-01-23_69_4, n74);
  Manatee River Journal (Bradentown): 30 June 1910, p. 1; 31 August 1911, p. 1; 20 April 1916, p. 8;
    9 May 1918, p. 1; 27 November 1919, p. 3 (UFDC AA00083046);
  NAACP, Thirty Years of Lynching in the United States, 1889–1918 (1919), pp. 55–56 (IA thirtyyearsoflyn00nati);
  Karl H. Grismer, The Story of Sarasota (1946), pp. 157, 159, 169–170, 174–175, 179 and plates (IA storyofsarasotah00gris).
Run from the site root: python tools/build-rails.py
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
MRJ = "Manatee River Journal (Bradentown)"

PALMER = [
    u(1, "Chicago Sunday Tribune, 23 January 1910, part X, p. 13: advertisement",
      "FLORIDA. GRAPE FRUIT AND ORANGE GROVES. BEAUTIFUL WINTER HOMES. FRUIT AND VEGETABLE LANDS in the famous Sarasota Bay district of Manatee County, on the gulf. I am one of the largest growers and land owners in Manatee County and can furnish you with any kind or size property desired. I also improve lands and raise groves for purchasers. Best location in U. S. Lowest prices. Easy terms. Call or write for free book and full information. J. H. LORD, Owner, 922 Marquette Bldg.",
      "An advertisement in Chicago",
      "Grismer tells that Bertha Honoré Palmer, widow of the Chicago merchant and hotel owner Potter Palmer, read an advertisement of J. H. Lord in this issue (pp. 155–156). This is the advertisement of Lord in the farm-lands columns of that Sunday; Grismer's paraphrase of its wording (“richest land in the world”, “like Venus from the foam of the sea”) does not match it, and the scene in which she reads it is his invention."),
    u(2, GR + ", p. 157",
      "On Thursday, February 10, the Palmers arrived in Sarasota in a private car—Mrs. Palmer and her two sons, Honore and Potter Palmer, Jr. Mrs. Palmer also was accompanied by her father, H. H. Honore, and her brother, Adrian C. Honore. Edwards met the party with misgivings. He was afraid that Mrs. Palmer, the world-known celebrity, would be “high hat” and arrogant. But, to his relief, he soon learned she was delightfully friendly and courteous. And instead of being scornful of Sarasota's shabbiness, she called the town “refreshingly quaint.”",
      "“Refreshingly quaint”",
      "A. B. Edwards, Lord's partner in Sarasota and later the city's first mayor ([1] in “A city”), was Grismer's informant; the words attributed to Mrs. Palmer come through him. The town's hotel was so run down, Grismer writes, that a doctor's sanitarium was refitted to house her party (pp. 156–157)."),
    u(3, MRJ + ", 30 June 1910, p. 1",
      "Planning for a Florida Colony. Mrs. Potter Palmer has undertaken one of the greatest development propositions ever known in Florida. She has just completed a purchase of between 75,000 and 100,000 acres on the west coast of Florida, in Manatee county, extending approximately twenty-five miles along Sarasota Bay from Sarasota to Venice, Florida, and about twelve miles inland. The Seaboard Air Line has just authorized a twenty-five mile extension from the terminus of Fruitville to Venice, bi-secting the property just purchased by Mrs. Palmer. Mrs. Palmer and her son, Honore Palmer, expect to develop the property and place some of it on sale this fall. Plans have already been drawn for bungalows for Mrs. Palmer and Honore Palmur, and it is expected that a society circle will be developed along the beautiful coast of Sarasota Bay. The investment totals approximately $300,000, and none of the acreage is to be sold to colonist at less than $100.00 per acre.",
      "“A society circle”",
      "Twenty-six years after the Edinburgh company's 47,000 acres at $3.40 (module 1), a single buyer takes up to twice as much, to resell at no less than $100 an acre (see the graphic). “Palmur” as printed."),
    u(4, GR + ", p. 159",
      "After building “The Oaks,” Mrs. Palmer bought more and more property. Finally, she acquired more than 80,000 acres in the Sarasota region and also made large purchases in Hillsborough County. Her purchases boosted land values in this region to an undreamed-of peak. To develop the property here, the Sarasota-Venice Co. was organized with Adrian C. Honore as president … An extensive advertising campaign was launched to sell small tracts to settlers. The Bee Ridge area was the first to be developed and sold. Mrs. Palmer then proceeded to establish a model cattle ranch, called Meadow Sweet Pastures, in the Myakka Lake region. To improve the breed of cattle, she purchased prize bulls. She was one of the first persons in the state to advocate cattle dipping to eliminate ticks. At that time, practically all free-range cattle owners fought the tick-eradication measures viciously, insisting dipping would “kill the cows.” Mrs. Palmer went ahead and proved it didn't.",
      "The Oaks and Meadow Sweet Pastures",
      "The open range on which the cattle of the back country grazed is the “right of free grazing” that the promoter of 1886 blamed for the settlers' hostility (module 1, “The colony”, [2]). A cattleman's view of the tick laws is not in the sources read."),
    u(5, MRJ + ", 20 April 1916, p. 8",
      "Representative A. M. Wilson, of Miakka, was in Bradentown today, having returned from Washington last Friday, where he went in the interest of a drainage project through which he hopes that by government aid more than 50,000 acres of valuable land may be reclaimed, in addition to large areas which will be materially benefitted. Mrs. Potter Palmer, of Osprey, accompanied the representative to Washington and appeared before the board of engineers in the intereset of the project.",
      "Draining the Myakka",
      "Under the headline “Mrs. Potter Palmer Talks to Engineers”. The resolution of 1913 asked the federal government to drain the Myakka River “for the double purpose of reclamation and transportation”. The same river's lake country became Myakka River State Park in the 1930s (module 5). “Intereset” as printed."),
    u(6, MRJ + ", 9 May 1918, p. 1",
      "Mrs. Potter Palmer died at her winter home, “The Oaks,” at Osprey, at 9:15 o'clock last Sunday night. Mrs. Palmer had been in failing health for several months and came to Florida somewhat earlier this winter than had been her custom, in the hope that climatic conditions would prove beneficial. In this she was disappointed.",
      "Died at Osprey, May 1918",
      "Eight years after her first visit. Her sons and her brother carried on the Sarasota-Venice Co.; the county's tax rolls of 1921 still list large holdings of “the late Mrs. Potter Palmer” (Manatee River Journal, 18 August 1921, OCR)."),
]

RINGLING = [
    u(1, MRJ + ", 31 August 1911, p. 1, after the Tampa Times of 28 August",
      "CIRCUS MAN BUYS HOME. John Ringling, the noted circus man, who has been spending some days in this section, as was noted in the Times last week, left last night in his private car for the north. He was accompanied by Mrs. Ringling. For several days they have been in the Sarasota section enjoying the fishing under the guidance of Dr. Jack Halton, the well known hotel man. … Mr. Ringling is very much impressed with this section of the State, and will return in a few weeks. He is considering the matter of bringing his immense shows to Tampa this winter. While at Sarasota Mr. Ringling purchased the winter home of C. N. Thompson, which is near that town, and is said to be one of the finest places in that section of the State.",
      "“Circus Man Buys Home”",
      "The Tampa paper reports the purchase in August 1911. Grismer, from the county's deed records, has the Thompson home bought first by Ralph C. Caples in November 1911 and resold to Ringling in January 1912 ([2]). The circus came to Sarasota for the winter only in 1927 (module 5)."),
    u(2, GR + ", p. 170",
      "Another Sarasota booster also was doing his utmost to lure the Ringlings to this section—Ralph C. Caples, then general agent of the New York Central … The Caples-Thompson publicity team proved irresistable. The Ringlings finally were sold on Sarasota's charms. Yellowing records in the Manatee County courthouse show that on November 3, 1911, Caples bought the Thompson home and a large tract of land—and that on January 31, 1912, less than three months later, Caples resold the house and most of the land to John Ringling. That started the Ringling ball a'rolling. John began buying more and more land and soon his brother Charles followed suit. By the spring of 1912, Shell Beach was booming.",
      "Boosters at work",
      "Charles N. Thompson, the seller, was a circus man too (Grismer, p. 169); he later opened Newtown ([3] in “The colour line”). “Irresistable” as printed."),
    u(3, MRJ + ", 27 November 1919, p. 3",
      "RINGLING TO ADVERTISE SARASOTA AND WEST COAST. The Ringling brothers, who have large holdings in Sarasota and vicinity announce that next year they are going to advertise Sarasota and the West Coast of Florida by placing stickers telling of the beauties of this section on the posters put up advertising their mammoth circus. The Ringling Brothers have the welfare of this entire section at heart and we know that any advertising put out by them will be of the very best and will do Manatee county and the entire state a lot of good.",
      "Sarasota on the circus posters",
      "The circus as an advertising medium for the town: the promise of Sarasota travels with the posters of “the greatest show on earth”."),
]

CITY = [
    u(1, GR + ", p. 175",
      "A plea was made to the state legislature for a city charter—and it was granted. Governor Park Trammel signed the enabling statute May 16, 1913, to become effective January 1, 1914. The new charter provided for a mayor and three councilmen, to be elected by wards. It stipulated that for ordinary purposes, the rate of taxation should not exceed ten mills on the dollar and that special taxes “may be levied not exceeding ten mills for a sinking fund, not exceeding five mills exclusively for street work, and not exceeding one mill for city advertising.” … The honor of being the first mayor of the newly-incorporated City of Sarasota was given to Arthur B. Edwards at the first election authorized by the new charter. Citizens cast their ballots December 6, 1913. Edwards received 108 votes and his opponent, William Worth, 63.",
      "A city, with a mill for advertising",
      "The charter itself (Laws of Florida 1913) has not yet been read; the clause in quotation marks is as Grismer gives it. A city that may tax itself to advertise: the promotion that companies and land agents had paid for becomes a public duty. 171 votes were cast."),
    u(2, GR + ", p. 174",
      "The only disturbing note in the whole program was a statement made by Prof. Yarbrough that the school had suffered badly during the term because of the heavy turnover of teachers, due to the fact that they were paid only $50 and $55 a month—and it cost them that much to live.",
      "Fifty dollars a month",
      "At the first graduation of Sarasota's high school, in 1914, as Grismer reports it from the Sarasota Times. The school was for white pupils; for the Black school see module 2 (“The lean years”, [5]) and module 4."),
]

COLOUR = [
    u(1, "NAACP, Thirty Years of Lynching in the United States, 1889–1918 (1919), p. 55",
      "1903. Mar. 9. THOMAS, HENRY. Parish, Manatee Co. Rape.",
      "Parrish, March 1903",
      "One line in the National Association for the Advancement of Colored People's list of persons lynched; the charge is the one given by those who killed him, not a finding. Parrish lies in the north of what was then Manatee County, which included Sarasota until 1921. The month is that of the Seaboard's arrival at Sarasota (module 2)."),
    u(2, "NAACP, Thirty Years of Lynching in the United States, 1889–1918 (1919), p. 56",
      "1912. July 4. ENGLISH, WM. Bradentown, Manatee Co. Insulting white woman.",
      "Bradentown, July 1912",
      "Lynched at the county seat on the Fourth of July, for an alleged “insult”, the year the Ringlings began building at Shell Beach. The list gives no lynching at Sarasota itself; it was compiled from newspapers and is incomplete by its own account."),
    u(3, GR + ", p. 179",
      "Flying inland, the passengers were given the opportunity to observe another type of habitation. Out on 33rd Street they could see tiny homes being erected by negroes in the colored community of Newtown, then being opened by Charles N. Thompson, not to make money but to provide the negroes with better places in which to live. Previously, their principal living quarters had been at Black Bottom, in the vicinity of 12th and Lemon.",
      "Newtown, about 1914",
      "Grismer describes Newtown as the passengers of a flight over the town saw it, in the years about 1914. The motive he gives to Thompson, “not to make money”, is his own. Newtown lay north of the city limits; whether it should belong to the city was argued in 1926 (module 4)."),
]

SRC = ("Chicago Sunday Tribune, 23 January 1910; NAACP, Thirty Years of Lynching in the United States, 1889–1918 (New York, 1919); "
       "Karl H. Grismer, The Story of Sarasota (1946; copyright not renewed): Internet Archive. Manatee River Journal, 1910–1919: Florida Digital Newspaper Library, University of Florida. All in the public domain.")

T = {
    "id": "rails", "titel": "Rails and patrons", "jahr": "1903–1920",
    "autor": "A Chicago land agent, the county paper, the NAACP's list of the lynched, and the town historian of 1946",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. The railroad of 1903 (module 2) made Sarasota reachable for winter residents with fortunes; this module follows the two families who changed the town most, the Palmers and the Ringlings, through what the press reported and what Grismer gathered. Grismer's scenes of Mrs. Palmer at her window are his invention and are not quoted. The violence of these years in Manatee County reaches the apparatus only through the NAACP's list; the county paper's reports of the two lynchings have not yet been read.",
    "sections": [
        {"id": "palmer", "titel": "Mrs. Potter Palmer (1910–1918)",
         "blurb": "In February 1910 Bertha Honoré Palmer of Chicago came to see Sarasota after her father had called on a land agent. Within months she had bought between 75,000 and 100,000 acres from Sarasota to Venice, built a winter home at Osprey, founded a cattle ranch on the Myakka and a company to sell small farms. She died at Osprey in 1918.",
         "plates": ["trib1910_lord", "grismer1946_palmer", "mrj1910_colony", "mrj1916_myakka", "mrj1918_death"], "viz": "rails-acre", "units": PALMER},
        {"id": "ringling", "titel": "The circus men (1911–1919)",
         "blurb": "In 1911 John Ringling came to fish and bought a house on the bay; his brother Charles followed. Within a few years the Ringlings held land across the town, and in 1919 they promised to advertise Sarasota on their circus posters.",
         "plates": ["mrj1911_ringling", "mrj1919_ringadv"], "units": RINGLING},
        {"id": "city", "titel": "A city (1913–1914)",
         "blurb": "In 1913 the town asked for a city charter. It allowed a tax for streets, one for debt, and one mill for advertising the city.",
         "plates": ["grismer1946_main1910"], "units": CITY},
        {"id": "colour", "titel": "The colour line (1903–1914)",
         "blurb": "Two Black men were lynched in Manatee County in these years, at Parrish in 1903 and at Bradentown in 1912. About 1914 Black families began building homes in Newtown, north of the city, moving from Black Bottom near 12th and Lemon.",
         "plates": ["naacp1919_p55", "naacp1919_p56"], "units": COLOUR},
    ],
}
for s in T["sections"]:
    s["zk"] = "Rails and patrons, " + re.sub(r" \(.*", "", s["titel"])
(D / "rails.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UF = "Florida Digital Newspaper Library, University of Florida; public domain."
IA = "Internet Archive; public domain."
NEW = [
    {"id": "trib1910_lord", "side": "promise", "titel": "Lord's advertisement, 1910",
     "caption": "“FLORIDA … in the famous Sarasota Bay district of Manatee County, on the gulf.” J. H. Lord's advertisement in the farm-lands columns of the Chicago Sunday Tribune, the issue in which, Grismer says, Mrs. Palmer found Sarasota.",
     "source": "Chicago Sunday Tribune, 23 January 1910, part X, p. 13, detail. " + IA},
    {"id": "grismer1946_palmer", "side": "colony", "titel": "Mrs. Potter Palmer",
     "caption": "Bertha Honoré Palmer, “—Changed the course of Sarasota's history”, in Grismer's book.",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 158. " + IA},
    {"id": "mrj1910_colony", "side": "promise", "titel": "“Planning for a Florida Colony”, 1910",
     "caption": "Between 75,000 and 100,000 acres from Sarasota to Venice, a railroad extension, bungalows for the Palmers, a “society circle”, and nothing sold to colonists under $100 an acre.",
     "source": "Manatee River Journal, 30 June 1910, p. 1, detail. " + UF},
    {"id": "mrj1916_myakka", "side": "work", "titel": "Mrs. Palmer and the engineers, 1916",
     "caption": "“Government Aid in Dredging the Miakka Would Reclaim Thousands of Acres of Fertile Lands”: Mrs. Palmer before the Board of Engineers in Washington.",
     "source": "Manatee River Journal, 20 April 1916, p. 8, detail. " + UF},
    {"id": "mrj1918_death", "side": "colony", "titel": "Death at Osprey, 1918",
     "caption": "“Mrs. Potter Palmer Died Sunday at Her Winter Home at Osprey.”",
     "source": "Manatee River Journal, 9 May 1918, p. 1, detail. " + UF},
    {"id": "mrj1911_ringling", "side": "colony", "titel": "“Circus Man Buys Home”, 1911",
     "caption": "John Ringling, fishing at Sarasota with his wife, buys the winter home of C. N. Thompson. Beside it, the city of Bradentown sells $45,000 in bonds.",
     "source": "Manatee River Journal, 31 August 1911, p. 1, detail. " + UF},
    {"id": "mrj1919_ringadv", "side": "promise", "titel": "On the circus posters, 1919",
     "caption": "“Ringling to Advertise Sarasota and West Coast”: stickers on the circus posters “telling of the beauties of this section”.",
     "source": "Manatee River Journal, 27 November 1919, p. 3, detail. " + UF},
    {"id": "grismer1946_main1910", "side": "town", "titel": "Sarasota in 1910",
     "caption": "“Sarasota as it was in 1910”: above, Lower Main from Palm Avenue; below, looking west from the Five Points, with water from the watering trough running down the unpaved street and the water oaks that, Grismer notes, Gillespie had planted in 1886.",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 168. " + IA},
    {"id": "naacp1919_p55", "side": "law", "titel": "Florida, 1900–1909",
     "caption": "The NAACP's chronological list of persons lynched in Florida, 1900–1909, among them “THOMAS, HENRY … Parish, Manatee Co.”, 9 March 1903.",
     "source": "NAACP, Thirty Years of Lynching in the United States, 1889–1918 (1919), p. 55. " + IA},
    {"id": "naacp1919_p56", "side": "law", "titel": "Florida, 1910–1917",
     "caption": "The list continued, among them “ENGLISH, WM. … Bradentown, Manatee Co. … Insulting white woman”, 4 July 1912.",
     "source": "NAACP, Thirty Years of Lynching in the United States, 1889–1918 (1919), p. 56. " + IA},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = P["credit"].replace("the Monthly Weather Review,", "the Chicago Sunday Tribune of 1910, the NAACP's Thirty Years of Lynching (1919), the Monthly Weather Review,")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "rails"), None) or next(x for x in M["shipped"] if x["id"] == "rails")
M["planned"] = [x for x in M["planned"] if x["id"] != "rails"]
m.update({"datei": "rails", "zk": "Palmer · Ringling · City · Colour line",
          "kurz": "3 · Rails and patrons",
          "warum": "After the railroad, the patrons: Bertha Palmer of Chicago bought up to 100,000 acres from 1910, John and Charles Ringling bought on the bay from 1911 and promised to advertise Sarasota on their circus posters. The town became a city in 1913 with a mill of tax for advertising. Two Black men were lynched in Manatee County; Newtown was begun about 1914.",
          "quelle": "Chicago Sunday Tribune 1910; Manatee River Journal 1910–1919; NAACP 1919; Grismer (1946)."})
order = ["prospectus", "village", "rails", "boom", "bust", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "rails"] + [m], key=lambda x: order.index(x["id"]))
ADD = [
    {"id": "lynch1903", "side": "law", "kurz": "Henry Thomas (1903) and William English (1912)",
     "warum": "Both lynchings are printed here only from the NAACP's list of 1919. The reports of the county paper and of the Tampa press, which would tell what happened and who took part, have not yet been read against the page image.",
     "quelle": "Manatee River Journal, March 1903 and July 1912."},
    {"id": "charter1913", "side": "town", "kurz": "The city charter of 1913",
     "warum": "The act of the Florida legislature granting the charter has not been read at its source; its clause on advertising is quoted from Grismer.",
     "quelle": "Laws of Florida 1913."},
    {"id": "directory1916", "side": "colour", "kurz": "The directory of 1916",
     "warum": "The Bradentown city directory of 1916 includes Sarasota and marks each resident as white or coloured; counted, it would show where Black and white residents lived and worked. It has not yet been read through.",
     "quelle": "Bradentown City Directory 1916 (UFDC AA00053890)."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "thompsonhome", "titel": "Who bought the Thompson home?",
     "frage": "When and how did John Ringling come to own a house at Sarasota?",
     "note": "A Tampa paper reported on 28 August 1911 that Ringling had bought the winter home of C. N. Thompson. Grismer, from the county's deed records, has Ralph C. Caples buy it on 3 November 1911 and resell it to Ringling on 31 January 1912. The newspaper may have reported an agreement before the deeds, or a rumour.",
     "voices": [{"text": "rails", "sec": "ringling", "n": [1], "wer": "Tampa Times, August 1911"},
                {"text": "rails", "sec": "ringling", "n": [2], "wer": "Karl H. Grismer, 1946"}]},
    {"id": "acres", "titel": "Land in one hand",
     "frage": "How much land did the great buyers take, and at what price?",
     "note": "In 1884 the Edinburgh company contracted for 47,000 acres at $3.40 an acre. In 1910 the county paper reported that Mrs. Palmer had bought between 75,000 and 100,000 acres and would sell none to colonists for less than $100 an acre; Grismer gives more than 80,000.",
     "voices": [{"text": "prospectus", "sec": "prospectus", "n": [6], "wer": "Prospectus, 1884"},
                {"text": "rails", "sec": "palmer", "n": [3], "wer": "Manatee River Journal, June 1910"},
                {"text": "rails", "sec": "palmer", "n": [4], "wer": "Karl H. Grismer, 1946"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/rails/"
LINK = {
    "The circus man buys a home": (K + "ringling/1", "Rails and patrons [ringling 1]", "mrj1911_ringling"),
    "Newtown": (K + "colour/3", "Rails and patrons [colour 3]", None),
}
for s in TL["stations"]:
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], pl = LINK[s["titel"]]
        if pl:
            s["plate"] = pl
NEWST = [
    {"d": "9 March 1903", "side": "law", "titel": "Lynched at Parrish",
     "text": "Henry Thomas is lynched at Parrish, in Manatee County, the month the railroad reaches Sarasota.",
     "cite": K + "colour/1", "citeLabel": "Rails and patrons [colour 1]", "plate": "naacp1919_p55",
     "quelle": "NAACP, Thirty Years of Lynching (1919), p. 55."},
    {"d": "10 February 1910", "side": "colony", "titel": "Mrs. Palmer arrives",
     "text": "Bertha Honoré Palmer of Chicago arrives in a private car with her sons, her father and her brother; she calls the town “refreshingly quaint”.",
     "cite": K + "palmer/2", "citeLabel": "Rails and patrons [palmer 2]", "plate": "grismer1946_palmer",
     "quelle": "Grismer (1946), p. 157."},
    {"d": "30 June 1910", "side": "promise", "titel": "75,000 to 100,000 acres",
     "text": "The county paper reports Mrs. Palmer's purchase from Sarasota to Venice: none of it “to be sold to colonist at less than $100.00 per acre”.",
     "cite": K + "palmer/3", "citeLabel": "Rails and patrons [palmer 3]", "plate": "mrj1910_colony",
     "quelle": "Manatee River Journal, 30 June 1910, p. 1."},
    {"d": "4 July 1912", "side": "law", "titel": "Lynched at Bradentown",
     "text": "William English is lynched at Bradentown, the county seat, on a charge of “insulting white woman”.",
     "cite": K + "colour/2", "citeLabel": "Rails and patrons [colour 2]", "plate": "naacp1919_p56",
     "quelle": "NAACP, Thirty Years of Lynching (1919), p. 56."},
    {"d": "16 May 1913", "side": "town", "titel": "A city charter",
     "text": "The Governor signs Sarasota's city charter, which allows a tax of up to “one mill for city advertising”.",
     "cite": K + "city/1", "citeLabel": "Rails and patrons [city 1]",
     "quelle": "Grismer (1946), p. 175."},
    {"d": "6 May 1918", "side": "colony", "titel": "Mrs. Palmer dies",
     "text": "Bertha Palmer dies at “The Oaks”, Osprey, on Sunday night, 5 May.",
     "cite": K + "palmer/6", "citeLabel": "Rails and patrons [palmer 6]", "plate": "mrj1918_death",
     "quelle": "Manatee River Journal, 9 May 1918, p. 1."},
    {"d": "27 November 1919", "side": "promise", "titel": "On the circus posters",
     "text": "The Ringlings announce stickers advertising Sarasota on the posters of their circus.",
     "cite": K + "ringling/3", "citeLabel": "Rails and patrons [ringling 3]", "plate": "mrj1919_ringadv",
     "quelle": "Manatee River Journal, 27 November 1919, p. 3."},
]
for s in NEWST:
    if s["titel"] == "Mrs. Palmer dies":
        s["d"] = "5 May 1918"
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
