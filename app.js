/* Below the Frost Line. Sarasota, 1884–1946. A documentary apparatus in English,
   built on the engine of "Not Practicable" (after "The Shipping Point"). Vanilla JS, hash routes. */
"use strict";

const view = document.getElementById("view");
const D = { mods: null, plates: null, timeline: null, compare: null, texts: {} };

const S = {
  title: "Below the Frost Line", loading: "Loading…", allTexts: "← All texts", allCmp: "← All comparisons",
  citeAs: "cited as", cite: "Cite as", srcNote: "Source and editorial note", source: "Source",
  planned: "planned", notTaken: "not included", shipped: "Printed here", plannedH: "Planned",
  missingH: "Examined and not included", textsTag: "Texts", textsH: "The corpus",
  textsLede: "Every module can be read in full, in the words of its public-domain sources, each passage read against the page image. What was examined and not included is listed below, with the reason.",
  cmpTag: "Compare", cmpH: "Voices side by side", tlTag: "Timeline", tlH: "From the prospectus of 1884 to the history of 1946",
  platesTag: "Plates", platesH: "Maps, photographs, views", fail: "The apparatus could not be loaded: "
};
const SIDES = {
  promise: "Promise and capital", colony: "Settlers and visitors", law: "Law and violence", colour: "The colour line", work: "Work and land", town: "Town and county"
};

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const side = s => `<span class="side ${s}">${esc(SIDES[s] || s)}</span>`;
const plateOf = id => (D.plates.plates || []).find(p => p.id === id);
const getJSON = url => fetch(url).then(r => { if (!r.ok) throw new Error(url); return r.json(); });

async function boot() {
  [D.mods, D.plates, D.timeline, D.compare] = await Promise.all(
    ["data/modules.json", "data/plates.json", "data/timeline.json", "data/compare.json"].map(getJSON));
  document.getElementById("navCompare").hidden = !(D.compare.pairs || []).length;
  document.getElementById("navPlates").hidden = !(D.plates.plates || []).length;
  window.addEventListener("hashchange", route);
  route();
}

async function text(id) {
  if (!D.texts[id]) D.texts[id] = await getJSON(`data/${id}.json`);
  return D.texts[id];
}

function route() {
  const parts = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean);
  const [page, ...args] = parts;
  document.querySelectorAll(".top nav a").forEach(a => {
    const t = a.getAttribute("href").replace(/^#\/?/, "");
    a.classList.toggle("on", (t || "") === (page === "text" ? "texts" : page || ""));
  });
  view.innerHTML = "";
  window.scrollTo(0, 0);
  const pages = { "": overview, texts, text: reader, compare, timeline, plates, sources };
  (pages[page || ""] || overview)(args);
}

/* ------------------------------------------------------------ overview */
const OVERVIEW = {
  tag: "Sarasota Bay · Manatee and Sarasota Counties · 1884–1946",
  h: "Below the Frost Line",
  lede: "In October 1884 a company in Edinburgh offered its investors 47,000 acres on Sarasota Bay, where, its prospectus said, the most delicate vegetables grew in the open air and reached the northern markets in January and February, “as the lands are below the frost line”. A year later Scottish colonists arrived. Shortly after, one of them remembered, snow began to fall. For the next sixty years Sarasota was promised again and again — to colonists, to winter residents, to the buyers of lots in the boom of the 1920s — and each promise met the ground, the weather and the market.",
  body: "This apparatus follows the town through its public-domain record: the company's prospectus, the decisions of Florida's Supreme Court on the murders of 1884, newspapers from Pensacola to Chicago and the Sarasota Herald of the boom, gazetteers and promotional booklets, the census and the reports of federal and state agencies, and Karl H. Grismer's Story of Sarasota of 1946, which quotes colonists' memoirs that survive nowhere else. It asks who was promised what, who came and who left, and who belonged to the town and who was kept at its edge. Where the sources are silent, it says so.",
  q: [
    ["Who made Sarasota?", "A Scottish land company and the colonists it sent in 1885; the settlers and fishermen who were on the bay before them; the railroad that reached the town in 1903; winter residents with fortunes from Chicago and the circus; and the people, Black and white, who cleared, built, fished and harvested, and whose names the sources record far less often."],
    ["What did it promise, and what came of it?", "Land below the frost line in 1884; lots, hotels and islands in the boom of the 1920s. The census counted 840 people in the city in 1910, 2,149 in 1920 and 8,398 in 1930."],
    ["Where was the violence?", "In 1884 members of a vigilance committee killed the settler Harrison Riley and the postmaster Charles E. Abbe; Florida's Supreme Court upheld the convictions. In 1921 a former convict guard was held for the murder of a Black prisoner at Salt Springs, in the new county. In 1925 some 150 local Klansmen paraded in full regalia. Black residents lived at the edge of the town, in Black Bottom and, from about 1914, in Newtown."],
    ["Can one retrace it?", "A City of Glorified Opportunity, the companion game, lets you sell Sarasota across six decades, from the prospectus to the airfield, and holds every promise against what the sources record. Every card points to its passage here. The game is free, like this apparatus."]
  ],
  none: "The modules are in preparation; the Texts page lists them with their sources.",
  have: "What the apparatus contains", qs: "The questions"
};

function overview() {
  const O = OVERVIEW;
  view.innerHTML = `
  <div class="hero one"><div>
    <span class="tag">${esc(O.tag)}</span>
    <h1>${esc(O.h)}</h1>
    <p class="lede">${esc(O.lede)}</p>
    <p class="readable">${esc(O.body)}</p>
  </div></div>
  <h2>${esc(O.have)}</h2>
  ${D.mods.shipped.length ? "" : `<p class="fine">${esc(O.none)}</p>`}
  <div class="grid g2">${D.mods.shipped.map(m => card(m)).join("")}${(D.mods.planned || []).map(m => card(m, true)).join("")}</div>
  <h2>${esc(O.qs)}</h2>
  <div class="grid g2">${O.q.map(([h, p]) => `<div class="panel"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join("")}</div>`;
}

function card(m, planned) {
  const inner = `<div>${side(m.side)} <span class="fine">${esc(planned ? S.planned : m.zk || "")}</span></div>
    <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p>`;
  return planned ? `<div class="card planned">${inner}</div>` : `<a class="card" href="#/text/${m.id}">${inner}</a>`;
}

/* ------------------------------------------------------------ texts */
function texts() {
  const other = (list, label) => list.map(m => `
      <div class="card planned"><div>${side(m.side)} <span class="fine">${esc(label)}</span></div>
      <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p><p class="fine"><b>${esc(S.source)}:</b> ${esc(m.quelle)}</p></div>`).join("");
  view.innerHTML = `
    <span class="tag">${esc(S.textsTag)}</span><h1>${esc(S.textsH)}</h1>
    <p class="lede">${esc(S.textsLede)}</p>
    ${D.mods.shipped.length ? `<h2>${esc(S.shipped)}</h2><div class="grid g2">${D.mods.shipped.map(m => card(m)).join("")}</div>` : ""}
    ${(D.mods.planned || []).length ? `<h2>${esc(S.plannedH)}</h2><div class="grid g2">${other(D.mods.planned, S.planned)}</div>` : ""}
    ${(D.mods.missing || []).length ? `<h2 id="missing">${esc(S.missingH)}</h2><div class="grid g2">${other(D.mods.missing, S.notTaken)}</div>` : ""}`;
}

async function reader([id, secId, unitN]) {
  const m = D.mods.shipped.find(x => x.id === id);
  if (!m) { location.hash = "#/texts"; return; }
  view.innerHTML = `<p class="fine">${esc(S.loading)}</p>`;
  const t = await text(m.datei);
  const sec = t.sections.find(s => s.id === secId) || t.sections[0];
  view.innerHTML = `
    <p class="fine"><a href="#/texts">${esc(S.allTexts)}</a></p>
    <span class="tag">${side(m.side)} ${esc(t.jahr)} · ${esc(S.citeAs)} ${esc(sec.zk)} [n]</span>
    <h1>${esc(t.titel)}</h1>
    <p class="fine">${esc(t.autor)}</p>
    <nav class="toc">${t.sections.map(s => `<a href="#/text/${id}/${s.id}" class="${s.id === sec.id ? "on" : ""}">${esc(s.titel)}</a>`).join("")}</nav>
    <div class="panel readable"><h3>${esc(sec.titel)}</h3><p>${esc(sec.blurb)}</p>${sec.note ? `<p class="fine">${esc(sec.note)}</p>` : ""}</div>
    ${(sec.plates || []).length ? `<div class="grid g4 secplates">${sec.plates.map(plateOf).filter(Boolean).map(plateFig).join("")}</div>` : ""}
    ${sec.viz ? `<div class="viz" id="viz"><p class="fine">${esc(S.loading)}</p></div>` : ""}
    <div id="units"></div>
    <div class="panel readable hinweis"><span class="tag">${esc(S.srcNote)}</span>
      <p><b>${esc(S.source)}.</b> ${esc(t.quelle)}</p><p>${esc(t.hinweis)}</p></div>`;
  bindPlates(view);
  if (sec.viz) fetch(`assets/viz/${sec.viz}.svg`).then(r => r.ok ? r.text() : "").then(svg => {
    const el = document.getElementById("viz");
    if (el) el.innerHTML = svg || "";
  });
  const box = view.querySelector("#units");
  for (const u of sec.units) {
    box.insertAdjacentHTML("beforeend", `
      <div class="unit ${String(u.n) === unitN ? "hl" : ""}" id="u${u.n}">
        <div class="num"><a href="#/text/${id}/${sec.id}/${u.n}" title="${esc(S.cite)} ${esc(sec.zk)} [${u.n}]">[${u.n}]</a>
          ${u.pg ? `<span class="pg">${esc(u.pg)}</span>` : ""}</div>
        <div>${u.titel ? `<h4>${esc(u.titel)}</h4>` : ""}<div class="cols one"><div class="text">${esc(u.orig)}</div></div></div>
        ${u.note ? `<div class="note">${esc(u.note)}</div>` : ""}
      </div>`);
  }
  if (unitN) { const el = document.getElementById("u" + unitN); if (el) el.scrollIntoView({ block: "center" }); }
}

/* ------------------------------------------------------------ compare */
async function compare([pid]) {
  const CMP = D.compare;
  const pair = (CMP.pairs || []).find(p => p.id === pid);
  if (!pair) {
    view.innerHTML = `
      <span class="tag">${esc(S.cmpTag)}</span><h1>${esc(S.cmpH)}</h1>
      <p class="lede">${esc(CMP.lede)}</p>
      <div class="grid g2">${(CMP.pairs || []).map(p => `<a class="card" href="#/compare/${p.id}">
        <h3>${esc(p.titel)}</h3><p class="fine">${esc(p.frage)}</p></a>`).join("")}</div>`;
    return;
  }
  view.innerHTML = `<p class="fine"><a href="#/compare">${esc(S.allCmp)}</a></p><p class="fine">${esc(S.loading)}</p>`;
  const docs = await Promise.all(pair.voices.map(v => {
    const m = D.mods.shipped.find(x => x.id === v.text);
    return text(m.datei).then(t => ({ v, m, t }));
  }));
  const col = ({ v, m, t }) => {
    const sec = t.sections.find(s => s.id === v.sec);
    const units = v.n.map(n => sec.units.find(u => u.n === n)).filter(Boolean);
    return `<div class="voice">
      <div class="vhead">${side(m.side)} <b>${esc(v.wer || t.autor)}</b><br><span class="fine">${esc(t.jahr)} · ${esc(sec.titel)}</span></div>
      ${units.map(u => `<div class="vunit"><div class="fine"><a href="#/text/${m.id}/${sec.id}/${u.n}">${esc(sec.zk)} [${u.n}]</a>${u.titel ? ` · ${esc(u.titel)}` : ""}</div>
        <div class="text">${esc(u.orig)}</div></div>`).join("")}
    </div>`;
  };
  view.innerHTML = `
    <p class="fine"><a href="#/compare">${esc(S.allCmp)}</a></p>
    <span class="tag">${esc(S.cmpTag)}</span><h1>${esc(pair.titel)}</h1>
    <p class="lede">${esc(pair.frage)}</p>
    <div class="panel readable"><p>${esc(pair.note)}</p></div>
    <div class="cmp n${docs.length}">${docs.map(col).join("")}</div>`;
}

/* ------------------------------------------------------------ timeline */
function timeline() {
  const TL = D.timeline;
  view.innerHTML = `
    <span class="tag">${esc(S.tlTag)}</span><h1>${esc(S.tlH)}</h1>
    <p class="lede">${esc(TL.lede)}</p>
    <div class="legend">${Object.keys(SIDES).map(side).join(" ")}</div>
    <div class="tl">${TL.stations.map(s => {
      const p = s.plate && plateOf(s.plate);
      return `<div class="st" style="--c:var(--${s.side})">
        <div><div class="d">${esc(s.d)} · ${side(s.side)}</div><h3>${esc(s.titel)}</h3><p>${esc(s.text)}</p>
        ${s.cite ? `<p class="fine"><a href="${s.cite}">✦ ${esc(s.citeLabel)}</a></p>` : ""}
        ${s.quelle ? `<p class="fine">${esc(s.quelle)}</p>` : ""}</div>
        ${p ? `<img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}" title="${esc(p.titel)}">` : "<span></span>"}
      </div>`;
    }).join("")}</div>`;
}

/* ------------------------------------------------------------ plates */
function plates() {
  view.innerHTML = `
    <span class="tag">${esc(S.platesTag)}</span><h1>${esc(S.platesH)}</h1>
    <p class="lede">${esc(D.plates.lede)}</p>
    <div class="grid g4">${D.plates.plates.map(plateFig).join("")}</div>
    <p class="fine">${esc(D.plates.credit)}</p>`;
  bindPlates(view);
}
function plateFig(p) {
  return `<figure class="plate card"><a href="#" data-p="${p.id}"><img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}"></a>
      <figcaption>${side(p.side)} <b>${esc(p.titel)}</b><br>${esc(p.caption)}<br><i>${esc(p.source)}</i></figcaption></figure>`;
}
function bindPlates(root) {
  root.querySelectorAll("[data-p]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const p = plateOf(a.dataset.p);
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `<figure><img src="assets/plates/${p.id}.jpg" alt="${esc(p.titel)}"><figcaption class="cap"><b>${esc(p.titel)}.</b> ${esc(p.caption)}</figcaption></figure>`;
    lb.onclick = () => lb.remove();
    document.body.append(lb);
  });
}

/* ------------------------------------------------------------ sources */
const METHOD = {
  tag: "Sources, method, limits", h: "How this apparatus is made",
  p: [
    ["Public domain only.", "The texts here were published before 1931, or are works of the United States government (the census, the reports of federal agencies, congressional documents) or decisions of Florida's courts, or were published later without a renewed copyright. Karl H. Grismer's Story of Sarasota (1946) carries a notice but was not renewed in 1973 or 1974, when renewal was due; it is in the public domain. Florida's agency publications are used where the state claims no copyright. Each passage is read against the page image. Recent research is named and summarized as such, never printed; the WPA guide to Florida (1939), whose copyright was renewed, is not quoted."],
    ["Promoters and witnesses.", "Much of what was printed about Sarasota was written to sell it: prospectuses, booklets, advertisements, the pages of its own newspaper. The apparatus says whose words a passage carries — a company's, a colonist's, a court's, a reporter's — and sets the promise next to the record."],
    ["Grismer's book.", "Grismer wrote in 1946 as a local historian of the town's leading families, with their language about Black residents and with scenes in which he invents the words spoken. His book is used for the memoirs and documents it quotes and for facts that can be checked; its invented dialogue is never cited as a source."],
    ["Whose voices.", "The Black residents of Sarasota, the fishermen of the bay, the labourers of the colony and the hands in the celery fields speak in these sources mostly through others: a directory, a police report, a promoter. Where a voice is missing, the apparatus says so and does not invent it."],
    ["Boundaries.", "Sarasota and the country around its bay that became Sarasota County in 1921, from the prospectus of 1884 to Grismer's history of 1946. What came before is told only as far as these sources tell it; the decades after 1946, the gardens and the art colony of the post-war town, are outlook, not subject."]
  ],
  printed: "Sources printed here", plates: "Plates"
};

function sources() {
  const M = METHOD;
  view.innerHTML = `
    <span class="tag">${esc(M.tag)}</span><h1>${esc(M.h)}</h1>
    <div class="readable">${M.p.map(([b, p]) => `<p><b>${esc(b)}</b> ${esc(p)}</p>`).join("")}</div>
    ${D.mods.shipped.length ? `<h2>${esc(M.printed)}</h2>
    <div class="grid g2">${D.mods.shipped.map(m => `<div class="panel"><b>${esc(m.kurz)}</b><p class="fine" id="src-${m.id}">…</p></div>`).join("")}</div>` : ""}
    ${(D.plates.plates || []).length ? `<h2>${esc(M.plates)}</h2><p class="fine readable">${esc(D.plates.credit)}</p>` : ""}`;
  D.mods.shipped.forEach(async m => {
    const t = await text(m.datei);
    const el = document.getElementById("src-" + m.id);
    if (el) el.textContent = t.quelle;
  });
}

boot().catch(e => { view.innerHTML = `<p>${esc(S.fail)}${esc(e.message)}</p>`; });
