"""Builds data/prospectus.json (module 1: The prospectus and the colony, 1884–1888) and enters the module
in modules.json, plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md, section "Modul 1"):
  The Economist, 25 October 1884, p. 1313 (Internet Archive sim_economist_1884-10-25_42_2148, n28);
  Bacon, Andrews and Bidwell v. State, 22 Fla. 51 (January term 1886), pp. 52–53, 61–64, 85 (case.law scan);
  Anderson v. State, 24 Fla. 139 (January term 1888), pp. 140, 144, 147 (case.law scan);
  The Pensacolian, 31 January 1885, p. 4, after the Florida Times-Union (UFDC AA00083042/00060);
  The Atlanta Constitution, 27 July 1885, editorial page, after the Buffalo Express (IA per_atlanta-constitution_1885-07-27_18, n3);
  Chicago Daily Tribune, 6 February 1886, p. 5 (IA per_chicago-daily-tribune_the-chicago-daily-tribun_1886-02-06_46, n4);
  Florida State Gazetteer and Business Directory 1886–87, s.v. Sarasota (IA floridastategaze1886sout, n417);
  W. R. Lawson, "Scottish Colonies on the Gulf of Mexico", Time (London), April 1887, pp. 479–480 (IA sim_time-a-monthly-magazine_1887-04_16_28);
  Karl H. Grismer, The Story of Sarasota (1946), pp. 96–98 and plates (IA storyofsarasotah00gris; not renewed, public domain).
Run from the site root: python tools/build-prospectus.py
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


EC = "The Economist, 25 October 1884, p. 1313"
BA = "Bacon, Andrews and Bidwell v. State, 22 Fla. 51 (January term 1886)"
AN = "Anderson v. State, 24 Fla. 139 (January term 1888)"
GR = "Karl H. Grismer, The Story of Sarasota (1946)"
TR = "Chicago Daily Tribune, 6 February 1886, p. 5"
LW = "W. R. Lawson, “Scottish Colonies on the Gulf of Mexico”, Time (London), April 1887"

PROSPECTUS = [
    u(1, EC,
      "A LARGE PROPORTION OF THE PRESENT ISSUE HAS BEEN SUBSCRIBED. THE FLORIDA MORTGAGE & INVESTMENT CO., LMTD. To be Incorporated under the Companies' Acts, 1862 to 1884, whereby the Liability of each Shareholder is limited to the amount for which he subscribes. CAPITAL, £50,000, WITH POWER TO INCREASE. Present Issue £150,000, in 30,000 Shares of £5 each, of which it is intended to call up only £1 per Share, the Balance to form a Security for Debentures. 10s payable on Application, and 10s on Allotment.",
      "A company in Edinburgh",
      "So printed: a capital of £50,000 against a present issue of £150,000; one of the two figures is a misprint, most likely the first. The second “10s” is broken in the print; ten shillings on application and ten on allotment make up the pound to be called."),
    u(2, EC,
      "DIRECTORS. ROBERT W. HANBURY, Esq., of Ilam Hall, Staffordshire, J.P. and D.L. for Counties Stafford, Warwick and Derby—Chairman. Colin J. Mackenzie, Esq., of Portmore—Vice-Chairman. Sir John Gillespie, W.S., Edinburgh. Major Houstoun, of Clerkington, Haddington. David Pearson, Esq., C.A., Edinburgh. ADVISORY BOARD OF DIRECTORS IN AMERICA. John Paton, Esq., Banker, New York. J. J. Dunne, Esq., Vice-President Florida Land Improvement Co, Florida. T. De Witt Cuyler, Esq., Philadelphia (Law Agent in America to the Matador Cattle Co. of Dundee). … General Manager in Florida. Piers E. Warburton, Esq., Sarasota, Florida. Secretary—W. J. Caesar, C.A., Edinburgh. Head Office—No. 4a St. Andrew square, Edinburgh.",
      "The board",
      "The chairman in 1884 is Robert W. Hanbury, not Sir John Gillespie, whom Grismer (1946) calls the company's president; Gillespie sits on the board as a Writer to the Signet. No churchman is among the directors. Lawson in 1887 ([2] in “Verdicts”) names Hanbury and “Colonel Dunn” as the owners of the land."),
    u(3, EC,
      "This Company is formed for the purpose of investing money, by way of mortgage, on the security of freehold property in the State of Florida, U.S.A. In addition to the share capital to be invested in this way, the Company will borrow on debentures to an amount not exceeding the capital uncalled for the time being; and the money so received will be invested along with the share capital. The Company will have power to purchase, improve, cultivate, and resell lands and other properties; but it is not intended to develop this part of the business to any great extent.",
      "Mortgages, not colonists",
      "The prospectus offers a mortgage business. Land, the part that became the colony, is a side line it does not mean “to develop … to any great extent”."),
    u(4, EC,
      "Florida possesses an area equal to that of England and Wales, and in the development of its exceptionally wide range of industries and cultivation of its rich sub-tropical soil, is capable of sustaining a larger population than any other State in the American Union. The population has been almost doubled within the last three years, and it is indicative of the high reputation Florida bears on her own Continent that the immigrants are almost exclusively Americans and Canadians, and not Europeans. There is at present a large and highly remunerative field open to a Company of this kind, and there is at the same time an undoubted prospect of substantial and permanent success in the growing value of its properties. The present legal rate of interest in Florida is 8 per cent., which rate is binding in the absence of any special contract, but the demand for money is so great that from 10 to 15 per cent. can be readily obtained on first mortgages of freehold lands, and with an ample margin of security.",
      "Eight per cent., and more"),
    u(5, EC,
      "They have also been fortunate in securing the services of Mr Piers E. Warburton, of Sarasota, Florida, as general manager there. Mr Warburton has had great experience in the valuation and management of land in Australia, New Zealand, and various parts of the United States. He has been three years in Florida engaged in valuing and selecting lands, and has personally inspected and approved the property which the Company proposes to acquire.",
      "The manager on the spot"),
    u(6, EC,
      "A provisional contract has been entered into on behalf of the Company for the purchase of 47,000 acres of freehold land, situate on Sarasota Bay, Manatee County, Florida, comprising choice selections of land suitable for residental sites, and for the cultivation of oranges, bananas, pine apples, sugar, cotton, tobacco, rice, maize, etc., and nowhere in the State of Florida do these crops grow to greater advantage, as the lands are below the frost line, and the most delicate vegetables grown there in the open air are marketed in northern cities in the months of January and February, and in these months have the monopoly of the markets at high prices. The cost of the land is $3.40 (or about 14s) per acre.",
      "Below the frost line",
      "The promise that names this apparatus. Fourteen months later, in January 1886, the colonists saw snow fall (“The colony”, [5]); the frost of February 1895 is told in module 2."),
    u(7, EC,
      "The climate of Florida is the finest and probably the healthiest in the world. The mean temperature, as shown by the official Blue-Books (Department of Agriculture, 1882), ranges between 7[0] degrees in winter and 8[2] degrees in summer, and is not subject to great changes. It is now considered the sanitarium of the United States, and is the chief resort of invalids from the Northern and Western States. During the last winter the number of Northern visitors to the State equalled one-fourth of the resident population, and was only limited by the accommodation.",
      "The finest climate",
      "The last figure of each temperature is broken in the print; the readings in brackets are the editor's. The winter visitor, here a sentence in a prospectus, became Sarasota's business from the 1890s on."),
]

VIGILANCE = [
    u(1, "The Pensacolian, 31 January 1885, p. 4, after the Florida Times-Union",
      "In August last one Riley was mysteriously killed. All efforts to find out who murdered him were unavailing at the time. Fortunately, the murder of Abbe was witnessed, and when the citizens of Manatee, fifteen miles distant, heard of the affair they at once called a meeting, selected a posse, and, following up the clue given them by the witness, Morehouse, they pursued the scoundrels until every one of them in Manatee county was arrested and jailed.",
      "Two killings, August and December 1884",
      "Harrison T. Riley was killed in August 1884, the postmaster Charles E. Abbe on 27 December 1884 ([6]). The posse came from Manatee, the older settlement on the Manatee River, “fifteen miles distant”."),
    u(2, "The Pensacolian, 31 January 1885, p. 4, after the Florida Times-Union",
      "The good citizens of Manatee deserve the thanks of the people of Florida for the vigor with which they pursued the dastardly murderers of Riley and C. E. Abbe, and are to be congratulated on arresting and bringing them to justice. In doing this they unearthed a society of thugs at Sarasota, the existence of which had not been suspected by any one outside of the diabolical gang. … They had a ritual of the most terrible nature, and when an initiate objected to the devilish oath administered the blindfold was taken from his eyes and his attention was directed to a double-barrel gun standing conveniently near and he was informed that he could go on or take its contents then and there. In this way they augmented their number to upwards of twenty. Andrews and Bidwell were the heads of the concern, with the title of judges, and Allford was captain. … Our informant, who is one of the leading citizens of Manatee, tells us that it was with great difficulty the people were prevented from lynching all the rascals, and that they are determined that every one of them shall be properly punished.",
      "“A society of thugs”",
      "A Jacksonville paper's account from an unnamed informant in Manatee, reprinted in Pensacola. Its “Allford” is Jason L. Alford of the court records. The crowd that nearly lynched the prisoners is reported in passing; the article praises the people who held it back."),
    u(3, BA + ", p. 61: testimony of Louis L. Cato",
      "“I belonged to an organization at Sara Sota with a number of twenty-two members. That organization was carried on from one meeting to another until it was the cause of Harrison T. Riley's death.” With reference to the meeting at which Riley was sentenced to be killed, he says: “Dr. Andrews and Mr. Bidwell gave the orders to Jason Alford. Dr. Andrews said that this man Riley had to be killed, to be put out of the neighborhood; I mean Riley; said that he was taking property that did not belong to him from orphan children. Mr. Bidwell never said a word, except he seconded what Mr. Andrews said. Bidwell said, yes, it will have to be done.”",
      "“Riley had to be killed”",
      "Cato, indicted as one of the men who fired, testified for the State after being told he could refuse to say anything that would incriminate himself. The charge against Riley is the committee's own pretext; nothing in the record shows it to be true."),
    u(4, BA + ", p. 62: testimony of Louis L. Cato",
      "“The man Riley came along the road I was stationed on, myself, Ed. P. Bacon and Thos. L. Dryman; when he got a little past us we all three fired at Riley; we ran out to where he was lying on his back; he was not moving hand or foot; … Edmund Bacon fired the fourth gun, and I ran up and cut his throat. We all then got away from the place as quickly as we could.”",
      "On the road",
      "The killing as one of the men who did it described it in court. It is printed so that the victim is not reduced to a name; the apparatus does not add to it."),
    u(5, BA + ", p. 63: testimony of Louis L. Cato",
      "“We had that to do, the killing of Riley, to save our own lives. They, Dr. Andrews and Bidwell, Judges, said if we didn't do it we would have to be done the same way.” … “Judges of the organization were to preside at all meetings, administer all oaths, and read the by-laws every time. If one was not there the other had to do it. They were to make all orders for any work to be done, for any man who was to be whipped, or anything of that kind, or any man to be killed. That was their duty, to make all orders, and they were to talk to outside men to get them into membership. That was one of the by-laws. They were all numbered. They were to talk to men and be more than careful how they approached them for membership, and sound them in general standing as to their back-bone and grit before he was brought in for membership.”",
      "The judges and the by-laws"),
    u(6, BA + ", p. 64: testimony of Thomas L. Dryman",
      "“I knew Harrison T. Riley; I knew Edmond P. Bacon, Adam W. Hunter, Alfred B. Bidwell and Leonard F. Andrews. I was present at a meeting held in one of the Alford houses the Saturday night previous to the Monday Riley was killed. That was a meeting of an organization known as the Sara Sota Vigilance Committee, styled S. S. V. C. The members were, first, Jason Alford, Dr. Andrews, (identifies him,) Alfred B. Bidwell, John M. Tippett, Frank Jones, Dr. Hayden, Edmond P. Bacon, Joseph C. Anderson, John Fletcher, James Fletcher, Lucien Belk, Thomas Dryman, Bob Smallwood, Council F. Brown, Miles Brown, John Trowel, —— Bartholomew—I don't know him by his given name; that's all I can remember; …”",
      "“Sara Sota Vigilance Committee, styled S. S. V. C.”"),
    u(7, AN + ", p. 140",
      "… that Willard, with a shot gun in his hands, on the 27th of December, 1884, killed Charles E. Abbe, by shooting him in the head, the death following instantly, that the killing was done from premeditated design, and that plaintiff in error was present aiding and abetting the act. … As to the first, Morehouse, a witness for the State testified, in substance that about 11 o'clock on the 27th of December, 1884, he and Abbe were working on a boat, when a man came up who was introduced to him as Mr. Willard, the same person then on trial.",
      "The postmaster, 27 December 1884",
      "Charles E. Abbe was Sarasota's postmaster. The indictment charged Charles B. Willard with the killing and Joseph C. Anderson with aiding and abetting it."),
    u(8, AN + ", p. 144",
      "Another witness, Mrs. Alford, says she heard Anderson say he would as soon shoot Abbe as a snake, and that she had heard him say it twice, once three or four months back, and once longer before the alleged killing of Abbe. … Another witness, Jones, said he was at a party at Bidwell's house Christmas night, and talking with Anderson about some manufactured stuff in a jug, aquadente, and warning him to be careful. Anderson said yes, and damn that old Abbe, he has always been a curse to Sara Sota (the neighborhood in which they were), him and his clique. They have got about to the end of their halter, and they had better look out for themselves; that Abbe was always in some deviltry, and there was not a judge or jury in the State but would commend the man who would kill him.",
      "“A curse to Sara Sota”",
      "Two nights before the killing. Why Abbe was hated the record does not establish. The court's own words, “Sara Sota (the neighborhood in which they were)”, describe the place in 1884: a neighbourhood, not a town."),
    u(9, BA + ", pp. 52–53",
      "In the month of March, 1885, at the Spring Term of the Circuit Court held in and for the county of Manatee, Edmond P. Bacon, Louis L. Cato, Thomas Dryman and Adam W. Hunter, were indicted for the murder of one Harrison T. Riley, and Leonard F. Andrews, Jason L. Alford, Charles B. Willard, Joseph C. Anderson and Alfred B. Bidwell were indicted as accessories before the fact. At a special term of the court held on the fourteenth day of July, in the same year, such proceedings were had that there was severance of the defendants, and the court proceeded to try the defendants, Edmond P. Bacon, Leonard F. Andrews, Alfred B. Bidwell and Adam W. Hunter. The jury rendered the following verdict: “We, the jury, find Edmond P. Bacon guilty of the murder of Harrison T. Riley in the first degree, so say we all. Leonard F. Andrews and Alfred B. Bidwell guilty of accessory before the fact of murder in the first degree of one Harrison T. Riley, Edmond P. Bacon, principal. Adam W. Hunter not guilty, so say we all.”",
      "The verdict, July 1885",
      "The prisoners were held in the jail at Pine Level ([2]), then the seat of Manatee County (“Verdicts”, [1]). Cato and Dryman, who testified, were not among those tried."),
    u(10, "The Atlanta Constitution, 27 July 1885, editorial page, after the Buffalo Express",
      "Now, what does Mrs. Greer say? She says that she knows, and that the respectable Christian people of southern Florida know that A. B. Bidwell is a villain of the blackest stamp. Sara Soto is no town. It is only a frontier settlement. Neighbors live half mile a part. There never was any formal organization known as the Sara Soto Assassination society. There were simply a number of bad, unscrupulous men in the neighborhood who wanted to rule things, and who stopped at no law, who were capable of any crime to carry their ends. Foremost among these were Dr. Andrews and Bidwell. Bidwell, she holds, had a bad record when he went to Florida. He kept a store at Sara Sota, where he sold pork, powder and shot, and other frontier supplies.",
      "“No formal organization”",
      "Bidwell had come from Buffalo (“formerly of Buffalo”, [2]); a Buffalo paper sought out Mrs. H. M. Greer, a neighbour at Sarasota then visiting the city. The name “Assassination society” was in the papers by July 1885; she rejects it. Her word against Dryman's “Sara Sota Vigilance Committee, styled S. S. V. C.” ([6]) is set side by side on the Compare page."),
    u(11, BA + ", p. 85",
      "In this case the defendants had a fair trial before a jury of their own selection. The verdict is not against the evidence, the witnesses were more or less corroborated by other testimony; there is no allegation that improper influences were brought to bear on their deliberations; or that they were, in any manner, controlled by passion or prejudice. … We can see no good reason to reverse his action, and must, therefore, affirm the judgment.",
      "Affirmed, 1886",
      "Florida's Supreme Court upholds the convictions of Bacon, Andrews and Bidwell. In January 1888 it upholds Anderson's conviction for the killing of Abbe: “its judgment is affirmed” (24 Fla. 139, p. 147). What became of the sentences is not in the sources read so far."),
]

COLONY = [
    u(1, GR + ", p. 96",
      "… company store had had for sale was a barrel of crackers which was emptied by the colonists' children soon after their arrival. So there was nothing left in the store to eat. But Whitaker made sure the Brownings wouldn't go hungry. He went out with his cast net and in a short time came back with a load of mullet. Then he helped clean and fry them. They were just ready to eat when Emile Whitaker came along with some bread his mother had baked for the strangers from a strange land.",
      "The settlers already there",
      "Grismer's own telling, not a quoted document. The Whitakers had settled on the bay, by Grismer's account, in the 1840s; they, the fishermen of the bay and the cattlemen of the back country were there before the colony, and are the “natives” and “crackers” of Tait's letter ([2])."),
    u(2, TR,
      "ORMISTON, Sarasota County, Fla., Jan. 4.—Dear Sir: I beg to inform you that the colonists, numbering upwards of 100 souls, arrived at their destination in due course and in excellent health, in which state they continue without exception. All were favorably impressed with the beauty of Sarasota Bay, and a fortnight's experience with the climate has created the general impression that it cannot be surpassed in point of salubrity and enjoyability. … I am sorry to say that arrangements for housing the emigrants in their new homes immediately on arrival were not possible in consequence of the sudden illness of the company's general manager, who had worked hard. … Before the colonists had been here a week it became evident that a most determined conspiracy had been formed to scare off our people by false rumors as to the land, produce, etc., by the natives or “crackers,” whose right of free grazing was certain to suffer by the formation of a settlement here. These rumors defeated their object in time, and the colonists are now settling on their lands contented and hopeful that the colony cannot fail to increase greatly in the near future. … Yours truly, J. S. TAIT.",
      "The promoter's letter, 4 January 1886",
      "J. S. Tait, who recruited the colonists in Scotland, wrote this letter to George Deas of Edinburgh, who sent it to the North British Mail against the complaints from the colony; the Tribune printed both in a cable from Glasgow. “Sarasota County” did not yet exist; the bay lay in Manatee County until 1921. Grismer calls Tait “Tate”."),
    u(3, GR + ", p. 97: memoirs of Alex Browning",
      "“One would naturally think the company would have selected close-in acreage, when it had so much land, and try to please the colonists. But in many cases the colonists drew plots which were six or eight miles out in the woods, common pine land, good only for cattle range. It took some time for everybody to learn just where their plots were. The forty acres my father drew were located near the site of the present Fruitville church and cemetery. This seems a short distance now but in those days it was a long, long way from Sarasota.”",
      "The drawing of lots",
      "Alex Browning came as a boy with his father John Browning. His memoirs survive, as far as is known, only in the passages Grismer printed; the manuscript was lent to Grismer by the family. Tait called the same drawing “carried with complete success”."),
    u(4, GR + ", p. 97: memoirs of Alex Browning",
      "“Some of the colonists started in at once to clear their land, grubbing and cutting down pine trees, digging wells and building shacks. But the work they did was painful and discouraging to men unaccustomed to the use of grub hoes, axes or shovels. They all began to realize Sarasota was not the paradise the pamphlets had pictured. A few of the hotheads decided to call on Tate with a shot gun but he evidently got wind of it and disappeared. He never returned.”",
      "“Not the paradise the pamphlets had pictured”"),
    u(5, GR + ", pp. 97–98: memoirs of Alex Browning",
      "“One of the most discouraging events, which occurred shortly after we arrived, was a change in the weather. About January 9 it became much colder and snow began to fall, greatly to the surprise of the natives who thought at first the woods were afire and that the ashes were being carried by the wind. It snowed quite a bit, enough to make snowballs. All work ceased and the men huddled around stumps being burned out of the road which was to be Main Street. Even the mules and oxen were too cold to work. Of course we all suffered, living in tents and shacks and cooking over camp fires. Many of the colonists were so discouraged by the bad weather and the remote farm plots they had gotten, that they decided to leave Sarasota. The Lawries were the first to go. Then the Breretons, and Galloways, and Watson's. Others followed.”",
      "Snow",
      "Five days after Tait's letter. Fourteen months before, the prospectus had sold the land as lying “below the frost line” (“The prospectus”, [6])."),
    u(6, GR + ", p. 97: memoirs of Nellie Lawrie",
      "She said that while church services were being held one Sunday outside a tent, a passage from Isaiah was read by Tate, the nephew of the archbishop of Canterbury. Related Miss Lawrie: “When he came to the verse which reads: ‘All we like sheep have gone astray’, there was an audible groan from the audience.”",
      "“All we like sheep”",
      "Only the words in quotation marks are Nellie Lawrie's; the rest is Grismer's paraphrase. That Tait was a nephew of the Archbishop of Canterbury is not confirmed by any source read here; Lawson ([2] in “Verdicts”) says he had been in a London bank."),
    u(7, GR + ", p. 98: diary of Dan McKinlay",
      "“Tuesday, Dec. 29: We are occupying a little log hut. It's queer experience; I can't describe it. I am going to light my pipe for I am very sad.” Dec. 31: “Weather very cold—not at all like sunny Florida.” Jan. 11: “The night was awfully cold. We could not keep out the cold.” Jan. 21: “Tramping through the thick undergrowth, my thoughts rigidly fixed on the formidable rattlesnake.” Jan. 25: “The talk is all about leaving.” Jan. 26: “The colony is breaking up very fast.” Feb. 1: “No church here … weary to get to one.” Feb. 3: “Prairie on fire all around us … everything is burning.” Feb. 4: “Prospects here are so bad … in fact, it means starvation if we stay.” Feb. 7: “Growing more and more of opinion that we can't make a living here. … The colony seems to have completely broken up.” Feb. 15: “Start today for Tampa.” Feb. 18: “Not over well pleased with Tampa—any place is better than desolate Sarasota.”",
      "A diary, December 1885 to February 1886",
      "The entries as Grismer selected them (“just a few of his entries”); the omission marks are his."),
    u(8, TR,
      "The copied revelations from New York have created a great interest hereabouts, and it is safe to say that no more deceived emigrants will go to Florida. The Glasgow Mail headed the inclosure: “Pitiful Condition of Emigrants from Glasgow, Edinboro, Paisley, Perth, and Dumbarton—A Tropical Paradise in a Swamp.”",
      "“A Tropical Paradise in a Swamp”",
      "The “revelations from New York” were a colonist's letter of complaint, John Lawrie's, printed in the New-York Tribune in January 1886; that paper is not reachable here (see “What is missing”). The left edge of this column is worn in the scan; “safe to say” and “will go” are read from the run of the lines."),
]

VERDICT = [
    u(1, "Florida State Gazetteer and Business Directory 1886–87, s.v. Sarasota",
      "SARASOTA. MANATEE COUNTY. A recently established settlement and post office, situated on Sarasota bay, about thirty miles northwest Pine Level, the county seat. It has no present business interest to report.",
      "“No present business interest to report”"),
    u(2, LW + ", p. 479",
      "The now notorious colony at Sarasota Bay, in Florida, is the youngest of a long series of Scottish failures in attempting to colonise a region utterly unsuited for them. In a small way that was an odd reproduction of the Darien fiasco. Its originator had a considerable share of Paterson's plausibility and a very large share indeed of his optimism. … Mr. Tait was not himself, I believe, a Scotchman. He had been originally in a London bank, and he came from the States to Scotland about three years ago, intending to go into the cattle ranche business. … Mr. Hanbury, an English Member of Parliament, and Colonel Dunn, an American, had acquired several tracts of land in South Florida, among them the site of this unfortunate colony at Sarasota. About two years ago Mr. Tait helped them to form a company in Edinburgh to “develop the property.” He got together a very respectable Board, which had but one fault,—not a single member of it, except, we believe, Mr. Hanbury himself, having ever been in Florida or knowing anything at all about the country.",
      "“The now notorious colony”",
      "Darien: the Scottish colony on the isthmus of Panama of 1698–1700, whose failure ruined many Scottish investors; William Paterson had promoted it. Lawson's “Colonel Dunn” is J. J. Dunne of the prospectus (“The prospectus”, [2])."),
    u(3, LW + ", pp. 479–480",
      "Altogether it was a very ill-advised idea to think of colonising a wild place like Sarasota Bay with raw Europeans. It was a great aggravation of that mistake to send out a ready-made colony. Finally, the selection of the colonists seems to have been made in the most reckless fashion. Had it been restricted to young fellows who could take no harm by roughing it for a time, and who might have thrown it up without much loss if they did not like it, comparatively little harm would have been done. Mr. Tait's blandishments were, however, exercised chiefly on elderly men and fathers of families, few of whom could have lived in the place, though it had been a certain fortune for them. The first month of the Gulf Coast mosquito would have convinced every mother and child that such a life was hardly worth living. […]",
      "Elderly men and fathers of families",
      "At […] Lawson's paragraph ends with a sentence that claims only Black people could enjoy such a life, using a racial slur, and that they expect to be well paid south of Tampa. The apparatus does not reprint the slur. The sentence shows how a London writer of 1887 measured the country: as fit for Black labour, not for Scottish families."),
    u(4, LW + ", p. 480",
      "Mr. Tait's unlucky and ill-conceived enterprise has done a great deal of harm to Florida as well as to its immediate victims; but there is no cause to despair. Florida has had booms before and will have them again.",
      "“Booms before and … again”"),
    u(5, GR + ", p. 98",
      "So went the Scotch colonists. The men, women and children who had left Scotland with such high hopes less than three months before. Now their hopes were blasted. Many were left almost penniless and had to borrow money to go to northern states where they had friends or relatives. All lost the hundred pounds they had invested, to say nothing of the money spent for the long trip from Scotland. … The colony was a complete, colossal failure. But it is difficult to fix the responsibility for the debacle. Certainly, Sir John Gillespie and the directors of the Florida Mortgage & Investment Co., Ltd., all men of honor and integrity, did not deliberately conspire to rob their fellow countrymen.",
      "The town's own verdict, 1946",
      "Grismer wrote sixty years later, as the town's historian; he acquits the directors and looks for the cause in the land deals that preceded the colony. The sum of a hundred pounds per family is his; it is not in the sources read here."),
]

SRC = ("The Economist, 25 October 1884 (Internet Archive); Florida Reports 22 Fla. 51 (1886) and 24 Fla. 139 (1888), scans of the Caselaw Access Project; "
       "The Pensacolian, 31 January 1885 (Florida Digital Newspaper Library, University of Florida); The Atlanta Constitution, 27 July 1885, "
       "and Chicago Daily Tribune, 6 February 1886 (Internet Archive); Florida State Gazetteer and Business Directory 1886–87 (Internet Archive); "
       "W. R. Lawson in Time (London), April 1887 (Internet Archive); Karl H. Grismer, The Story of Sarasota (Sarasota: M. E. Russell, 1946; copyright not renewed), "
       "pp. 43, 79, 96–98 (Internet Archive). All in the public domain.")

T = {
    "id": "prospectus", "titel": "The prospectus and the colony", "jahr": "1884–1888",
    "autor": "A company in Edinburgh, Florida's Supreme Court, newspapers from Pensacola to Chicago, colonists as quoted in 1946",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; words in square brackets are the editor's. The voices of this module are unequal: the company speaks in its prospectus and its promoter in a letter; the killers of 1884 speak in court; the murdered men, Harrison T. Riley and Charles E. Abbe, speak nowhere, and the people of the bay before the colony speak only through a historian of 1946. The colonists' memoirs and diary survive, as far as is known, only in the passages Grismer printed.",
    "sections": [
        {"id": "prospectus", "titel": "The prospectus (October 1884)",
         "blurb": "In October 1884 a new company in Edinburgh advertised its shares in The Economist. Its business was to be mortgages in Florida at rates no lender at home could get; on the side it had contracted for 47,000 acres on Sarasota Bay, land “below the frost line” where vegetables grew for the northern markets in January.",
         "plates": ["econ1884_head", "econ1884_frostline"], "units": PROSPECTUS},
        {"id": "vigilance", "titel": "The vigilance committee (1884–1888)",
         "blurb": "In the same months a group of settlers on the bay organized themselves into a committee with judges, a captain, an oath and numbered by-laws, and ordered men killed. Harrison T. Riley was shot on the road in August 1884; the postmaster, Charles E. Abbe, was shot on 27 December. A posse from Manatee arrested the members; juries at Pine Level convicted them, and Florida's Supreme Court upheld the verdicts.",
         "plates": ["bacon1886_p64", "pens1885_victory", "grismer1946_bidwell", "atl1885_greer"], "units": VIGILANCE},
        {"id": "colony", "titel": "The colony (December 1885 – February 1886)",
         "blurb": "Shortly before Christmas 1885 the colonists landed: Scottish families who had bought land through the company's promoter. The lots were drawn, many far out in the pine woods; there were no houses; in January snow fell. Within two months, as a colonist's diary records, “the colony seems to have completely broken up.”",
         "plates": ["trib1886_tait", "grismer1946_whitaker"], "viz": "prospectus-tracks", "units": COLONY},
        {"id": "verdict", "titel": "Verdicts (1886–1946)",
         "blurb": "What remained: a gazetteer's entry for a settlement with “no present business interest to report”, a London essay on “the now notorious colony”, and, sixty years later, the town historian's acquittal of the directors.",
         "plates": ["gaz1886_sarasota", "time1887_notorious"], "units": VERDICT},
    ],
}
for s in T["sections"]:
    s["zk"] = "The prospectus, " + re.sub(r" \(.*", "", s["titel"])
(D / "prospectus.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
IA = "Internet Archive; public domain."
NEW = [
    {"id": "econ1884_head", "side": "promise", "titel": "The prospectus, 1884",
     "caption": "The head of the advertisement: “THE FLORIDA MORTGAGE & INVESTMENT CO., LMTD.”, its capital, its directors in Scotland and in America, and its general manager “in Florida”, Piers E. Warburton of Sarasota.",
     "source": "The Economist, 25 October 1884, p. 1313, detail. " + IA},
    {"id": "econ1884_frostline", "side": "promise", "titel": "“Below the frost line”",
     "caption": "47,000 acres on Sarasota Bay at $3.40 an acre, for oranges, bananas, pineapples, sugar, cotton, tobacco, rice and maize, “as the lands are below the frost line”.",
     "source": "The Economist, 25 October 1884, p. 1313, detail. " + IA},
    {"id": "bacon1886_p64", "side": "law", "titel": "“Styled S. S. V. C.”",
     "caption": "Florida's Supreme Court reports the testimony of Thomas L. Dryman: the meeting before the killing of Harrison T. Riley, “a meeting of an organization known as the Sara Sota Vigilance Committee, styled S. S. V. C.”, and its members.",
     "source": "Bacon, Andrews and Bidwell v. State, 22 Fla. 51 (1886), p. 64. Caselaw Access Project; public domain."},
    {"id": "pens1885_victory", "side": "law", "titel": "“A Law and Order Victory”, 1885",
     "caption": "The Florida Times-Union's account, reprinted in Pensacola: “a society of thugs at Sarasota”, the oath at gunpoint, the judges and the captain, the arrests, and the crowd held back from lynching the prisoners.",
     "source": "The Pensacolian, 31 January 1885, p. 4, two column sections set side by side. Florida Digital Newspaper Library, University of Florida; public domain."},
    {"id": "grismer1946_bidwell", "side": "law", "titel": "Bidwell's house",
     "caption": "“Did the Vigilantes plan a murder here?” The house of Alfred B. Bidwell as photographed for Grismer's book; his caption says the murder of the postmaster was accused of having been planned there on Christmas Day 1884 (he misprints the postmaster's initial as “R.”).",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 79. " + IA},
    {"id": "atl1885_greer", "side": "law", "titel": "“Sara Soto is no town”, 1885",
     "caption": "A neighbour from Sarasota, visiting Buffalo, against the name in the papers: “There never was any formal organization known as the Sara Soto Assassination society.”",
     "source": "The Atlanta Constitution, 27 July 1885, editorial page, after the Buffalo Express, detail. " + IA},
    {"id": "trib1886_tait", "side": "colony", "titel": "Tait's letter, 1886",
     "caption": "“ORMISTON, Sarasota County, Fla., Jan. 4.” The promoter's letter to Edinburgh, cabled from Glasgow, with the Glasgow paper's heading below: “A Tropical Paradise in a Swamp.”",
     "source": "Chicago Daily Tribune, 6 February 1886, p. 5, detail. " + IA},
    {"id": "grismer1946_whitaker", "side": "colony", "titel": "The Whitaker children",
     "caption": "“Sarasota's first children”: six of the eleven children of William H. and Mary Jane Whitaker, whose family, by Grismer's account, had been on the bay since the 1840s and fed the newcomers in 1885.",
     "source": "Karl H. Grismer, The Story of Sarasota (1946), p. 43. " + IA},
    {"id": "gaz1886_sarasota", "side": "town", "titel": "“No present business interest”",
     "caption": "Sarasota in the Florida gazetteer of 1886–87: “A recently established settlement and post office … It has no present business interest to report.”",
     "source": "Florida State Gazetteer and Business Directory 1886–87, s.v. Sarasota, detail. " + IA},
    {"id": "time1887_notorious", "side": "colony", "titel": "“The now notorious colony”, 1887",
     "caption": "A London monthly on the colony: “the youngest of a long series of Scottish failures in attempting to colonise a region utterly unsuited for them”, and on the board that had never been to Florida.",
     "source": "W. R. Lawson, “Scottish Colonies on the Gulf of Mexico”, Time (London), April 1887, p. 479. " + IA},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["lede"] = "Public-domain pages, maps and photographs, each with its source."
P["credit"] = ("Pages of The Economist, The Atlanta Constitution, the Chicago Daily Tribune, Time (London), a Florida gazetteer and Karl H. Grismer's Story of Sarasota (1946): Internet Archive. "
               "Florida Reports: Caselaw Access Project, Harvard Law School Library. The Pensacolian: Florida Digital Newspaper Library, University of Florida. All in the public domain.")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "prospectus"), None) or next(x for x in M["shipped"] if x["id"] == "prospectus")
M["planned"] = [x for x in M["planned"] if x["id"] != "prospectus"]
m.update({"datei": "prospectus", "zk": "Prospectus · Vigilance committee · Colony · Verdicts",
          "kurz": "1 · The prospectus and the colony",
          "warum": "In October 1884 a company in Edinburgh contracted for 47,000 acres on Sarasota Bay, “below the frost line”. In the same year a vigilance committee of settlers killed Harrison T. Riley and the postmaster Charles E. Abbe; Florida's courts convicted its leaders. In December 1885 Scottish colonists landed; in January snow fell, and by February the colony had broken up.",
          "quelle": "The Economist 1884; Florida Reports 1886 and 1888; The Pensacolian and The Atlanta Constitution 1885; Chicago Daily Tribune 1886; Florida gazetteer 1886–87; Time (London) 1887; Grismer (1946)."})
order = ["prospectus", "village", "rails", "boom", "bust", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "prospectus"] + [m], key=lambda x: order.index(x["id"]))
ADD = [
    {"id": "lawrie", "side": "colony", "kurz": "John Lawrie's letter, January 1886",
     "warum": "The colonist John Lawrie of Paisley wrote the letter of complaint that the New-York Tribune printed in January 1886 and the Scottish papers copied. The New York paper is on Chronicling America, which is not reachable here; a summary in the Los Angeles Times of 17 January 1886 is too worn in the scan to be read reliably.",
     "quelle": "New-York Tribune, January 1886."},
    {"id": "riley", "side": "law", "kurz": "Harrison T. Riley and Charles E. Abbe",
     "warum": "Both murdered men appear in the sources only through their killers, the courts and the press. What Riley was accused of comes from the committee itself; why Abbe was hated is disputed in the press of 1885. A genealogy of the Abbe family (1916) and the post office records have not yet been read against the page image.",
     "quelle": "Abbe-Abbey Genealogy (1916); records of the Post Office Department."},
    {"id": "sentences", "side": "law", "kurz": "The sentences",
     "warum": "The Supreme Court's opinions affirm the judgments but do not state the sentences, and what became of the convicted men — pardons, commutations, escapes — is not documented in the sources read so far. The records of the Florida Board of Pardons and the state prison would be needed.",
     "quelle": "State Archives of Florida."},
    {"id": "before1884", "side": "colony", "kurz": "The bay before 1884",
     "warum": "The Calusa, the Cuban and Spanish fishing ranchos on the bay, the Seminole wars and the Whitakers' settlement of the 1840s are told here only in passing. The federal documents on the fishing ranchos of the 1830s and the naval records of the Civil War on the bay have been found but not yet read against the page image.",
     "quelle": "Congressional documents of the 1830s; Official Records of the Union and Confederate Navies, vol. 17 (1903)."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "society", "titel": "Was there a society?",
     "frage": "Was there an organized committee of killers at Sarasota in 1884?",
     "note": "A member testified to “the Sara Sota Vigilance Committee, styled S. S. V. C.”, its meetings and its members; a Jacksonville paper called it “a society of thugs”. A neighbour, speaking in Buffalo, denied that there was ever “any formal organization” and blamed “a number of bad, unscrupulous men”. The juries and the Supreme Court followed the testimony.",
     "voices": [{"text": "prospectus", "sec": "vigilance", "n": [6, 5], "wer": "Thomas L. Dryman and Louis L. Cato, in court, 1885"},
                {"text": "prospectus", "sec": "vigilance", "n": [2], "wer": "Florida Times-Union, January 1885"},
                {"text": "prospectus", "sec": "vigilance", "n": [10], "wer": "Mrs. H. M. Greer, July 1885"}]},
    {"id": "arrival", "titel": "Excellent health",
     "frage": "How did the colony fare in its first weeks?",
     "note": "The promoter wrote on 4 January 1886 that the colonists continued in excellent health and were settling on their lands “contented and hopeful”. Five days later, by a colonist's memoir, snow fell; a diary of the same weeks ends with “Start today for Tampa.”",
     "voices": [{"text": "prospectus", "sec": "colony", "n": [2], "wer": "J. S. Tait, 4 January 1886"},
                {"text": "prospectus", "sec": "colony", "n": [5, 7], "wer": "Alex Browning; Dan McKinlay"}]},
    {"id": "blame", "titel": "Whose fault?",
     "frage": "Who was responsible for the failure of the colony?",
     "note": "A London writer in 1887 blamed the promoter's plausibility, a board that had never seen Florida, and the choice of “elderly men and fathers of families”. The town's historian in 1946 called the directors “men of honor and integrity” and looked for the cause elsewhere.",
     "voices": [{"text": "prospectus", "sec": "verdict", "n": [2, 3], "wer": "W. R. Lawson, 1887"},
                {"text": "prospectus", "sec": "verdict", "n": [5], "wer": "Karl H. Grismer, 1946"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/prospectus/"
LINK = {
    "47,000 acres below the frost line": (K + "prospectus/6", "The prospectus, 1884 [6]", "econ1884_frostline"),
    "The Sara Sota Vigilance Committee": (K + "vigilance/6", "The vigilance committee [6]", "bacon1886_p64"),  # date set to August 1884 below
    "The postmaster is shot": (K + "vigilance/7", "The vigilance committee [7]", None),
    "Snow": (K + "colony/5", "The colony [5]", None),
}
for s in TL["stations"]:
    if s["titel"] == "The Sara Sota Vigilance Committee":
        s["d"] = "August 1884"
    if s["titel"] == "Snow":
        s["d"] = "about 9 January 1886"
    if s["titel"] in LINK:
        s["cite"], s["citeLabel"], pl = LINK[s["titel"]]
        if pl:
            s["plate"] = pl
NEWST = [
    {"d": "August 1884", "side": "law", "titel": "Riley on the road",
     "text": "Harrison T. Riley is shot on the road and his throat cut, on the orders, as members later testify, of the committee's “judges”.",
     "cite": K + "vigilance/4", "citeLabel": "The vigilance committee [4]",
     "quelle": "The Pensacolian, 31 January 1885, p. 4; Bacon v. State, 22 Fla. 51 (1886), p. 62."},
    {"d": "31 January 1885", "side": "law", "titel": "“A society of thugs”",
     "text": "The press reports the arrests: “a society of thugs at Sarasota”, with judges, a captain and an oath; the prisoners are held at Pine Level, and the people were “with great difficulty” prevented from lynching them.",
     "cite": K + "vigilance/2", "citeLabel": "The vigilance committee [2]", "plate": "pens1885_victory",
     "quelle": "The Pensacolian, 31 January 1885, p. 4, after the Florida Times-Union."},
    {"d": "14 July 1885", "side": "law", "titel": "The verdict",
     "text": "At a special term of the Circuit Court for Manatee County the jury finds Edmond P. Bacon guilty of the murder of Harrison T. Riley, and Leonard F. Andrews and Alfred B. Bidwell guilty as accessories; Adam W. Hunter is acquitted.",
     "cite": K + "vigilance/9", "citeLabel": "The vigilance committee [9]",
     "quelle": "Bacon, Andrews and Bidwell v. State, 22 Fla. 51 (1886), pp. 52–53."},
    {"d": "27 July 1885", "side": "law", "titel": "“No formal organization”",
     "text": "A neighbour from Sarasota, in Buffalo: “Sara Soto is no town. It is only a frontier settlement. … There never was any formal organization known as the Sara Soto Assassination society.”",
     "cite": K + "vigilance/10", "citeLabel": "The vigilance committee [10]", "plate": "atl1885_greer",
     "quelle": "The Atlanta Constitution, 27 July 1885, editorial page, after the Buffalo Express."},
    {"d": "4 January 1886", "side": "colony", "titel": "“In excellent health”",
     "text": "The promoter J. S. Tait writes from “Ormiston”: the colonists, “upwards of 100 souls”, arrived “in excellent health”; the natives are spreading “false rumors”.",
     "cite": K + "colony/2", "citeLabel": "The colony [2]", "plate": "trib1886_tait",
     "quelle": "Chicago Daily Tribune, 6 February 1886, p. 5."},
    {"d": "15 February 1886", "side": "colony", "titel": "“Start today for Tampa”",
     "text": "A colonist's diary: “The colony seems to have completely broken up.” Three days later: “any place is better than desolate Sarasota.”",
     "cite": K + "colony/7", "citeLabel": "The colony [7]",
     "quelle": "Diary of Dan McKinlay, in Grismer, The Story of Sarasota (1946), p. 98."},
    {"d": "1886–87", "side": "town", "titel": "No business to report",
     "text": "The state gazetteer lists Sarasota as “a recently established settlement and post office” that “has no present business interest to report”.",
     "cite": K + "verdict/1", "citeLabel": "Verdicts [1]", "plate": "gaz1886_sarasota",
     "quelle": "Florida State Gazetteer and Business Directory 1886–87, s.v. Sarasota."},
    {"d": "April 1887", "side": "colony", "titel": "“The now notorious colony”",
     "text": "A London monthly counts Sarasota among the “Scottish failures in attempting to colonise a region utterly unsuited for them” — and adds: “Florida has had booms before and will have them again.”",
     "cite": K + "verdict/2", "citeLabel": "Verdicts [2]", "plate": "time1887_notorious",
     "quelle": "W. R. Lawson, Time (London), April 1887, pp. 479–480."},
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
TL["lede"] = "Stations read against the page images of their sources only; each names its source and, where printed, links to its passage."
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
