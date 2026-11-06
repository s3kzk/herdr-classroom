// The buildings a look draws the spaces in. A look is a building (`kind`) and its
// colors; the building decides what sits on top (crown), between floors (ledge) and at
// the bottom (base), how far its walls stand in from the edges (inset, in art pixels),
// and how a room's window is dressed (`win`). Pictures are pixel art in icons/, sized
// from art.js so they keep their proportions; one art pixel is `u` (2u for scenery).
//
// Cost: a building's scenery is a few pictures and bands drawn once per render; a
// window adds at most about as many elements as the school's.
import { div, image } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { ART } from "./art.js";

const pic = (name, s) => {
  const [w, h] = ART[name];
  return image(`mods/rooms/icons/${name}.svg`).w(w * s).h(h * s);
};
const times = (n, f) => Array.from({ length: n }, (_, i) => f(i));
const tall = (name) => ART[name][1];

const SCHOOL = { top: "transom", side: "curtain", under: "sill", prop: "board" };

// The buildings, in the order the header lists them.
export const BUILDING_LIST = [
  { key: "school", name: "School" },
  { key: "office", name: "Office" },
  { key: "apartment", name: "Apartment" },
  { key: "hotel", name: "Hotel" },
  { key: "submarine", name: "Submarine" },
  { key: "rocket", name: "Rocket" },
  { key: "castle", name: "Castle" },
  { key: "ryokan", name: "Ryokan" },
  { key: "sento", name: "Sento" },
];

// The towns a building can stand in: a band of their landmarks over its roof.
export const TOWNS = [
  { key: "", name: "No town" },
  { key: "tokyo", name: "Tokyo" },
  { key: "kyoto", name: "Kyoto" },
  { key: "osaka", name: "Osaka" },
  { key: "fuji", name: "Mt. Fuji" },
];
// The landmarks are drawn at 1.5 art pixels per picture pixel, to read as a town from
// a sidebar; the band's height in art pixels holds the tallest of them (a 40-pixel tower).
const TOWN_K = 1.5;
const TOWN_H = 64;
// Each town's sky: the top of the band, and the horizon it fades to behind the roof.
const TOWN_SKY = {
  tokyo: { day: ["#7cc4f2", "#cfeaf8"], night: ["#1b1f4a", "#46306e"] },
  kyoto: { day: ["#f3b88f", "#fbe1c4"], night: ["#1d2340", "#4a3456"] },
  osaka: { day: ["#89d0f0", "#e3f4fb"], night: ["#1a1d3d", "#5a2850"] },
  fuji: { day: ["#6fb0ea", "#d6ecfa"], night: ["#14203f", "#2c406e"] },
};
export const townSky = (p) => (p.town ? TOWN_SKY[p.town][p.time] : null);

// Each building by day. Its night is made from it (below), except the school's,
// which was drawn by hand.
const DAY = {
  school: { win: SCHOOL,
    wall: "#e8dcc4", edge: "#cbbd9f", ledge: "#bfae8c", roof: "#a8463c", roofHi: "#c8644f", eave: "#7a2f28",
    frame: "#f6f6f2", sill: "#d9d6cc", glass: "#b7d7ea", transom: "#cfe5f2", curtain: "#f3e7c9", fold: "#ddcda6", board: "#2f5a43", boardRim: "#8a6a45",
    deskTop: "#e2b57a", desk: "#a8743e", leg: "#9aa0a6", plate: "#ffffff", ink: "#33302a", door: "#8b6a4a", step: "#cfc8b8", ground: "#5c9a44", groundDark: "#467a33" },
  apartment: { win: { top: "shutter", side: "curtain", under: "balcony", prop: "tv" },
    wall: "#c98b6b", edge: "#a46a4f", ledge: "#ece6dc", ledgeShade: "#c9c0b2", parapet: "#ece6dc", parapetHi: "#ffffff",
    frame: "#d5d9dd", glass: "#d9ecf5", shutter: "#b9bfc5", shutterEdge: "#9aa1a8", curtain: "#fbf7ee", fold: "#e7dfcf",
    tv: "#3a3f47", screen: "#7fc4e8", rail: "#5d6670", futon: "#f2a7b8", futonEdge: "#d9839a",
    seat: "sofa", deskTop: "#7a9cc6", desk: "#4f6d99", leg: "#3a3f47", plate: "#ffffff", ink: "#3a3f47",
    canopy: "#5d6670", door: "#8d959d", step: "#cfc8b8", curb: "#b9bcc0", ground: "#6f7378" },
  hotel: { win: { top: "valance", side: "drape", under: "planter", prop: "painting" },
    wall: "#7c2f3b", edge: "#5e2029", ledge: "#5e2029", gold: "#e6b450", roof: "#3b3f5c", roofHi: "#55597a",
    frame: "#f1e6cf", glass: "#d6e8f0", curtain: "#b3263a", fold: "#7d1626",
    painting: "#c9a24a", paintSky: "#8ec5e8", paintHill: "#5f9e5a",
    seat: "bed", deskTop: "#fbf8f0", desk: "#e6c47a", leg: "#5a2d18", plate: "#e6c47a", ink: "#3b2414",
    box: "#5a3a22", flowers: ["#ff6b8a", "#ffd166", "#ffffff", "#ff6b8a", "#ffd166"],
    awning: "#b3263a", awning2: "#f4ead6", carpet: "#a3192e", door: "#3b2414", step: "#c9bfae", ground: "#5d6170", groundDark: "#454956" },
  submarine: { win: { round: 7, rivets: true, prop: "pipes", lights: true },
    wall: "#4d6170", edge: "#33434f", ledge: "#3b4c59", rivet: "#8aa0b0",
    frame: "#c99a3a", glass: "#bfe3d6", pipe: "#5f7685", pipe2: "#a8743e", gauge: "#f4f1e8",
    deskTop: "#8b9aa6", desk: "#5d6c78", leg: "#3b4c59", lights: ["#ff5f5f", "#6dff9a"], plate: "#f2c14e", ink: "#262626",
    ground: "#d9c48c", groundDark: "#b9a36a" },
  rocket: { win: { round: 6, prop: "screens", lights: true },
    wall: "#eef1f5", edge: "#c3cad3", ledge: "#c3cad3", roof: "#d6453d", roofHi: "#ef6b5f",
    frame: "#8d99a6", glass: "#dce8f6", screen: "#1f2b45", screenLine: "#5ef0a0",
    deskTop: "#aeb8c3", desk: "#7b8794", leg: "#5b6673", lights: ["#ff5f5f", "#5ef0a0"], plate: "#1f2b45", ink: "#ffffff",
    nozzle: "#4a4f5a", nozzleHi: "#6a707c", pad: "#5b6673", padHi: "#8d99a6", groundDark: "#3f4752" },
  castle: { win: { top: "lattice", side: "shoji", prop: "scroll" },
    wall: "#f4f0e6", edge: "#2e2e33", siding: "#2e2e33", sidingHi: "#4a4a52", roof: "#45536a", roofHi: "#6a7a94",
    frame: "#3b2a1e", glass: "#efe2c0", transom: "#efe2c0", curtain: "#faf6ec", fold: "#3b2a1e",
    scroll: "#f7f2e4", rod: "#3b2a1e", scrollInk: "#4a4a52",
    seat: "low", cushion: "#8a2f22", cup: "#7fa66a", deskTop: "#5a3420", desk: "#3b2216", leg: "#2e1a12", plate: "#c9a06a", ink: "#2e1a12",
    stones: ["#8d8b84", "#a19f97", "#77756f"], mortar: "#5c5a55", water: "#3f7fae", waterHi: "#7fb6dc", waterDark: "#2f5f86" },
  office: { win: { top: "blinds", prop: "chart" },
    wall: "#5f7f99", edge: "#3e566b", ledge: "#2f4456", ledgeHi: "#8fa9bf", parapet: "#9fb3c4", parapetHi: "#d9e1e8",
    frame: "#d9e1e8", glass: "#e8f1f7", blind: "#c4ccd3", board: "#ffffff", boardRim: "#8d969e", bar: ["#3d7be0", "#2ecc71", "#f39c12"],
    deskTop: "#d0d5da", desk: "#8d969e", leg: "#5d6670", plate: "#ffffff", ink: "#2f4456",
    canopy: "#2f4456", door: "#3e566b", step: "#cfd4d8", curb: "#b9bcc0", ground: "#6f7378" },
  ryokan: { win: { top: "sudare", side: "shoji", under: "railing", prop: "ikebana" },
    wall: "#efe5d0", edge: "#4a3222", roof: "#3d4250", roofHi: "#5b6274", rail: "#6b4a2e",
    frame: "#5a3b26", glass: "#f1e4c4", sudare: "#c9a96b", sudareLine: "#9c7c45", curtain: "#faf6ec", fold: "#5a3b26",
    vase: "#3a5a7a", flower: ["#d8402f", "#f2a33a", "#d8402f"], stem: "#4f7a2c",
    seat: "low", cushion: "#6b4a8c", cup: "#7fa66a", deskTop: "#8a5a34", desk: "#5a3b26", leg: "#3b2616", plate: "#f4efe2", ink: "#3b2616",
    noren: "#2c3e6b", norenHi: "#f4efe2", door: "#c9b48a", stone: "#a19f97", gravel: "#cfc6b0", moss: "#6f8f4a" },
  sento: { win: { top: "transom", under: "sill", prop: "fuji" },
    wall: "#e9dfca", edge: "#4a3222", ledge: "#6b4a2e", roof: "#3d4250", roofHi: "#5b6274",
    frame: "#6b4a2e", sill: "#c9b48a", glass: "#d8eef0", transom: "#e8f6f7",
    mural: "#7fc0e8", fuji: "#3f6fa8", snow: "#ffffff", lake: "#5a9fd0",
    seat: "tub", water: "#9fd8ea", deskTop: "#c9a96b", desk: "#8a6a45", leg: "#5a3b26", plate: "#f4efe2", ink: "#3b2616",
    norenM: "#2c3e6b", norenW: "#c0392b", norenHi: "#f4efe2", door: "#c9b48a", step: "#cfc8b8", ground: "#8a8478", groundDark: "#6f6a60" },
};

const SCHOOL_NIGHT = { win: SCHOOL,
  wall: "#3d4160", edge: "#2f3350", ledge: "#2a2e48", roof: "#5a4b8f", roofHi: "#7464ad", eave: "#3a2f63",
  frame: "#8a91b8", sill: "#6b7196", glass: "#f5d67f", transom: "#f9e3a3", curtain: "#e8b85c", fold: "#cf9a3a", board: "#244636", boardRim: "#6b4f33",
  deskTop: "#c99a5e", desk: "#7d5a33", leg: "#6b7196", plate: "#e8eaf6", ink: "#23263d", door: "#2a2e48", step: "#4a4f6e", ground: "#25412c", groundDark: "#1b3020",
  off: { glass: "#20253d", transom: "#262c48", curtain: "#2e3556", fold: "#262c48", board: "#1b2a26" } };

// At night the rest of a building goes toward the night sky; a room with someone
// awake keeps its light (these), and one where everyone sleeps goes dark.
const LIT = {
  apartment: { glass: "#ffe3a3", curtain: "#f6e7c4", fold: "#e0c992", screen: "#7fc4e8" },
  hotel: { glass: "#ffd98a", curtain: "#b3263a", fold: "#7d1626", gold: "#e6b450", painting: "#c9a24a", paintSky: "#8ec5e8", paintHill: "#5f9e5a" },
  submarine: { glass: "#a9d9c8", frame: "#b8892f", gauge: "#f4f1e8" },
  rocket: { glass: "#dce8f6", screen: "#1f2b45", screenLine: "#5ef0a0" },
  castle: { glass: "#ffe2a6", transom: "#ffe2a6", curtain: "#fff3d6", scroll: "#f7f2e4" },
  office: { glass: "#fff2c2", blind: "#e6d9a8", board: "#ffffff", bar: ["#3d7be0", "#2ecc71", "#f39c12"] },
  ryokan: { glass: "#ffe2a6", curtain: "#fff3d6", sudare: "#d9b56b", vase: "#3a5a7a", flower: ["#d8402f", "#f2a33a", "#d8402f"] },
  sento: { glass: "#e8f6f7", transom: "#fff2c2", mural: "#7fc0e8", fuji: "#3f6fa8", snow: "#ffffff", lake: "#5a9fd0" },
};
const ROOM = ["glass", "transom", "curtain", "fold", "board", "tv", "screen", "screenLine", "painting", "paintSky", "paintHill", "scroll", "scrollInk", "shutter", "pipe", "pipe2", "gauge",
  "blind", "bar", "sudare", "vase", "flower", "mural", "fuji", "snow", "lake"];
const NAVY = [29, 33, 64];
const dim = (hex, k) => {
  const n = parseInt(hex.slice(1), 16);
  return "#" + [n >> 16, (n >> 8) & 255, n & 255].map((v, i) => Math.round(v + (NAVY[i] - v) * k).toString(16).padStart(2, "0")).join("");
};
const isColor = (v) => typeof v === "string" && v.startsWith("#");
const darken = (o, k) => Object.fromEntries(Object.entries(o).map(([key, v]) =>
  [key, isColor(v) ? dim(v, k) : Array.isArray(v) ? v.map((x) => (isColor(x) ? dim(x, k) : x)) : v]));

function nightOf(key) {
  const day = DAY[key];
  const off = Object.fromEntries(ROOM.filter((k) => k in day).map((k) => [k, Array.isArray(day[k]) ? day[k].map((x) => dim(x, 0.82)) : dim(day[k], 0.82)]));
  return { ...darken(day, 0.55), plate: day.plate, ink: day.ink, ...(day.lights ? { lights: day.lights } : {}), ...LIT[key], off };
}

// The look of a building at a time of day: its colors, its pictures (`art`), its
// window dressing (`win`). Made once each.
const made = new Map();
export function look(building, time, town = "") {
  const key = `${building}-${time}-${town}`;
  if (!made.has(key)) {
    const school = building === "school";
    const colors = time === "night" ? (school ? SCHOOL_NIGHT : nightOf(building)) : DAY[building];
    made.set(key, { ...colors, kind: building, art: school ? time : `${building}-${time}`, town, time });
  }
  return made.get(key);
}

// The town over the roof: its sky, a far row (skyline, hills or a lake) across the
// width, landmarks at the sides (L, R), nearer the middle (M, N) and in it (C), and a
// train in front (T). `width` is the building's, in screen pixels before the zoom.
export function skyline(p, u, width) {
  if (!p.town) return null;
  const name = (part) => `town-${p.town}-${part}-${p.time}`;
  const has = (part) => Boolean(ART[name(part)]);
  const k = TOWN_K * u, [skyTop, skyLow] = townSky(p);
  const farW = has("far") ? ART[name("far")][0] * k : 0;
  const at = (part, place) => place(pic(name(part), k).absolute().bottom(0));
  return v_flex().relative().w_full().h(TOWN_H * u).overflow_hidden().bg(skyTop)
    .child(div().absolute().bottom(0).left(0).w_full().h("55%").bg(skyLow))
    .when(farW > 0, (el) => el.child(h_flex().absolute().bottom(0).left(0)
      .children(times(Math.ceil(width / farW) + 1, () => pic(name("far"), k)))))
    .when(has("C"), (el) => el.child(h_flex().absolute().bottom(0).left(0).w_full().justify_center().child(pic(name("C"), k))))
    .when(has("M"), (el) => el.child(at("M", (x) => x.left("24%"))))
    .when(has("N"), (el) => el.child(at("N", (x) => x.right("24%"))))
    .child(at("L", (x) => x.left(4 * u)))
    .child(at("R", (x) => x.right(4 * u)))
    .when(has("T"), (el) => el.child(h_flex().absolute().bottom(0).left(0).w_full().justify_center().child(pic(name("T"), k))));
}

// ---- a room's window ----

// Above the glass.
export function windowTop(kind, c, u) {
  if (kind === "transom") return h_flex().w_full().h(4 * u).gap(u).children(times(3, () => div().flex_1().h_full().bg(c.transom)));
  if (kind === "shutter") return div().w_full().h(3 * u).bg(c.shutter).border_b(u).border_color(c.shutterEdge);
  if (kind === "valance") return div().w_full().h(3 * u).bg(c.curtain).border_b(u).border_color(c.gold);
  if (kind === "blinds") return v_flex().w_full().h(4 * u).gap(u).bg(c.glass).children(times(2, () => div().w_full().h(1.5 * u).bg(c.blind)));
  if (kind === "sudare") return div().w_full().h(3 * u).bg(c.sudare).border_b(u).border_color(c.sudareLine);
  if (kind === "lattice") return h_flex().w_full().h(3 * u).px(u).justify_between().bg(c.transom).children(times(6, () => div().w(u).h_full().bg(c.frame)));
  return null;
}

// Both sides of the glass, over the room.
export function windowSides(kind, c, u) {
  if (!kind) return [];
  const w = kind === "curtain" ? 3 * u : 4 * u;
  return ["l", "r"].map((side) => div().absolute().top(0).bottom(0).w(w).bg(c.curtain)
    .when(side === "l", (el) => el.left(0).border_r(u).border_color(c.fold))
    .when(side === "r", (el) => el.right(0).border_l(u).border_color(c.fold))
    // A drape is tied back; a shoji has a crosspiece.
    .when(kind === "drape", (el) => el.child(div().absolute().top("58%").left(0).w_full().h(u).bg(c.gold)))
    .when(kind === "shoji", (el) => el.child(div().absolute().top("40%").left(0).w_full().h(u).bg(c.fold))));
}

// On the room's far wall.
export function backdrop(kind, c, u) {
  const at = () => h_flex().absolute().top(2 * u).left(0).w_full().justify_center();
  if (kind === "board") return at().child(div().w("46%").h(4 * u).bg(c.board).border_b(u).border_color(c.boardRim));
  if (kind === "tv") return at().child(div().w(11 * u).h(7 * u).p(u).bg(c.tv).child(div().size_full().bg(c.screen)));
  if (kind === "painting") return at().child(v_flex().w(12 * u).h(7 * u).p(u).bg(c.painting)
    .child(div().w_full().flex_1().bg(c.paintSky)).child(div().w_full().h(2 * u).bg(c.paintHill)));
  if (kind === "screens") return at().gap(u).children(times(3, () => div().w(5 * u).h(4 * u).bg(c.screen).border_b(u).border_color(c.screenLine)));
  if (kind === "scroll") return h_flex().absolute().top(u).left(0).w_full().justify_center()
    .child(v_flex().w(5 * u).h(8 * u).items_center().pt(2 * u).bg(c.scroll).border_t(u).border_b(u).border_color(c.rod)
      .child(div().w(u).h(3 * u).bg(c.scrollInk)));
  if (kind === "chart") return at().child(h_flex().w(12 * u).h(7 * u).px(1.5 * u).pb(u).gap(u).items_end().bg(c.board).border(u).border_color(c.boardRim)
    .children(c.bar.map((b, i) => div().flex_1().h((2 + i * 1.5) * u).bg(b))));
  // A bathhouse's Mount Fuji on the wall: a stepped peak with snow over a lake.
  if (kind === "fuji") return at().child(v_flex().w(16 * u).h(8 * u).items_center().justify_end().bg(c.mural)
    .children([2, 4, 6, 8, 10, 12].map((w, i) => div().w(w * u).h(u).bg(i < 2 ? c.snow : c.fuji)))
    .child(div().w_full().h(u).bg(c.lake)));
  // An alcove's flower arrangement: three blooms over a vase.
  if (kind === "ikebana") return h_flex().absolute().top(u).left(0).w_full().justify_center()
    .child(v_flex().items_center()
      .child(h_flex().gap(u).children(c.flower.map((f) => div().size(u).bg(f))))
      .child(div().w(u).h(2 * u).bg(c.stem))
      .child(div().w(3 * u).h(3 * u).bg(c.vase)));
  if (kind === "pipes") return v_flex().absolute().top(2 * u).left(0).w_full().gap(u)
    .child(div().w_full().h(u).bg(c.pipe)).child(div().w_full().h(u).bg(c.pipe2))
    .child(div().absolute().top(3 * u).right(5 * u).size(4 * u).rounded(2 * u).bg(c.gauge).border(u).border_color(c.pipe));
  return null;
}

// Under the window. A balcony sometimes airs a futon (the same rooms each time).
export function windowUnder(kind, c, u, airing) {
  if (kind === "sill") return div().w_full().h(1.5 * u).bg(c.sill);
  if (kind === "balcony") return v_flex().relative().w_full().h(6 * u).border_t(u).border_b(u).border_color(c.rail)
    .child(h_flex().w_full().h_full().px(2 * u).justify_between().children(times(6, () => div().w(u).h_full().bg(c.rail))))
    .when(airing, (el) => el.child(div().absolute().top(-u).left("16%").w("40%").h(5 * u).bg(c.futon).border_b(u).border_color(c.futonEdge)));
  // An engawa's wooden railing.
  if (kind === "railing") return h_flex().w_full().h(4 * u).px(u).justify_between().border_t(u).border_b(u).border_color(c.rail)
    .children(times(8, () => div().w(u).h_full().bg(c.rail)));
  if (kind === "planter") return v_flex().w_full().items_center()
    .child(h_flex().w("74%").h(u).justify_between().children(c.flowers.map((f) => div().w(u).h_full().bg(f))))
    .child(div().w("82%").h(2 * u).bg(c.box));
  return null;
}

// How much a window's dressing adds to its height, in art pixels: the top and the
// gap under it, and what hangs below. Kept with windowTop and windowUnder above.
const TOP_RISE = { transom: 4, shutter: 3, valance: 3, lattice: 3, blinds: 4, sudare: 3 };
const UNDER_RISE = { sill: 1.5, balcony: 6, planter: 3, railing: 4 };
const winRise = (w) => (w.top ? TOP_RISE[w.top] + 1 : 0) + (UNDER_RISE[w.under] ?? 0);

// A porthole's rivets.
export const rivets = (c, u) => [
  div().absolute().top(0.25 * u).left(6 * u).size(u).bg(c.edge),
  div().absolute().top(0.25 * u).right(6 * u).size(u).bg(c.edge),
  div().absolute().bottom(0.25 * u).left(6 * u).size(u).bg(c.edge),
  div().absolute().bottom(0.25 * u).right(6 * u).size(u).bg(c.edge),
];

// ---- the building ----

const sky = (p, u) => [
  pic(`skyL-${p.art}`, 2 * u).absolute().top(2 * u).left(4 * u),
  pic(`skyR-${p.art}`, 2 * u).absolute().top(4 * u).right(4 * u),
];
const top = (p, u) => v_flex().relative().w_full().items_center().pt(4 * u).children(sky(p, u));
// A band as wide as the walls, with their edges.
const band = (p, u, ins, h, bg) => h_flex().w_full().px(ins)
  .child(div().flex_1().h(h).bg(bg).border_l(2 * u).border_r(2 * u).border_color(p.edge));
// A Japanese eave with upturned ends.
const eave = (p, u) => v_flex().w_full()
  .child(h_flex().w_full().justify_between().child(div().w(2 * u).h(u).bg(p.roofHi)).child(div().w(2 * u).h(u).bg(p.roofHi)))
  .child(div().w_full().h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi));
const doors = (p, u, w, h, frame) => {
  const door = () => v_flex().flex_1().h_full().bg(p.door).p(u).child(div().w_full().h(8 * u).bg(p.glass));
  return h_flex().w(w * u).h(h * u).gap(u).p(u).bg(frame).child(door()).child(door());
};
// The ground floor's wall with pictures at its feet on both sides.
const lobby = (p, u, h, left, right, middle) => h_flex().relative().w_full().h(h * u).justify_center().items_end()
  .bg(p.wall).border_l(2 * u).border_r(2 * u).border_color(p.edge)
  .child(left.absolute().bottom(0).left(4 * u)).child(right.absolute().bottom(0).right(4 * u)).child(middle);

// Each building's height in art pixels, as drawn below: what sits on top (crown),
// between floors (ledge) and at the bottom (base). main.js sizes the building to the
// panel with them, so a change to a drawing changes its numbers too.
export const BUILDINGS = {
  school: {
    rise: { crown: (p) => 4 + tall(`tower-${p.art}`) * 1.5 + 5 * 3 + 2, ledge: 2, base: 30 + 3 + 2 },
    inset: 0,
    // The sky and a stepped roof under a clock tower.
    crown: (p, u) => top(p, u).child(pic(`tower-${p.art}`, 1.5 * u))
      .children(["34%", "50%", "66%", "82%", "100%"].map((w) => div().w(w).h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi)))
      .child(div().w_full().h(2 * u).bg(p.eave)),
    ledge: (p, u, ins) => band(p, u, ins, 2 * u, p.ledge),
    // A canopy over two glass doors and steps, a tree each side.
    base: (p, u) => v_flex().w_full()
      .child(lobby(p, u, 30, pic(`tree-${p.art}`, 2 * u), pic(`tree-${p.art}`, 2 * u), v_flex().items_center()
        .child(div().w(36 * u).h(2 * u).bg(p.eave))
        .child(doors(p, u, 28, 18, p.frame))
        .child(div().w(32 * u).h(2 * u).bg(p.step))
        .child(div().w(36 * u).h(2 * u).bg(p.step).opacity(0.85))))
      .child(div().w_full().h(3 * u).bg(p.ground))
      .child(div().w_full().h(2 * u).bg(p.groundDark)),
  },
  apartment: {
    rise: { crown: (p) => 4 + tall(`roof-${p.art}`) * 2 + 1 + 2, ledge: 2, base: 30 + 2 + 3 },
    inset: 0,
    // A flat roof: the stair hut, the water tank and an antenna behind a parapet.
    crown: (p, u) => top(p, u).child(pic(`roof-${p.art}`, 2 * u))
      .child(div().w_full().h(u).bg(p.parapetHi))
      .child(div().w_full().h(2 * u).bg(p.parapet).border_b(u).border_color(p.ledgeShade)),
    // Each floor's slab runs out past the walls as the balconies' floor.
    ledge: (p, u) => div().w_full().h(2 * u).bg(p.ledge).border_b(u).border_color(p.ledgeShade),
    // Bicycle and mailboxes, a glass door, a vending machine and a plant.
    base: (p, u) => v_flex().w_full()
      .child(lobby(p, u, 30, pic(`baseL-${p.art}`, 2 * u), pic(`baseR-${p.art}`, 2 * u), v_flex().items_center()
        .child(div().w(30 * u).h(2 * u).bg(p.canopy))
        .child(doors(p, u, 22, 20, p.frame))
        .child(div().w(26 * u).h(2 * u).bg(p.step))))
      .child(div().w_full().h(2 * u).bg(p.curb))
      .child(div().w_full().h(3 * u).bg(p.ground)),
  },
  hotel: {
    rise: { crown: (p) => 4 + tall(`sign-${p.art}`) * 2 + 3 * 3 + 2, ledge: 3, base: 32 + 3 + 2 },
    inset: 0,
    // A lit five-star sign over a mansard roof and a gilded cornice.
    crown: (p, u) => top(p, u).child(pic(`sign-${p.art}`, 2 * u))
      .children(["88%", "94%", "100%"].map((w) => div().w(w).h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi)))
      .child(div().w_full().h(2 * u).bg(p.gold)),
    ledge: (p, u) => div().w_full().h(3 * u).bg(p.ledge).border_t(u).border_color(p.gold),
    // A striped awning over gilt doors and a red carpet, lamps and topiaries.
    base: (p, u) => v_flex().w_full()
      .child(lobby(p, u, 32, pic(`baseL-${p.art}`, 2 * u), pic(`baseR-${p.art}`, 2 * u), v_flex().items_center()
        .child(h_flex().w(40 * u).h(4 * u).children(times(10, (i) => div().flex_1().h_full().bg(i % 2 ? p.awning2 : p.awning))))
        .child(div().w(40 * u).h(u).bg(p.gold).mb(3 * u))
        .child(doors(p, u, 26, 17, p.gold))
        .child(div().w(30 * u).h(2 * u).bg(p.carpet))
        .child(div().w(36 * u).h(2 * u).bg(p.carpet).opacity(0.85))))
      .child(div().w_full().h(3 * u).bg(p.ground))
      .child(div().w_full().h(2 * u).bg(p.groundDark)),
  },
  submarine: {
    rise: { crown: (p) => 4 + tall(`sail-${p.art}`) * 2 + 10, ledge: 3, base: 10 + 2 + 30 + 3 + 2 },
    inset: 0,
    // The sail and its periscope on the hull's rounded top.
    crown: (p, u) => top(p, u).child(pic(`sail-${p.art}`, 2 * u))
      .child(div().w_full().h(10 * u).bg(p.wall).rounded_t(10 * u).border_t(2 * u).border_l(2 * u).border_r(2 * u).border_color(p.edge)),
    ledge: (p, u) => h_flex().w_full().h(3 * u).px(6 * u).items_center().justify_between().bg(p.ledge)
      .border_l(2 * u).border_r(2 * u).border_color(p.edge).children(times(7, () => div().size(u).bg(p.rivet))),
    // The hull's rounded bottom and keel over a sandy sea floor.
    base: (p, u) => v_flex().w_full()
      .child(div().w_full().h(10 * u).bg(p.wall).rounded_b(10 * u).border_b(2 * u).border_l(2 * u).border_r(2 * u).border_color(p.edge))
      .child(h_flex().w_full().justify_center().child(div().w("36%").h(2 * u).bg(p.edge)))
      .child(h_flex().relative().w_full().h(30 * u)
        .child(pic(`baseL-${p.art}`, 2 * u).absolute().bottom(0).left(3 * u))
        .child(pic(`baseR-${p.art}`, 2 * u).absolute().bottom(0).right(3 * u)))
      .child(div().w_full().h(3 * u).bg(p.ground))
      .child(div().w_full().h(2 * u).bg(p.groundDark)),
  },
  rocket: {
    rise: { crown: (p) => 4 + tall(`tip-${p.art}`) * 2 + 10 * 3 + 2, ledge: 2, base: 8 + 3 + 2 + 3 + 18 + 3 + 2 },
    inset: 12,
    // A stepped red nose cone with a beacon.
    crown: (p, u, ins) => {
      return top(p, u).child(pic(`tip-${p.art}`, 2 * u))
        .child(h_flex().w_full().px(ins).child(v_flex().flex_1().items_center()
          .children(times(10, (i) => div().w(`${10 + i * 10}%`).h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi)))))
        .child(band(p, u, ins, 2 * u, p.ledge));
    },
    ledge: (p, u, ins) => band(p, u, ins, 2 * u, p.ledge),
    // A red band, the nozzle and its flame over the pad; fins either side reach down past the nozzle.
    base: (p, u, ins) => v_flex().relative().w_full()
      .child(h_flex().w_full().px(ins)
        .child(v_flex().flex_1().min_w(0)
          .child(div().w_full().h(8 * u).bg(p.wall).border_l(2 * u).border_r(2 * u).border_color(p.edge))
          .child(div().w_full().h(3 * u).bg(p.roof).border_l(2 * u).border_r(2 * u).border_color(p.edge))
          .child(v_flex().w_full().items_center()
            .child(div().w("46%").h(2 * u).bg(p.nozzleHi))
            .child(div().w("52%").h(3 * u).bg(p.nozzle)))))
      .child(h_flex().relative().w_full().h(18 * u).justify_center()
        .child(pic(`smoke-${p.art}`, 2 * u).absolute().bottom(0).left(2 * u))
        .child(pic(`smoke-${p.art}`, 2 * u).absolute().bottom(0).right(2 * u))
        .child(pic(`flame-${p.art}`, 2 * u)))
      .child(div().w_full().h(3 * u).bg(p.pad).border_t(u).border_color(p.padHi))
      .child(div().w_full().h(2 * u).bg(p.groundDark))
      .child(pic(`finL-${p.art}`, ins / 8).absolute().top(0).left(0))
      .child(pic(`finR-${p.art}`, ins / 8).absolute().top(0).right(0)),
  },
  castle: {
    rise: { crown: (p) => 4 + tall(`ridge-${p.art}`) * 2 + 4 * 3 + 4, ledge: 4 + 4, base: 5 * 5 + 3 + 2 },
    inset: 6,
    // Golden shachihoko on the ridge, a gable, tiled tiers and an eave.
    crown: (p, u) => top(p, u).child(pic(`ridge-${p.art}`, 2 * u))
      .children(["60%", "72%", "84%", "96%"].map((w) => div().w(w).h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi)))
      .child(eave(p, u)),
    // Black weatherboards under each floor's windows, then that floor's eave.
    ledge: (p, u, ins) => v_flex().w_full()
      .child(h_flex().w_full().px(ins).child(v_flex().flex_1().h(4 * u).bg(p.siding)
        .border_l(2 * u).border_r(2 * u).border_color(p.edge).child(div().w_full().h(u).bg(p.sidingHi))))
      .child(eave(p, u)),
    // A stone base widening to the moat, a pine each side.
    base: (p, u) => v_flex().w_full()
      .child(v_flex().relative().w_full().items_center()
        .children(["93%", "94.75%", "96.5%", "98.25%", "100%"].map((w, i) => h_flex().w(w).h(5 * u).gap(0.5 * u).pb(0.5 * u).bg(p.mortar)
          .children(times(7 + (i % 2), (j) => div().flex_1().h_full().bg(p.stones[(i + j) % 3])))))
        .child(pic(`pineL-${p.art}`, 2 * u).absolute().bottom(0).left(2 * u))
        .child(pic(`pineR-${p.art}`, 2 * u).absolute().bottom(0).right(2 * u)))
      .child(div().w_full().h(3 * u).bg(p.water).border_t(u).border_color(p.waterHi))
      .child(div().w_full().h(2 * u).bg(p.waterDark)),
  },
  office: {
    rise: { crown: (p) => 4 + tall(`roof-${p.art}`) * 2 + 1 + 2, ledge: 2, base: 30 + 2 + 3 },
    inset: 0,
    // Cooling units and a mast with a beacon behind a parapet.
    crown: (p, u) => top(p, u).child(pic(`roof-${p.art}`, 2 * u))
      .child(div().w_full().h(u).bg(p.parapetHi))
      .child(div().w_full().h(2 * u).bg(p.parapet)),
    // A dark spandrel between the glass floors.
    ledge: (p, u, ins) => h_flex().w_full().px(ins).child(div().flex_1().h(2 * u).bg(p.ledge).border_t(0.5 * u).border_color(p.ledgeHi)),
    // A canopy over glass doors, a bench and a plant each side.
    base: (p, u) => v_flex().w_full()
      .child(lobby(p, u, 30, pic(`baseL-${p.art}`, 2 * u), pic(`baseR-${p.art}`, 2 * u), v_flex().items_center()
        .child(div().w(34 * u).h(2 * u).bg(p.canopy))
        .child(doors(p, u, 24, 20, p.frame))
        .child(div().w(28 * u).h(2 * u).bg(p.step))))
      .child(div().w_full().h(2 * u).bg(p.curb))
      .child(div().w_full().h(3 * u).bg(p.ground)),
  },
  ryokan: {
    rise: { crown: (p) => 4 + tall(`ridge-${p.art}`) * 2 + 3 * 3 + 4, ledge: 4, base: 30 + 3 + 2 },
    inset: 4,
    // A tiled ridge with ogre tiles at its ends over a hipped roof.
    crown: (p, u) => top(p, u).child(pic(`ridge-${p.art}`, 2 * u))
      .children(["70%", "84%", "98%"].map((w) => div().w(w).h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi)))
      .child(eave(p, u)),
    // A tiled eave over each floor.
    ledge: (p, u) => eave(p, u),
    // Red lanterns either side of an indigo noren over the sliding door, stepping
    // stones on the gravel; a stone lantern with a maple, and one with bamboo.
    base: (p, u) => {
      const lantern = () => pic(`lantern-${p.art}`, 2 * u);
      const noren = h_flex().w_full().h(7 * u).gap(0.5 * u).children(times(3, () => div().flex_1().h_full().bg(p.noren)
        .child(div().mt(2 * u).mx_auto().w(2 * u).h(2 * u).rounded(u).bg(p.norenHi))));
      const door = v_flex().w(24 * u).h(20 * u).p(u).bg(p.frame).child(noren)
        .child(h_flex().w_full().flex_1().gap(u).children(times(2, () => div().flex_1().h_full().bg(p.door).border(0.5 * u).border_color(p.frame))));
      return v_flex().w_full()
        .child(lobby(p, u, 30, pic(`baseL-${p.art}`, 2 * u), pic(`baseR-${p.art}`, 2 * u), v_flex().items_center()
          .child(div().w(38 * u).h(2 * u).bg(p.roof).border_t(u).border_color(p.roofHi))
          .child(h_flex().items_start().gap(2 * u).child(lantern()).child(door).child(lantern()))
          .child(h_flex().gap(2 * u).children(times(3, () => div().w(5 * u).h(2 * u).bg(p.stone))))))
        .child(div().w_full().h(3 * u).bg(p.gravel))
        .child(div().w_full().h(2 * u).bg(p.moss));
    },
  },
  sento: {
    rise: { crown: (p) => 4 + tall(`roof-${p.art}`) * 2 + 2 * 3 + 4, ledge: 2, base: 30 + 3 + 2 },
    inset: 0,
    // A curved gable and the chimney with its smoke over a tiled roof.
    crown: (p, u) => top(p, u).child(pic(`roof-${p.art}`, 2 * u))
      .children(["90%", "100%"].map((w) => div().w(w).h(3 * u).bg(p.roof).border_t(u).border_color(p.roofHi)))
      .child(eave(p, u)),
    ledge: (p, u, ins) => band(p, u, ins, 2 * u, p.ledge),
    // The hot-spring sign over two noren, blue and red, and the sliding doors;
    // wash buckets on one side, a bottled-milk machine on the other.
    base: (p, u) => {
      const noren = (c) => h_flex().flex_1().h(7 * u).gap(0.5 * u).children(times(2, () => div().flex_1().h_full().bg(c)));
      return v_flex().w_full()
        .child(lobby(p, u, 30, pic(`baseL-${p.art}`, 2 * u), pic(`baseR-${p.art}`, 2 * u), v_flex().items_center()
          .child(pic(`sign-${p.art}`, u).mb(u))
          .child(v_flex().w(30 * u).h(16 * u).p(u).bg(p.frame)
            .child(h_flex().w_full().gap(u).child(noren(p.norenM)).child(noren(p.norenW)))
            .child(h_flex().w_full().flex_1().gap(u).children(times(2, () => div().flex_1().h_full().bg(p.door).border(0.5 * u).border_color(p.frame)))))
          .child(div().w(34 * u).h(2 * u).bg(p.step))))
        .child(div().w_full().h(3 * u).bg(p.ground))
        .child(div().w_full().h(2 * u).bg(p.groundDark));
    },
  },
};

// A building's heights in art pixels, with its windows' dressing.
export function rise(p) {
  const r = BUILDINGS[p.kind].rise;
  return { crown: r.crown(p) + (p.town ? TOWN_H : 0), ledge: r.ledge, base: r.base, win: winRise(p.win) };
}
