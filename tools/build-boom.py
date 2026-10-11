"""Builds data/boom.json (module 4: The county and the boom, 1921–1926) and enters the module
in modules.json, plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md, section "Modul 4"):
  Manatee River Journal, 5 May 1921, p. 1 (UFDC AA00083046/01013) and 23 June 1921, p. 1 (AA00083046/01017);
  Monthly Weather Review, October 1921, pp. 569–570 (IA sim_monthly-weather-review_1921-10_49_10, n38–n39);
  Sarasota County, Florida: "A Land of Opportunities and Resources" (T. F. Arnold, about 1922; IA sarasota-county-1922);
  Sarasota: A City of Glorified Opportunity (about 1924; IA sarasotacityofglorifiedopportunity, PDF p. 4);
  Sarasota Herald, 17 and 29 November 1925, 19 February, 13 May and 18 August 1926 (UFDC AA00088925);
  Karl H. Grismer, The Story of Sarasota (1946), pp. 202–204, 212–213, 240 (IA storyofsarasotah00gris; not renewed).
Run from the site root: python tools/build-boom.py
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
MWR = "Monthly Weather Review, October 1921"
SH = "Sarasota Herald"

COUNTY = [
    u(1, MRJ + ", 5 May 1921, p. 1",
      "Monday night there was another meeting of the joint committees, and after considerable discussion the boundary line was agreed to as follows: Beginning at a point in the waters of the Gulf of Mexico, intersected by an extension of the line dividing townships 35 and 36; thence east along said line to the northeast corner township 36, range twenty, thence south on range line to the southwest corner township 37, range 21; thence east on the township line to the boundary of DeSoto county. All north of this boundary to remain as Manatee county, and all south to become Sarasota county.",
      "The line",
      "The joint committees had been named by a mass meeting at the courthouse in Bradentown; the paper reports the line they agreed on before the legislature acted. The courses are given as printed."),
    u(2, MRJ + ", 23 June 1921, p. 1",
      "J. R. BUNKLEY GIVEN PRELIMINARY HEARING. J. R. Bunkley, former convict guard, who is being held for the murder of a negro prisoner at Salt Springs was given a preliminary hearing before Judge O. K. Reaves yesterday afternoon. Bunkley was not represented by an attorney at the hearing. The state had three witnesses and the defendant produced several witnesses. After the testimony Judge Reaves fixed the defendant's bond at $5,000.00. There has been no statement from parties who are interested in the boy as to whether they will try and raise the bond or let Bunkley remain in jail until the Grand Jury meets in Sarasota county, which will be some time in November.",
      "A prisoner killed at Salt Springs",
      "The paper calls Bunkley a former convict guard and the dead man a prisoner; it does not name him or say why he was held at Salt Springs. The outcome of the case has not been found (see “What is missing”). “The boy” is how the paper refers to the guard."),
    u(3, MRJ + ", 23 June 1921, p. 1",
      "SARASOTA COUNTY OFFICIALS APPOINTED. Tuesday Governor Hardee appointed the officials for Sarasota county, with the exception of Tax Assessor and the Sheriff. These two officials were appointed yesterday, they are, Charles G. Strohmeyer, Tax Assessor, and B. D. Levi, Sheriff. Commissioners—Frank A. Walpole, first district. L. L. May, second district. E. J. Hayden, third district. P. E. Buchan, fourth distirct. Henry Hancock, fifth distirct. School Board—A. L. Joiner, first district. T. L. Livermore, second district. Mrs. Westley Higel, third district. …",
      "The first officials",
      "The article stands directly below the report on Bunkley ([2]) on the same page. Mrs. Westley Higel on the school board is the only woman among the appointees."),
    u(4, GR + ", pp. 202–203",
      "Early on the morning of Thursday, January 6, 1921, the body of a man was seen lying in a pool of blood near the center of Beach Road on Siesta Key by Bert Luzier and his son Merle. … He was Harry L. Higel, one of Sarasota's most beloved and respected citizens! … Suspicion centered on Rube Allyn, former editor of the Sarasota Sun. … Placed under arrest, Allyn was brought to Sarasota from his home on Siesta Key. A mob began gathering. A rope was hurriedly secured and a hangman's knot drawn. However, before the mob took the law into its own hands, the sheriff appeared and whisked Allyn away to Bradenton. A coroner's jury ordered him held on a charge of murder. Allyn was held in jail in Bradenton for 61 days. Then the grand jury decided that a true bill could not be returned against him, inasmuch as all the evidence against him was circumstantial. So Allyn was released.",
      "A mob with a rope",
      "The meeting that made Sarasota a town in 1902 was held in Higel's office on the wharf (module 2); Grismer counts five terms as councilman and three as mayor. Grismer adds that the murderer “never paid the penalty for his crime”. A mob ready to hang a white suspect in January 1921 stands beside the Black prisoner killed in a convict camp ([2]) in the year the county began."),
]

STORM = [
    u(1, MWR + ", p. 570",
      "Loss of life.—So far as known the loss of life was small—not exceeding five or six—due, no doubt, to the fact that shipping remained in port. … Intrastate loss.—The citrus crop sustained a loss 800,000 to 1,000,000 boxes of fruit, approximating a monetary loss of more than $1,000,000. The loss of trees was not great; in fact, the damage from that source was slight. Truck crops adjacent to the coast were greatly damaged—a complete loss in many instances. And the loss of fertilizer and labor greatly augments the disaster, totaling, no doubt, $1,000,000 or more. … Miscellaneous damage.—The damage to residences, docks, warehouses, buildings, bridges, and miscellaneous property, at Tampa, Tarpon Springs, St. Petersburg, Sarasota, Punta Gorda, Marco, Caxambus, and Fort Myers; in short, along the coast from a point near Cedar Keys, southward, will exceed $1,000,000, and the aggregate of losses will probably total $3,000,000.",
      "The Weather Bureau's account",
      "The centre of the storm of 25 October 1921 “passed inland just north of Tampa” (p. 569); at Tampa the tide was 10.5 feet, “the highest since 1848” (p. 570). Sarasota is one name in a list. The report counts boxes of fruit and dollars; the fishermen whose houses stood on the water are in the next passage."),
    u(2, GR + ", p. 204",
      "The storm started with a slow rain Saturday afternoon, October 22, 1921. By Sunday morning the slow rain had become a downpour which continued hour after hour without letup. Then, at 9 p.m. Monday, winds of hurricane strength, coming out of the southwest, hit the city. The wind moaned and howled—and water kept piling into the bay, flooding the waterfront. In the city, the hurricane did little damage—but it wreaked havoc down on the bayfront. First the small boat houses began breaking up. Then the railroad dock began to disintegrate, and the wholesale fish house of John Savarese was destroyed. After that, in rapid succession, went the other fish houses, and many fishing boats and launches, and thousands of dollars worth of nets. A large part of the municipal pier was washed away—and all the other docks.",
      "The bayfront",
      "Grismer heads the section “A Hurricane Cleans the Waterfront”: the town had wanted the “unsightly” fish houses moved from its “front yard” before the storm (p. 203). The fishermen, he writes, “had no other place to go”. In his telling the storm did for the town what it had not done itself."),
]

SELLING = [
    u(1, "Sarasota County, Florida: “A Land of Opportunities and Resources” (published by T. F. Arnold, about 1922), p. [1]",
      "Sarasota County, where Homeseekers, Sportsmen or Tourists will find a place of rest and the opportunity to get away from the mad rush and artificiality of the large cities or long settled, set-in-their ways and not so favored by nature communities, is in that part of Florida where it is indeed June time all the time. Swept by the invigorating, health prolonging breezes from the once seen, always remembered, waters of Sarasota Bay and the Gulf of Mexico, and lying far enough south to be free from chilling frost dangers and discomforts, this county with only twenty degrees difference between mean summer and winter climate offers 365 genuine growing days in the year and the opportunity to live out doors all the time. If you are looking for the opportunity and place to obtain real relaxation, a place to make a home for your family among the kind of people you want them to mingle with or the chance to see Semi-Tropical Florida at its best, the pages of this booklet are worth your consideration.",
      "“Among the kind of people you want them to mingle with”",
      "The date “ca. 1922” is a librarian's pencil note on the cover. Thirty-eight years after the Edinburgh prospectus (module 1), the county is again “free from chilling frost”. The phrase about “the kind of people” names no one. In a town whose Black residents lived apart, and where the Klan paraded three years later ([3] in “The colour line”), it can be read as a promise of whom a buyer would not meet; the booklet does not say."),
    u(2, "Sarasota: A City of Glorified Opportunity (about 1924), p. [4]",
      "… advantages could not long be overlooked by the all-seeing eye of Capital, and for several years a number of nationally known men of great wealth have made it their home. They have been quietly investing and developing plans which soon will make Sarasota a storm center of opportunity. Tens of thousands of acres of surrounding territory have been cleared, drained and set out in citrus groves under highly scientific supervision, and tens of thousands more are in process of preparation to accommodate the hosts of prospective tenants. … The neighboring Keys soon will be linked to the main land by additional bridges and causeways, and modern highways will be constructed in furtherance of a plan that will make these Keys the theater of the most ambitious and artistic landscape development ever attempted in Florida.",
      "“The all-seeing eye of Capital”",
      "The booklet names none of its “men of great wealth”; the winter residents with great fortunes, the Palmers and the Ringlings, are followed in module 3. The keys are Lido, St. Armands and Longboat, on which John Ringling's company was building ([5])."),
    u(3, "Sarasota: A City of Glorified Opportunity (about 1924), p. [4]",
      "Civic spirit runs high and team work is everywhere in evidence. Clubs, societies, churches, banks, schools and private citizens are united in the onward movement toward the great goal—namely, to make Sarasota a city of twenty-five thousand permanent residents within the next five years with more than double that number in winter. Nor is this aspiration unjustified. … Sarasota is indeed favored of God and man.",
      "Twenty-five thousand in five years",
      "The census of 1930 counted 8,398 people in the city (see the graphic). The booklet gives the game its title: a city “of glorified opportunity”."),
    u(4, SH + ", 17 November 1925, p. 7",
      "“People are actually leaving Sarasota because they can find no place to live,” said J. Walker Davis, senior member of the firm, and the situation has reached a really critical point. It should be realized that every person who comes to Sarasota as a visitor is a possible and even probable permanent resident.",
      "No place to live",
      "From the article “Locating Rooms”: a real estate firm offers its staff to the Chamber of Commerce for a canvass of rooms for visitors. On the same page, in the next column, the Klan's circus ([3] in “The colour line”)."),
    u(5, SH + ", 19 February 1926, p. 24: advertisement of John Ringling Estates, Inc.",
      "JOHN RINGLING ESTATES. A HOMESITE SUBDIVISION. $3,000.00 AND UPWARD. All Improvements Guaranted Free From Assessment. Nowhere in the State of Florida is there an Opportunity Like This. Five minutes from the heart of the city over the magnificent Causeway, in surroundings unsurpassed, between beautiful, Sarasota Bay and the Gulf of Mexico. … The John Ringling Causeway Now Open to the Public. DAILY CONCERTS ON ST. ARMAND'S BY THE CZECHO-SLOVAKIAN NATIONAL BAND 2:00 P. M. TO 5:00 P. M. Free Busses from the Offices of John Ringling Estates, Inc. HOURLY ON THE HOUR.",
      "The causeway open",
      "“Guaranted” as printed."),
    u(6, GR + ", pp. 212–213",
      "The first concrete pile was driven to bedrock on the Sarasota side of the bay on January 1, 1925, and Ringling drove over the bridges just one year later. The causeway was opened to the public February 7, 1926. Ringling presented it to the city as a gift June 13, 1927, and it was accepted on January 31, 1928. At that time it was stated the causeway cost $750,000. On the day the causeway was formally opened, February 7, 1926, Ringling Estates also were opened to the public with the Czecho-Slovakian Band playing two concerts on St. Armands. It was reported that sales on the opening day exceeded a million dollars—probably this total included “pre-opening” sales made to prospects who had been taken to the islands, before the causeway was completed, in rowboats and launches.",
      "A million dollars in a day",
      "Grismer's “reported” and “probably” are his own caution. The Herald's advertisements of April 1926 call it “the new $1,000,000 John Ringling Causeway” (OCR, not read against the image); Grismer's $750,000 is the figure given when the city accepted it."),
]

COLOUR = [
    u(1, GR + ", p. 240",
      "… and the Booker High School, for colored pupils, at a cost of $21,000. By October, 1925, the schools were so badly crowded that two shifts of teachers had to be employed. Students attended only part time.",
      "A school “for colored pupils”",
      "Grismer lists the schools built in the boom with their cost."),
    u(2, SH + ", 13 May 1926, p. 9",
      "ARRESTS NEGRO. Willie Johnson was arrested last night in Newtown by “Wildcat” Morgan, colored police sergeant, on a charge of drunkenness and disturbing the peace. Previously in the evening, Morgan assisted in apprehending a negro named Bookertree who has been taken to Georgia where he is wanted for jail breaking.",
      "“Colored police sergeant”",
      "Sam Morgan, called “Wildcat”, policed Newtown for the city; the Herald reports his arrests repeatedly in 1925–26 (OCR of several issues). Newtown's residents appear in the paper of the boom mostly in such notes."),
    u(3, SH + ", 17 November 1925, p. 7",
      "Approximately 150 local Klansmen attended the circus in full Klan regalia. A huge Klan parade was held immediately before the start of the evening's program.",
      "The Klan at the circus",
      "The “Klan circus” was a travelling show staged at the fair grounds under the auspices of the local Klan for a week in November 1925; the Herald announced it for weeks and reported a coronation of a Klan “Queen” and a wedding under the big top (OCR of 1, 7, 15 and 19 November, not read against the image)."),
    u(4, SH + ", 29 November 1925, p. 8: advertisement",
      "Knights of the Ku Klux Klan. No HONEST, RIGHT-THINKING, WHITE, AMERICAN can CONSCIENTIOUSLY oppose the Knights Of The Ku Klux Klan, however, some do because they DO NOT KNOW what its objects and purposes are. … The Klan has no fight to make on any men because of his RACE, COLOR, PLACE OF BIRTH, RELIGIOUS or POLITICAL AFFILLIATIONS. … The Klan stands for LAW and ORDER, Freedom of Speech and Press, Free Public Schools, Separation of Church and State, White Supremacy and Protestant Christianity. Thoes Interested Address P. O. Box 551 Sarasota",
      "“White Supremacy”",
      "A paid recruiting advertisement, printed here to show how openly the Klan presented itself in Sarasota's daily paper during the boom. It denies any fight over race and in the same column declares for “White Supremacy”. Spelling as printed. No act of violence by the Sarasota Klan has been found in the sources read; the apparatus does not supply one."),
    u(5, SH + ", 18 August 1926, p. 5",
      "Early yesterday morning six negroes were nabbed on disorderly conduct charges by “Wilcat” Sam Morgan. The men were said to have been engaged in a loud argument on the subject of whether or not Newtown, the new negro quarters, should be included in Greater Sarasota. Four of the men claimed that Newtown should be a portion of the city but the others held out, maintaining that it would be better to be out of the jurisdiction of the city police officers. Suddenly the argument turned into a free-for-all fight and just then the “Wildcat” appeared upon the scene. All six were lodged in county jail pending trial before Mayor Bacon Monday morning. After being placed in jail the four who had taken the side that Newtown should remain within the jurisdiction of the city officers changed their views and peace reigned.",
      "Inside the city, or outside?",
      "Under the headline “Jail Negroes for Fighting”. The paper tells it as a joke. Underneath it is a real question: what being inside the city would mean for Newtown — city services, or city police. “Greater Sarasota” is the paper's phrase. “Wilcat” as printed."),
    u(6, SH + ", 18 August 1926, p. 5",
      "$15,000 Negro Hostelry Will Be Built Here. Announcement of plans for the erection of a $15,000 negro hotel was made yesterday by E. O. Burns. The modern hostelry which will cater to the colored tourist trade will be situated on Central near Fourteenth street. It is also intended to use this hotel to aid in the alleviation of the housing situation existing in the quarters at present. The hotel will be named for a negro servant who worked in the home of Col. J. H. Gillespie, founder of Sarasota. The negro, Louis Colson, died about two years ago here. It is expected that a building permit for the structure will be applied for within the next few days.",
      "A hotel named for Lewis Colson",
      "In the same column as [5]. Lewis Colson (the Herald writes “Louis”) is one of the six Black residents named in the directory of 1897 (module 2). Whether the hotel was built has not been found; the Herald's digitized run ends a week later."),
]

SRC = ("Manatee River Journal, 5 May and 23 June 1921, and Sarasota Herald, November 1925 to August 1926: Florida Digital Newspaper Library, University of Florida. "
       "Monthly Weather Review, October 1921 (U.S. Weather Bureau); the booklets Sarasota County, Florida: A Land of Opportunities and Resources (T. F. Arnold, about 1922) and "
       "Sarasota: A City of Glorified Opportunity (about 1924), State Library of Florida; Karl H. Grismer, The Story of Sarasota (1946; copyright not renewed): Internet Archive. All in the public domain.")

T = {
    "id": "boom", "titel": "The county and the boom", "jahr": "1921–1926",
    "autor": "The Bradentown paper, the Weather Bureau, the town's booklets and its daily paper of the boom, and the town historian of 1946",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission. Most of the voices of this module sold Sarasota: booklets, advertisements, a daily paper founded at the height of the boom. The Black residents of Newtown appear in it through police notes, a school's cost and a hotel planned by a white builder; where their own view is missing, the apparatus says so. The Sarasota Herald is digitized only from October 1925 to August 1926; the collapse that followed is told in module 5.",
    "sections": [
        {"id": "county", "titel": "A county of its own (1921)",
         "blurb": "In 1921 the south of Manatee County became Sarasota County, after months of meetings over where the line should run. The year began with the murder of a former mayor and a mob with a rope, and in June, in the week the Governor named the county's first officials, a former convict guard was held for the murder of a Black prisoner at Salt Springs.",
         "plates": ["mrj1921_boundary", "mrj1921_bunkley"], "units": COUNTY},
        {"id": "storm", "titel": "The storm (October 1921)",
         "blurb": "Four months after the county's founding a hurricane struck the Gulf coast. The Weather Bureau counted losses in boxes of fruit and dollars; in Sarasota it destroyed the fish houses on the bayfront that the town had wanted gone.",
         "plates": ["mwr1921_damage"], "units": STORM},
        {"id": "selling", "titel": "Selling the boom (1922–1926)",
         "blurb": "Booklets promised June all the time, freedom from frost and “the kind of people you want them to mingle with”; one set a goal of twenty-five thousand residents in five years. In the season of 1925–26 there were not enough rooms, and on 7 February 1926 John Ringling's causeway opened the keys to buyers of lots.",
         "plates": ["arnold1922_cover", "glor1924_cover", "glor1924_goal", "herald1926_causeway"], "viz": "boom-promise", "units": SELLING},
        {"id": "colour", "titel": "The colour line in the boom (1924–1926)",
         "blurb": "The boom was built on a divided town. Black children went to Booker school, Newtown had its own Black police sergeant, and the Klan paraded in robes at the circus and advertised for members in the daily paper. In August 1926 six men from Newtown argued over whether their quarter should belong to the city, and a builder announced a hotel for Black tourists named for Lewis Colson.",
         "plates": ["herald1925_klan", "herald1925_klanad", "herald1926_morgan", "herald1926_newtown"], "units": COLOUR},
    ],
}
for s in T["sections"]:
    s["zk"] = "The boom, " + re.sub(r" \(.*", "", s["titel"])
(D / "boom.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UF = "Florida Digital Newspaper Library, University of Florida; public domain."
IA = "Internet Archive; public domain."
SLF = "State Library of Florida, via Internet Archive; Public Domain Mark."
NEW = [
    {"id": "mrj1921_boundary", "side": "town", "titel": "Where the line should run, 1921",
     "caption": "The Bradentown paper reports the boundary agreed by the joint committees: all north to remain Manatee County, “and all south to become Sarasota county.”",
     "source": "Manatee River Journal, 5 May 1921, p. 1, detail. " + UF},
    {"id": "mrj1921_bunkley", "side": "law", "titel": "Salt Springs and the new county, 1921",
     "caption": "Two items on one page: a former convict guard held for the murder of a Black prisoner at Salt Springs, and the Governor's appointment of the officials of Sarasota County.",
     "source": "Manatee River Journal, 23 June 1921, p. 1, detail. " + UF},
    {"id": "mwr1921_damage", "side": "work", "titel": "The hurricane of October 1921",
     "caption": "The Weather Bureau on the losses: citrus, truck crops “a complete loss in many instances”, and damage to docks and buildings at Tampa, Tarpon Springs, St. Petersburg, Sarasota and southward.",
     "source": "Monthly Weather Review, October 1921, p. 570, detail. " + IA},
    {"id": "arnold1922_cover", "side": "promise", "titel": "“A Land of Opportunities and Resources”",
     "caption": "The cover of a promotional booklet of about 1922: “A Glimpse of Sarasota from the Air”, the town on the bay with the pier and the railroad.",
     "source": "Sarasota County, Florida (published by T. F. Arnold, about 1922), cover. " + SLF},
    {"id": "glor1924_cover", "side": "promise", "titel": "“A City of Glorified Opportunity”",
     "caption": "The cover of a booklet of about 1924: a golfer, a woman on water skis, a parasol on the beach. Its title is the title of the companion game.",
     "source": "Sarasota: A City of Glorified Opportunity (about 1924), cover. " + SLF},
    {"id": "glor1924_goal", "side": "promise", "titel": "Twenty-five thousand in five years",
     "caption": "“… to make Sarasota a city of twenty-five thousand permanent residents within the next five years with more than double that number in winter.”",
     "source": "Sarasota: A City of Glorified Opportunity (about 1924), p. [4], detail. " + SLF},
    {"id": "herald1926_causeway", "side": "promise", "titel": "The causeway open, 1926",
     "caption": "John Ringling Estates: homesites from $3,000, “Five minutes from the heart of the city over the magnificent Causeway”, daily concerts on St. Armands, free buses every hour.",
     "source": "Sarasota Herald, 19 February 1926, p. 24, advertisement, detail. " + UF},
    {"id": "herald1925_klan", "side": "law", "titel": "Rooms, and the Klan, 1925",
     "caption": "One page of the boom: “People are actually leaving Sarasota because they can find no place to live”, and, in the next column, “Approximately 150 local Klansmen attended the circus in full Klan regalia.”",
     "source": "Sarasota Herald, 17 November 1925, p. 7, detail. " + UF},
    {"id": "herald1925_klanad", "side": "law", "titel": "A Klan advertisement, 1925",
     "caption": "“Knights of the Ku Klux Klan”: a recruiting advertisement in the daily paper, ending with “White Supremacy and Protestant Christianity” and a Sarasota post office box. The large pencilled “30” is a later mark on the copy that was filmed.",
     "source": "Sarasota Herald, 29 November 1925, p. 8, detail. " + UF},
    {"id": "herald1926_morgan", "side": "colour", "titel": "“Colored police sergeant”, 1926",
     "caption": "“Willie Johnson was arrested last night in Newtown by ‘Wildcat’ Morgan, colored police sergeant …”",
     "source": "Sarasota Herald, 13 May 1926, p. 9, detail. " + UF},
    {"id": "herald1926_newtown", "side": "colour", "titel": "Newtown and the city, 1926",
     "caption": "“Jail Negroes for Fighting”: six men argue whether Newtown should be part of Greater Sarasota; beside it, “$15,000 Negro Hostelry Will Be Built Here”, to be named for Louis (Lewis) Colson.",
     "source": "Sarasota Herald, 18 August 1926, p. 5, two column sections set side by side. " + UF},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = ("Pages of The Economist, The Atlanta Constitution, the Chicago Daily Tribune, Time (London), the Monthly Weather Review, a Florida gazetteer and Karl H. Grismer's Story of Sarasota (1946): Internet Archive. "
               "Promotional booklets of about 1922 and 1924: State Library of Florida, via Internet Archive. Florida Reports: Caselaw Access Project, Harvard Law School Library. "
               "The Pensacolian, the Manatee River Journal and the Sarasota Herald: Florida Digital Newspaper Library, University of Florida. All in the public domain.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "boom"), None) or next(x for x in M["shipped"] if x["id"] == "boom")
M["planned"] = [x for x in M["planned"] if x["id"] != "boom"]
m.update({"datei": "boom", "zk": "County · Storm · Selling · Colour line",
          "kurz": "4 · The county and the boom",
          "warum": "In 1921 Sarasota became the seat of its own county, in a year of a mob with a rope, a Black prisoner killed at a convict camp and a hurricane on the bayfront. In the boom of 1925–26 booklets promised twenty-five thousand residents, John Ringling's causeway opened the keys, the Klan paraded and advertised, and Newtown argued whether to belong to the city.",
          "quelle": "Manatee River Journal 1921; Monthly Weather Review 1921; booklets of about 1922 and 1924; Sarasota Herald 1925–26; Grismer (1946)."})
order = ["prospectus", "village", "rails", "boom", "bust", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "boom"] + [m], key=lambda x: order.index(x["id"]))
for x in M["missing"]:
    if x["id"] == "bunkley":
        x["warum"] = ("The Manatee River Journal of 23 June 1921 reports that a former convict guard, J. R. Bunkley, was held for the murder of a Black prisoner at Salt Springs and bound over to the grand jury of Sarasota County (printed in module 4). "
                      "The prisoner is not named, and the outcome — indictment, trial, verdict — has not been found. The county's court records and Florida's reports on its convict camps of 1921–22 would be needed.")
ADD = [
    {"id": "act1921", "side": "town", "kurz": "The act creating Sarasota County",
     "warum": "The act of the Florida legislature of 1921 that created the county has not yet been read at its source; the apparatus prints the boundary as the Bradentown paper reported it.",
     "quelle": "Laws of Florida 1921."},
    {"id": "newtownvoice", "side": "colour", "kurz": "Newtown in its own words",
     "warum": "The digitized papers of the boom were written by and for white Sarasota. No Black newspaper, church record or letter from Newtown in the 1920s has been found in a public-domain source; the quarter speaks here only through police notes and announcements.",
     "quelle": "To be found."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "frost", "titel": "Below the frost line",
     "frage": "What did Sarasota promise about its winters, and what happened?",
     "note": "In 1884 an Edinburgh prospectus sold land on the bay as lying “below the frost line”; a colonist remembered the snow of January 1886. In about 1922 a county booklet promised a place “free from chilling frost dangers and discomforts”. The promise outlived the colony by forty years.",
     "voices": [{"text": "prospectus", "sec": "prospectus", "n": [6], "wer": "Florida Mortgage and Investment Co., 1884"},
                {"text": "prospectus", "sec": "colony", "n": [5], "wer": "Alex Browning, January 1886"},
                {"text": "boom", "sec": "selling", "n": [1], "wer": "County booklet, about 1922"}]},
    {"id": "keys", "titel": "The keys",
     "frage": "How were the keys sold?",
     "note": "A booklet of about 1924 announced that the keys would become “the theater of the most ambitious and artistic landscape development ever attempted in Florida”. In February 1926 the causeway opened with concerts and free buses; the town historian of 1946 doubted the million dollars of sales reported for the first day.",
     "voices": [{"text": "boom", "sec": "selling", "n": [2], "wer": "Booklet, about 1924"},
                {"text": "boom", "sec": "selling", "n": [5], "wer": "John Ringling Estates, February 1926"},
                {"text": "boom", "sec": "selling", "n": [6], "wer": "Karl H. Grismer, 1946"}]},
    {"id": "mob", "titel": "Two killings, 1921",
     "frage": "How did the law meet violence in the county's first year?",
     "note": "In January 1921 a mob gathered a rope for a white man suspected of killing a former mayor; the sheriff took him away and he was released for want of evidence. In June a white guard was bound over for the murder of a Black prisoner whom the paper does not name. What became of that case is not known.",
     "voices": [{"text": "boom", "sec": "county", "n": [4], "wer": "Karl H. Grismer, 1946"},
                {"text": "boom", "sec": "county", "n": [2], "wer": "Manatee River Journal, June 1921"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/boom/"
LINK = {
    "A guard held for murder": (K + "county/2", "The boom, 1921 [2]", "mrj1921_bunkley"),
    "The Klan at the circus": (K + "colour/3", "The colour line in the boom [3]", "herald1925_klan"),
    "A hotel for the colored tourist trade": (K + "colour/6", "The colour line in the boom [6]", "herald1926_newtown"),
}
for s in TL["stations"]:
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], s["plate"] = LINK[s["titel"]]
NEWST = [
    {"d": "6 January 1921", "side": "law", "titel": "A mob with a rope",
     "text": "Harry L. Higel, three times mayor, is found dying on Siesta Key. When a suspect is brought to Sarasota, “a mob began gathering. A rope was hurriedly secured”; the sheriff takes him to Bradenton. He is released; the murder is never solved.",
     "cite": K + "county/4", "citeLabel": "The boom, 1921 [4]",
     "quelle": "Grismer, The Story of Sarasota (1946), pp. 202–203."},
    {"d": "May 1921", "side": "town", "titel": "The line",
     "text": "Committees in Bradentown agree on the line: “All north of this boundary to remain as Manatee county, and all south to become Sarasota county.”",
     "cite": K + "county/1", "citeLabel": "The boom, 1921 [1]", "plate": "mrj1921_boundary",
     "quelle": "Manatee River Journal, 5 May 1921, p. 1."},
    {"d": "25 October 1921", "side": "work", "titel": "The bayfront goes",
     "text": "A hurricane comes ashore north of Tampa. At Sarasota the fish houses, the railroad dock, boats and nets and most of the municipal pier are destroyed.",
     "cite": K + "storm/2", "citeLabel": "The boom, 1921 [storm 2]", "plate": "mwr1921_damage",
     "quelle": "Monthly Weather Review, October 1921, p. 570; Grismer (1946), p. 204."},
    {"d": "about 1924", "side": "promise", "titel": "Twenty-five thousand",
     "text": "A booklet sets “the great goal”: “a city of twenty-five thousand permanent residents within the next five years”.",
     "cite": K + "selling/3", "citeLabel": "The boom [selling 3]", "plate": "glor1924_goal",
     "quelle": "Sarasota: A City of Glorified Opportunity (about 1924), p. [4]."},
    {"d": "29 November 1925", "side": "law", "titel": "“White Supremacy”",
     "text": "The Klan advertises in the Sarasota Herald: it stands for “LAW and ORDER … White Supremacy and Protestant Christianity”.",
     "cite": K + "colour/4", "citeLabel": "The colour line in the boom [4]", "plate": "herald1925_klanad",
     "quelle": "Sarasota Herald, 29 November 1925, p. 8."},
    {"d": "7 February 1926", "side": "promise", "titel": "The causeway opens",
     "text": "John Ringling's causeway to St. Armands and Lido opens to the public; homesites from $3,000, concerts by the Czecho-Slovakian National Band.",
     "cite": K + "selling/5", "citeLabel": "The boom [selling 5]", "plate": "herald1926_causeway",
     "quelle": "Grismer (1946), pp. 212–213; Sarasota Herald, 19 February 1926, p. 24."},
    {"d": "17 August 1926", "side": "colour", "titel": "Inside the city?",
     "text": "Six men from Newtown are jailed after arguing whether “the new negro quarters, should be included in Greater Sarasota”.",
     "cite": K + "colour/5", "citeLabel": "The colour line in the boom [5]",
     "quelle": "Sarasota Herald, 18 August 1926, p. 5."},
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
