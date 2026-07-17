This file is a 38-case sample (19 NSWCA, 1988-2024; 19 HCA, 1972-2024) drawn from a local Neo4j case-law database on 2026-07-16/17. It is meant to be illustrative of judicial register — how these particular judges, in these particular judgments, actually wrote — not a statistically representative claim about NSWCA or HCA judgment-writing as a whole. The sample list, the Cypher-query schema notes, and the full methodology are set out below for auditability; anyone using this file to justify a claim in human-legal-voice/SKILL.md should be able to trace it back to a specific case and paragraph in the tables and quotes that follow.

# How NSWCA and HCA judges actually write: empirical patterns from real judgment text

Source: local Neo4j database of AustLII-derived Australian case law. All quotes below are verbatim text pulled directly from `Paragraph`/`HCAParagraph` nodes via Cypher queries — none are paraphrased or reconstructed from memory. Minor OCR/extraction artefacts in the source text (stray line-break numerals, spacing glitches like "URJ", "50", "45" mid-sentence from page-number/margin-note bleed) have been left as-is in quotes rather than silently cleaned, since they are genuinely present in the underlying corpus text.

## Sample

**NSWCA (19 cases, 1988–2024), `court = 'Court of Appeal of New South Wales'`:**

| Citation | Case name | Year | Paragraphs read |
|---|---|---|---|
| [1988] NSWCA 67 | Hooker Corporation Ltd v Darling Harbour Authority | 1988 | 88 |
| [1988] NSWCA 52 | Goldberg v Law Society of NSW | 1988 | 84 |
| [1991] NSWCA 68 | Custom Credit Corporation Ltd v Cenepro Pty Ltd | 1991 | 160 |
| [1993] NSWCA 10 | Australian Consolidated Press Ltd v Ettingshausen | 1993 | 109 |
| [1994] NSWCA 199 | McBride v Walton | 1994 | 148 |
| [1995] NSWCA 166 | Geebung Investments Pty Ltd v Varga Group Investments No 8 Pty Ltd | 1995 | 120 |
| [1999] NSWCA 6 | Vanmeld Pty Ltd v Fairfield City Council | 1999 | 193 |
| [2001] NSWCA 61 | Brambles Holdings Ltd v Bathurst City Council | 2001 | 180 |
| [2005] NSWCA 32 | Redowood Pty Ltd v Mongoose Pty Ltd | 2005 | 178 |
| [2006] NSWCA 388 | Gales Holdings Pty Ltd v Minister for Infrastructure and Planning | 2006 | 200 |
| [2008] NSWCA 326 | Wattyl Australia Pty Ltd v McArthur | 2008 | 200 |
| [2009] NSWCA 406 | Pacific Steel Constructions Pty Ltd v Barahona | 2009 | 180 |
| [2012] NSWCA 399 | Tomasetti v Brailey | 2012 | 199 |
| [2014] NSWCA 288 | Dank v Cronulla Sutherland District Rugby League Football Club Ltd | 2014 | 199 |
| [2016] NSWCA 152 | Keith v Gal | 2016 | 179 |
| [2019] NSWCA 52 | Trajkovski v Simpson | 2019 | 200 |
| [2021] NSWCA 126 | Hoblos v Alexakis | 2021 | 196 |
| [2024] NSWCA 249 | Kmart Australia Ltd v Marmara | 2024 | 200 |
| [2024] NSWCA 14 | Schrader v Broach | 2024 | 196 |

**HCA (19 cases, 1972–2024), `HCACase`/`HCAParagraph` via `FROM_CASE`:**

| Citation | Case name | Year | Paragraphs read |
|---|---|---|---|
| [1972] HCA 51 | Fisher v Ship "Oceanic Grandeur" | 1972 | 89 |
| [1974] HCA 23 | R v Bull | 1974 | 88 |
| [1975] HCA 63 | Steinberg v Federal Commissioner of Taxation | 1975 | 125 |
| [1976] HCA 44 | Johnson v R | 1976 | 72 |
| [1985] HCA 11 | Gerhardy v Brown | 1985 | 51 |
| [1988] HCA 40 | Breavington v Godleman | 1988 | 65 |
| [1989] HCA 38 | Philip Morris Ltd v Commissioner of Business Franchises (Vic) | 1989 | 70 |
| [1996] HCA 56 | Victoria v Commonwealth ("Industrial Relations Act case") | 1996 | 225 |
| [1997] HCA 31 | Levy v Victoria ("Duck shooting case") | 1997 | 221 |
| [1997] HCA 50 | Green v R | 1997 | 219 |
| [2005] HCA 20 | Commissioner of Taxation v Linter Textiles Australia Ltd | 2005 | 248 |
| [2007] HCA 46 | Em v The Queen | 2007 | 239 |
| [2008] HCA 56 | Kennon v Spry | 2008 | 238 |
| [2012] HCA 21 | PGA v The Queen | 2012 | 248 |
| [2013] HCA 34 | Fortescue Metals Group Ltd v The Commonwealth | 2013 | 234 |
| [2015] HCA 6 | Korda v Australian Executor Trustees (SA) Ltd | 2015 | 242 |
| [2019] HCA 1 | Unions NSW v New South Wales | 2019 | 223 |
| [2021] HCA 4 | Minister for Home Affairs v Benbrika | 2021 | 240 |
| [2024] HCA 7 | Redland City Council v Kozik | 2024 | 246 |

Schema note for reproducibility: NSWCA paragraph text lives on generic `Paragraph` nodes joined via `document_citation_key`; HCA paragraph text lives on `HCAParagraph` nodes joined to `HCACase` via `(:HCAParagraph)-[:FROM_CASE]->(:HCACase)`, matched to `DecisionDocument` by `HCACase.citation = DecisionDocument.citation_key` (HCA paragraphs have **no** `document_citation_key` property — this is the join HCAParagraph actually uses).

---

## 1. Opening moves

NSWCA judgments in this sample almost never open with a generic scene-setter. The very first substantive sentence typically does one of two things: (a) the *first* judge to write states the appeal's posture directly, or (b) if not the first judge in the file, immediately states agreement with another judge before anything else. Genuinely explicit "This is an appeal from..." framing exists but is not the majority pattern — more common is jumping straight into the facts or the specific issue mid-stream, because the case name/citation/procedural history is carried by separate coversheet fields rather than restated in prose.

- `[1994] NSWCA 199 at [16]`: "Powell JA This is an appeal from the determinations and orders made by the Medical Tribunal of New South Wales ("the Tribunal") following an inquiry by it into the subject matter of a complaint, originally lodged by the Respondent..."
- `[1995] NSWCA 166 at [3]`: "Kirby P This is an appeal from orders of Abadee J."
- `[1993] NSWCA 10 at [1]`: "Gleeson CJ This is an appeal following a large award of damages against the appellant in a defamation action. The respondent is a prominent rugby league footballer."
- `[2021] NSWCA 126 at [1]`: "WHITE JA: This appeal raises two separate but, in the circumstances of this case, related issues. The first is the application of the principle that the burden lies on the plaintiff to prove the injury or loss for which he seeks damages (*Todorovic v Waller* (1981) 150 CLR 402; [1981] HCA 72 per Gibbs CJ and Wilson J at 412)..."

A very distinctive NSWCA structural feature — one a generic AI writer would not naturally reproduce — is that in **multi-judge panels, the second and third judgments frequently open with nothing more than a one-line agreement**, before (if anything) adding supplementary reasons:

- `[2019] NSWCA 52 at [1]`: "BASTEN JA AND SACKVILLE AJA: We are grateful to Brereton JA for recounting the facts and for identifying the issues debated on the appeal. We agree with the orders proposed by his Honour but prefer to state our own reasons for concluding that the appeal should be allowed."
- `[2024] NSWCA 249 at [1]`: "KIRK JA: I agree with McHugh JA."
- `[2024] NSWCA 14 at [1]`: "GLEESON JA: I agree with Stern JA."
- `[2016] NSWCA 152 at [1]`: "MEAGHER JA: I agree with Gleeson JA."
- `[2006] NSWCA 388 at [1]`: "BEAZLEY JA: I have had the opportunity to read in draft the reasons of Tobias JA. I agree with his Honour's reasons and proposed orders."

HCA joint judgments open completely differently: with a **bench-identification byline in the collective voice**, then straight into the substantive facts/legislative scheme — no "this is an appeal" framing at all in this sample; the appeal's posture is stated as a fact about the parties and the court below, not announced as a genre move:

- `[2005] HCA 20 at [1]`: "GLEESON CJ, GUMMOW, HAYNE, CALLINAN AND HEYDON JJ. The appellant ("the Commissioner") appeals from the judgment of the Full Court of the Federal Court (Hill, Goldberg and Conti JJ). The Full Court dismissed the Commissioner's appeal against the judgment of Hely J. His Honour upheld an "appeal" by the respondent taxpayer..."
- `[2019] HCA 1 at [1]`: "KIEFEL CJ, BELL AND KEANE JJ. In *Unions NSW v New South Wales* ("*Unions NSW [No 1]*") and in *McCloy v New South Wales*, consideration was given by this Court to the general structure, key provisions and purposes of the *Election Funding, Expenditure and Disclosures Act 1981* (NSW)..."
- `[2021] HCA 4 at [1]`: "KIEFEL CJ, BELL, KEANE AND STEWARD JJ. Division 105A of the *Criminal Code* (Cth) ("the Code") empowers the Supreme Court of a State or Territory, on the application of the Minister for Home Affairs..., to order that a person who has been convicted of a terrorist offence be detained in prison for a further period after the expiration of his or her sentence of imprisonment."
- `[2024] HCA 7 at [1]`: "GAGELER CJ AND JAGOT J. In the Preface to the second edition of Mason and Carter's *Restitution Law in Australia*, the authors referred metaphorically to the "restitution common of the law" being "tended by judges". They encouraged preparedness on the part of judges to "tear out weeds, however ancient"."

That last example ([2024] HCA 7) is worth flagging on its own: modern HCA joint judgments will occasionally open with a genuinely literary framing device (a quoted metaphor from a text) before descending into the facts — something a generic AI legal-writing mode would either overdo everywhere or never attempt.

---

## 2. Engagement with the primary judge / trial judge

Both courts use "the primary judge" (appellate review of a single judge below) far more than "the trial judge" in civil appeals, though "trial judge" still dominates numerically because it also covers jury-trial criminal appeals where the term is idiomatic regardless of forum.

- `[2005] NSWCA 32 at [46]`: "The primary judge found (at [115]) that the second rights acceptance form, although signed, did not conform with the "How to accept the offer" instructions endorsed on its reverse side."
- `[2005] NSWCA 32 at [74]`: "Thus, in my opinion, the primary judge erred in concluding that there was insufficient correspondence between offer and acceptance."
- `[2006] NSWCA 388 at [175]`: "In my opinion, therefore, the primary judge erred not only in the manner in which he approached this issue but also in his conclusion that the Council was not bound to take into consideration that Core Economics retail study."
- `[2009] NSWCA 406 at [179]`: "No error has been shown in her Honour's dismissal of this claim."
- `[1993] NSWCA 10 at [40]`: "I see no error requiring intervention on this point."
- `[1995] NSWCA 166 at [3]`: "Whilst it might have made this court's task a little easier if his Honour had made a finding as to whether he preferred the evidence of Mr Varga or Mr Lamont, I see no error in his ultimate conclusion."
- `[2001] NSWCA 61 at [177]`: "Having found that the offer was accepted and that there was consideration, it follows that I consider that Hodgson CJ in Eq correctly found that the parties entered into the October 1991 contract and that contract was binding and enforceable."

HCA does the identical move but the "primary judge" is more often a judge of a State Supreme Court or Family Court whose findings are being tested against a doctrinal standard, not merely re-weighed:

- `[2008] HCA 56 at [106]`: "With respect to the terms of s 106B(1), the primary judge found that, as to the 1998 Instrument, at the relevant time the husband "was looking to defeat an anticipated order for property settlement"."
- `[2007] HCA 46 at [123]`: "The conclusion reached in the courts below, that no error was shown in the trial judge refusing to exclude under s 90 the evidence of part of what the appellant said to police, was correct."
- `[2015] HCA 6 at [44]`: "The primary judge found it unnecessary to determine whether they could be taken into account, although he thought it "unlikely that an admission [could] create an express trust with retrospective operation ... where none was intended or found to exist"."

The gendered pronoun usage tracks the bench over time: "his Honour found" dominates the earlier NSWCA sample; "her Honour found" appears only from the 2009 case onward in this sample (`[2009] NSWCA 406`), consistent with the increasing proportion of women on the NSW trial bench being reflected in appellate prose over the sampled decades — a real, dateable shift rather than stylistic variation.

---

## 3. How submissions and argument are reported

This is one of the most mechanically consistent conventions across both courts and all eras: submissions are reported in indirect/reported speech using a small, closed set of verbs (submitted, contended, argued, conceded, accepted), almost never as direct quotation of counsel's actual words except when quoting an opening/closing address verbatim for a specific evidentiary point.

- `[1988] NSWCA 67 at [72]`: "It was then submitted that the combination of this fact and the terms of the Deed of Offer allow only of the conclusion that the Government was free to withdraw from the arrangement..."
- `[1988] NSWCA 67 at [75]`: "Indeed counsel for the Government at one stage submitted that that was the effect of the Deed of Offer although its terms provide scant support for that submission."
- `[1991] NSWCA 68 at [115]`: "Although counsel for the appellant accepted that the hallmarks of a concluded agreement were to be found in the critical discussion which took place between the parties on 21 September 1988 he submitted that outstanding matters on which there had been no agreement negated the existence of a binding contract."
- `[1993] NSWCA 10 at [63]`: "Senior counsel for Mr Ettingshausen conceded that the verdict was very high — at one stage he said "massive"."
- `[2012] NSWCA 399 at [62]`: "However he submitted that the primary judge erred in concluding, in light of a finding to similar effect in relation to Mr Brailey's evidence, that his Fair Trading Act claim was "to be determined on the basis of the documents and what has been admitted by Mr Brailey"..."

HCA reports submissions the same way but frequently attributes them to the represented State/party rather than to named counsel, especially in constitutional matters (e.g. "South Australia submitted that…" rather than "counsel for South Australia submitted"):

- `[1974] HCA 23 at [50]`: "It was submitted that the expression "prohibited imports" described a class of goods identified by their proscription by regulation."
- `[1972] HCA 51 at [30]`: "In the present case, the plaintiffs contended that but for services such as those rendered by them, *Oceanic Grandeur* would have been immobilized and useless to its owners..."
- `[2012] HCA 21 at [76]`: "South Australia submitted that Hale's proposition "was never authoritatively declared as part of the common law in Australia." It also submitted that no case had Hale's proposition as its ratio decidendi."
- `[2019] HCA 1 at [221]`: "As senior counsel for the plaintiffs submitted, it was clear "what this law is doing" but one simply does not "know why it is doing that other than to shut down that protected speech"."

Direct quotation of a named counsel's actual courtroom words does occur, but is reserved for moments where the exact phrasing matters to the ground of appeal (e.g. what was actually said to a jury):

- `[1993] NSWCA 10 at [43]`: "Clearly enough (and understandably) counsel for the appellant opened this point to the jury in his address: "You see you come here as members of the community, ordinary decent members of the community, and you bring to the case, you should bring to the case, no extreme views...""

---

## 4. Hedging, certainty, and disagreement

"With respect" is extremely common in both courts (96 hits/19 cases NSWCA, 177 hits/19 cases HCA in this sample) but is used far more often as an ordinary preposition ("with respect to the arguments...", "jurisdiction with respect to offences...") than as the polite-disagreement idiom ("with respect, I do not accept..."). A generic AI writer reaching for "with respect" as a disagreement marker would badly overstate its actual rate as a disagreement marker specifically — most tokens are load-bearing prepositions, not politeness softeners.

- `[1988] NSWCA 67 at [86]`: "These findings were said to be incorrect but with respect to the arguments to the contrary a conclusion that his Honour erred in these two respects would not necessarily lead to the upholding of the restitution claim." (ordinary prepositional use, not disagreement)

Genuine hedged/disagreement phrasing clusters around a small repertoire: "in my view", "it seems to me", "I am not persuaded", "I do not accept", "I am unable to accept", "I would reject" — and, more rarely, explicit "I would respectfully [adopt/decline to follow]":

- `[1988] NSWCA 67 at [15]`: "I think, however, I should state in my own words why it seems to me that the better construction of the Deed of Offer is that arrived at by Mahoney JA."
- `[1988] NSWCA 52 at [82]`: "But perhaps more significantly I am not persuaded that the unreliability which has been amply demonstrated in some areas of his practice is not liable to be repeated in every part of his practice..."
- `[2012] NSWCA 399 at [130]`: "I do not accept these submissions."
- `[1991] NSWCA 68 at [132]`: "I am unable to accept this submission."
- `[1988] NSWCA 67 at [84]`: "Before concluding I would observe that like Rogers J I would reject an approach that propounded the existence of two contracts as a consequence of the notification of the acceptance."
- `[1976] HCA 44 at [57]`: "Thomas [1837] EngR 242; (1833) 7 Car & P 817 (173 ER 356) puts the matter in a sense which I would respectfully adopt."
- `[2005] HCA 20 at [233]`: "To the extent that the reasons of Menzies J, addressing a different expression, suggest any different conclusion in this case, I would respectfully decline to follow it."

Note: across the full sample, "I would respectfully dissent" and "I would reach a different conclusion" as fixed idioms returned **zero** hits — real disagreement is expressed through the more specific verbs above ("I do not accept", "I am unable to accept", "I would reject") or, for genuine dissents, through the terse structural marker discussed in section 8 below (e.g. "Clarke JA dissenting" in the catchwords, or "this judgment dissents from the orders proposed by the other members of the Court" — [2008] HCA 56 at [182]), not through a set dissent-announcing phrase. A skill that scripts "I would respectfully dissent" as boilerplate would be producing something these judgments don't actually say.

---

## 5. Sentence rhythm and structure (measured, not estimated)

Using a naive sentence splitter over the full retrieved text of all 38 cases, word-count per sentence by court and era bucket:

| Court | Era | Sentences | Mean words | Median | 90th pctile | Max |
|---|---|---|---|---|---|---|
| NSWCA | pre-2000 | 5,412 | 30.1 | 25 | 56 | 199 |
| NSWCA | 2000–2014 | 4,062 | 32.2 | 27 | 59 | 196 |
| NSWCA | 2015+ | 2,576 | 28.9 | 25 | 51 | 175 |
| HCA | pre-2000 | 4,277 | 25.1 | 21 | 51 | 195 |
| HCA | 2000–2014 | 4,820 | 27.2 | 24 | 49 | 200 |
| HCA | 2015+ | 2,866 | 34.0 | 30 | 61 | 189 |

Two things stand out against a generic-AI baseline (which tends to default to short, uniform 15–20 word sentences): median sentence length is **materially longer** in this corpus (21–30 words), and the tail is long — 10% of sentences run past 50 words, some past 150–200 (a single sentence can carry an entire subordinate clause chain: a proposition, its qualification, an authority for the qualification, and a return to the proposition). Long sentences are typically built from stacked subordinate clauses hung off a small number of connective phrases ("in circumstances where...", "notwithstanding that...", "it being common ground that...", "on the footing that..."), not run-on coordination with "and"/"but". Interestingly HCA's most recent bucket (2015+) has the *longest* sentences of the whole sample (mean 34.0) — the opposite of a simple "modern = plainer" story; this may reflect the constitutional/statutory-construction subject matter of the 2015+ HCA sample ([2019] HCA 1, [2021] HCA 4, [2024] HCA 7) more than a general era effect, and should not be over-generalised from three cases.

Example of the long stacked-clause pattern:

- `[1988] NSWCA 67 at [87]`: "Those circumstances, at least those which arose after 24 June, will be subjected to careful analysis during the breach/repudiation argument and it seems to me therefore quite inappropriate to proceed at this stage to consider the restitution claim while the possibility remains that factual findings will be ultimately made which might falsify the bases of any conclusion."
- `[2019] HCA 1 at [221]`: "The only rational explanation for the reduction in the cap for third-party campaigners and the introduction of the "acting in concert" offence is that in implementing the recommendations and reasoning of the Expert Panel Report, the Parliament of New South Wales acted with the additional purpose, not merely the effect, of quietening the voices of third-party campaigners relative to political parties."

Numbered sub-clauses within a single paragraph are a real, recurring device for enumerating grounds, findings, or orders (not just for final orders):

- `[2016] NSWCA 152 at [54]`: "In oral argument, the issues raised by the grounds of appeal were grouped by the appellant's counsel as follows: 1. whether his Honour erred in entering a verdict in favour of the respondents becaus[e]..."
- `[1991] NSWCA 68 at [1]` (catchwords-style summary paragraph): "(1) The developer was entitled to the consequential loss of profits which flowed from the failure of the financier to adhere to its promise to provide full funding... (2) It was open to the trial judge to conclude..."

---

## 6. Latin phrases and terms of art — actual frequency, not assumed frequency

Across the full sample, Latin/term-of-art incidence is genuinely modest — a handful of instances per judgment at most, clustered where they are doctrinally load-bearing, not sprinkled as decoration. Measured rate per 10,000 words of judgment text:

| Court | Era | Latin-phrase hits | Words | Rate /10k words |
|---|---|---|---|---|
| NSWCA | pre-2000 | 67 | 167,102 | 4.01 |
| NSWCA | 2000–2014 | 12 | 132,444 | 0.91 |
| NSWCA | 2015+ | 2 | 74,554 | 0.27 |
| HCA | pre-2000 | 23 | 107,638 | 2.14 |
| HCA | 2000–2014 | 15 | 131,583 | 1.14 |
| HCA | 2015+ | 50 | 98,284 | 5.09 |

(Phrases counted: *prima facie, obiter, ratio decidendi, inter alia, bona fide, ex parte, mutatis mutandis, de novo, amicus curiae*. `sub judice`, `res judicata`, `sui generis` and `curia advisari vult` returned **zero** hits in this entire 38-case sample — worth noting explicitly, since a generic AI legal-writing mode tends to assume these appear constantly.)

NSWCA shows a clean, monotonic decline across the three eras — consistent with the "older judgments more Latinate, modern judgments plainer" hypothesis. HCA does **not** show the same clean decline in this sample; the 2015+ HCA bucket is actually the highest, but that bucket contains only three cases and the spike looks topic-driven (constitutional/doctrinal cases using "ratio decidendi"/"inter alia" repeatedly in argument) rather than a genuine era effect — this should be treated as a caveat, not a finding, given the small n.

Representative uses, showing Latin is deployed for precise doctrinal work, not flourish:

- `[1989] HCA 38 at [22]`: "Section 10, therefore, prima facie imposes an excise on the tobacco products manufactured by P.M.L. and sold by it by wholesale."
- `[1996] HCA 56 at [131]`: "Article 5 provides that a number of grounds "inter alia, shall not constitute valid reasons for termination". The use of the words "inter alia" recognises that the list in Art 5 is not an exhaustive one." (note: the Court here is glossing the meaning of "inter alia" *within a statute it is construing*, not using it as its own connective)
- `[2012] HCA 21 at [159]`: "For the Court in this appeal the question is whether, as a matter of ratio decidendi, not obiter dicta, South Australia's second submission should be recognised as correct."
- `[1996] HCA 56 at [30]`: "It is to seek to distort the principles of stare decisis and of ratio decidendi to contend that a decision lacks authority because it might have been reached upon a different path of legal reasoning to that which was actually followed."
- `[1985] HCA 11 at [48]`: "A curial declaration of the law, once made, relieves the Court from the necessity of undertaking the same enquiry de novo and binds courts below it in the hierarchy."

"Ex parte" appears almost exclusively as part of a case name (e.g. "*Ex parte Law Society of New South Wales*"), not as a standalone Latin connective — another point where a generic AI writer might misuse a term-of-art that in practice only survives embedded in fixed citation strings:

- `[1988] NSWCA 52 at [38]`: "This misconduct can properly be regarded as wilful: *Re Miles; Ex parte Law Society of New South Wales* (1966) 84 WN (Pt 1) (NSW) 163."

---

## 7. Structural conventions

The corpus's own ML-derived `section` classification on `Paragraph` nodes (`background`, `issues`, `submissions`, `evidence`, `consideration`, `conclusion`, `orders`, `representation`, `other`, `body`) is a post-hoc classifier tag, **not** literal heading text the judges wrote — checking `text_html` for the same paragraphs confirms no literal `<h2>Background</h2>`-style markup survives; standalone heading-only paragraphs (a lone word like "Background" or "Orders" with nothing else) were essentially absent from the raw text in this sample (only one incidental hit: `[2009] NSWCA 406 at [179]` ends "...No error has been shown in her Honour's dismissal of this claim. Orders" — where "Orders" functions as a genuine inline section break that got folded into the preceding paragraph by the text extraction). This is a useful corrective: real judgments in this corpus **do not reliably use bolded/numbered subheadings** the way a generic AI "IRAC-with-headers" template assumes; the section structure is there in substance (background → issues → consideration → orders) but is signalled by transitional sentences, not by markdown-style headers.

The most distinctive real structural convention — and the one most different from how an AI would default to writing a "judgment" — is the **panel structure of lead reasons + short concurrences**, seen repeatedly in the NSWCA sample. A three-judge NSWCA panel routinely produces one substantive judgment plus two one-or-two-line concurrences, not three independently reasoned essays:

- `[2024] NSWCA 249 at [1]` and `[199]`: "KIRK JA: I agree with McHugh JA." ... "GRIFFITHS AJA: I agree with McHugh JA."
- `[2016] NSWCA 152 at [1]` and `[178]`: "MEAGHER JA: I agree with Gleeson JA." ... "TOBIAS AJA: I agree with the orders proposed by Gleeson JA for the reasons he has expressed."
- `[2012] NSWCA 399 at [1]`: "McCOLL JA: I agree with Macfarlan JA's reasons and the orders his Honour proposes."
- `[2014] NSWCA 288 at [196]–[197]`: "GLEESON JA: I agree with the orders proposed by Ward JA for the reasons given by her Honour. I would add the following observation..." (a concurrence that then adds a substantive paragraph of its own — a common variant: agree, then supplement)

Orders themselves are stated in a small number of recurring formulas, usually as the final one or two paragraphs, sometimes under an explicit "Orders" or "I propose the following orders" transition and a numbered list:

- `[2005] NSWCA 32 at [106]`: "I would therefore propose the following orders: (1) Appeal allowed; (2) Set aside orders 1 and 2 made by Einstein J on 19 March 2004; (3) In lieu thereof the respondent to pay to the appellant the sum of $550,000 together with interest..."
- `[2001] NSWCA 61 at [179]`: "Accordingly, I would dismiss the appeal. I agree with the orders proposed by Heydon JA. **********" (the asterisks are a literal end-of-document marker preserved in the source text)
- `[2015] HCA 6 at [241]–[242]`: "The appeal should be allowed with costs. It should be ordered that paragraphs 1 and 2 of the orders of the Court of Appeal made on 10 April 2014 should be set aside. In their place, it should be ordered:"
- `[2024] HCA 7 at [246]`: "The Council's appeal should be dismissed with costs. The respondents should be granted special leave to cross-appeal but the cross-appeal should be dismissed with costs."

HCA joint judgments end the same way but as a single collective disposition rather than a chain of individual agreements, since the joint judgment already speaks with one voice for however many justices signed onto it; separate reasons from other members of the bench (concurring or dissenting) then follow as their own complete blocks, each ending in its own disposition sentence — e.g. `[2008] HCA 56 at [238]`, a separate judgment ending "I would dismiss the appeals and grant special leave to cross-appeal in each matter on the ground that s 85A of the Act enabled the Court to deal with the Trust property..." immediately after the joint reasons had already disposed of the matter.

---

## 8. Concurrence and dissent

Concurrence in NSWCA is typically a bare, unadorned sentence naming the judge agreed with — often *without* restating "for the reasons given by [Judge]", though that fuller form also occurs:

- `[1988] NSWCA 67 at [68]`: "I agree with the conclusions of Mahoney JA that any agreement was not conditioned upon any favourable reports for the reasons which his Honour gives in his judgment."
- `[1988] NSWCA 52 at [46]`: "I agree with the majority that the affidavit was misleading."
- `[2021] NSWCA 126 at [195]`: "DAVIES J: I agree with the reasons of McCallum JA and with the orders proposed by White JA." (agreeing with one judge's reasons but a *different* judge's orders — a real, precise variant worth noting; concurrence in NSWCA is not always monolithic "I agree with X" across both reasons and orders)

Dissent is signalled structurally rather than through a fixed dissent-announcing idiom. In the catchwords/headnote of `[1991] NSWCA 68 at [1]`, dissent is flagged parenthetically: "Mahoney JA: Clarke JA dissenting)". In `[2008] HCA 56 at [182]`, the dissenting judge's own reasons open by stating the fact of dissent plainly: "In view of the fact that this judgment dissents from the orders proposed by the other members of the Court, it will be brief in dealing with the other difficulties." Neither uses a formulaic "I respectfully dissent" (which, as noted above, returned zero hits in this sample).

HCA agreement can also be with "the joint reasons" as a collective entity rather than with a named individual, when the concurring judge is joining a multi-author joint judgment:

- `[2005] HCA 20 at [248]`: "It follows that, on the first and third issues, and not just on the first, the Commissioner is entitled to succeed. It is for these reasons that I agree in the orders proposed in the joint reasons."
- `[2013] HCA 34 at [234]`: "I agree with the orders proposed by Hayne, Bell and Keane JJ."

---

## 9. How citations are woven into sentences

"See" is the dominant signal phrase in both courts for a supporting-but-not-load-bearing citation, usually placed at the end of the sentence it supports rather than as a stand-alone sentence:

- `[1988] NSWCA 67 at [5]`: "...is not a matter which has been the subject of detailed argument and which need be pursued: see generally Greig and Davis "The Law of Contract", p 436..."
- `[1974] HCA 23 at [17]`: "The Supreme Courts of Calcutta, Madras and Bombay had Admiralty jurisdiction by virtue of the Acts and charters by which they were constituted — see Stephen, *History of the Criminal Law of England*, vol..."

"cf" is used, correctly, to flag a genuinely contrary or merely-adjacent authority, almost always mid-sentence after a full citation and typically in a footnote-heavy HCA passage or an NSWCA parenthetical:

- `[1991] NSWCA 68 at [101]`: "...a promise to pay "a substantial cut on all work done" has been held to be such: *Stevenson v Ellis* (1912) 29 WN (NSW) 52; cf a different view of "pay you handsomely" in *Kina v Ivanhoe Gold Corporation Ltd* (1908) 7 CLR 617."
- `[1997] HCA 31 at [42]`: "[1930] HCA 52; (1930) 44 CLR 319 at 330-331; but cf *Bonser v La Macchia* [1969] HCA 31; (1969) 122 CLR 177 at 182."

Note: "As this Court held in..." and "As the High Court held..." — phrases a generic AI writer reaches for constantly as a citation-signal template — returned **zero hits** in the entire 38-case sample. The real equivalent, when it occurs at all, is more circumstantial and specific, e.g. `[1996] HCA 56 at [262]`: "It was held in *Actors and Announcers Equity Association v Fontana Films Pty Ltd*, a case concerned with a provision operating to much the same effect as s 162 in its primary operation, that s 51(xx) of the Constitution authorises a law forbidding conduct engaged in for the purpose of causing loss or damage to a corporation..." — i.e., the case is named and its facts distinguished/aligned in the same breath, not cited as a bare abstract proposition.

Pinpoint citation to a specific judge within a multi-judge historical authority is routine and specific ("per Griffiths CJ" style):

- `[1995] NSWCA 166 at [118]`: "(1908) 5 CLR 647, 669 per Griffiths CJ"

Older HCA judgments in the sample (1972–1976) use a distinctive **"(at p345)" pinpoint-to-own-judgment convention** repeated after almost every paragraph — a citation habit essentially absent from the modern HCA sample, which instead uses bracketed footnote markers:

- `[1972] HCA 51 at [2]`: "...the plaintiffs have recovered substantially in excess of the amount paid in and should have their taxed costs of the action. (at p345)"
- `[1975] HCA 63 at [125]`: "In my opinion this appeal should also be dismissed. (at p678)"
- versus `[2007] HCA 46 at [237]`: "...s 90 of the Act (as well as the antecedent common law) provides that such resolution may not be achieved by reliance on admissions procured in circumstances that render their use unfair to the suspect [162]." (footnote-number citation, no inline pinpoint)

---

## 10. NSWCA vs HCA — differences actually observed (not assumed)

- **Voice**: NSWCA reasons are almost always written in first person singular ("I", "in my opinion") even where three judges sit, because each judge's block is written separately. HCA joint judgments are written in first person plural ("we"), e.g. `[1988] HCA 40 at [64]`: "It seems to us that s.56 operates to curtail the invocation and exercise of jurisdiction..." — a genuine "we" voice that doesn't occur in the NSWCA sample at all (NSWCA "we" only appears when two judges *jointly* write one set of reasons, e.g. `[2019] NSWCA 52 at [1]`: "BASTEN JA AND SACKVILLE AJA: We are grateful to Brereton JA...").
- **How counsel are named**: NSWCA text frequently names counsel and quotes/paraphrases their submissions at length, including a formal "Counsel for the Appellant: ... Counsel for the Respondent: ..." block at the end. HCA paragraph text in this sample almost never carries a "counsel for the respondent" attribution in the body of the reasons (that information sits in separate representation metadata, not in the reasons text) — "counsel for the appellant"/"counsel for the respondent" occurs at similar raw rates but "counsel for the respondent" returned **zero** hits in the HCA sample versus 17 in NSWCA, consistent with HCA reasons focusing on the State/party's position rather than which barrister said what.
- **Subject matter shapes register**: HCA in this sample skews constitutional/statutory-construction and criminal-appeal (duty of the Court to declare general law, e.g. `[1996] HCA 56`, `[2019] HCA 1`, `[2013] HCA 34`), producing more abstract, doctrine-first reasoning; NSWCA in this sample skews fact-dense negligence, contract, and professional-discipline appeals, producing much denser engagement with what "the primary judge found" on specific facts. This matches the brief's expectation but the actual textual signature of it is: NSWCA paragraphs contain far more specific dates, dollar figures, and named individuals per paragraph; HCA paragraphs contain far more named statutory sections and prior authorities per paragraph.
- **Historical citation style**: the "(at pXXX)" self-pinpoint convention in 1970s HCA judgments versus bracketed footnote numbers in 2000s+ HCA judgments is a clean, dateable shift (see section 9).
- **Latin/formality trend**: NSWCA shows a clean decline in Latin usage across the sampled eras (see section 6 table); HCA's trend is noisier in this sample and should not be treated as confirmed without a larger sample.

---

## 11. Patterns that shifted across the sampled eras — summary

- **Latin phrase density**: NSWCA declines steadily from the 1988–1999 cases to the 2015+ cases (4.01 → 0.91 → 0.27 per 10k words). HCA's decline is not clean in this sample (see caveat above).
- **Citation format**: HCA moves from inline "(at pXXX)" pinpoints (1970s) to bracketed footnote-number citations (2000s onward).
- **Gendered pronouns**: "her Honour" begins appearing in the NSWCA sample from 2009 onward, absent in the pre-2000 sample, tracking bench composition rather than a stylistic choice.
- **Sentence length**: no clean monotonic trend either direction — NSWCA is fairly flat (28.9–32.2 mean words) across all three eras; HCA's most recent bucket is longest, likely driven by subject matter (constitutional cases) rather than era per se.
- **Panel concurrence style**: the terse "[Judge] JA: I agree with [Judge] JA" one-liner appears throughout the NSWCA sample from 1988 to 2024 without visible change — this is a stable convention, not one that eras have altered.
