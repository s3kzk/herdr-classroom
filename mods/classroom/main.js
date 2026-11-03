// Spaces as rooms in a building, agents as the students in them: Claw'd, or the
// agent's own character drawn from Herdr's icons (see tools/students.py). The header
// shows the time of day (day from sunrise to sunset, by the clock) and the building (a
// press lists them: a school, an apartment, a hotel, a submarine, a rocket, a castle;
// looks.js draws each). A floor of windows per row of rooms, rooms with agents first
// and the most recently changed first within each; the rooms without agents sit under
// a plate that folds them away or shows them all. Through each window, a desk per
// agent with its student sitting at it, dressed for its status (hard hat and wrench
// while working, a hand up or a big "!" while it waits for you, confetti when done,
// a nightcap and a snot bubble while idle). At night a room whose students all sleep
// goes dark.
// The window's shoulder carries a warning (someone waits for you) or a check
// (someone finished). Resting the pointer on a window lists its students; a click
// goes to the space or the agent.
//
// The building is sized to the panel: its art shrinks in whole screen pixels, to half
// the usual size at most, and its columns change, so that it fits whole when it can.
//
// Cost: everything is still pictures; working students move in steps on a slow
// timer that runs only while someone works, so a quiet school doesn't redraw the window.
// render reads spaces() and agents() once and builds the hovered roster only. Resizing
// the panel redraws only when the size or columns picked for it change.
import { View, div, svg, image } from "gpui-kit";
import { v_flex, h_flex, Popup } from "gpui-base";
import { spaces, agents, run, theme, settings, props, openOverlay } from "herdr";
import { session } from "./session.js";
import { Menu, menuItems, menuHeight, probe, MENU_WIDTH } from "./menu.js";
import { sunTimes } from "./sun.js";
import { BUILDING_LIST, look, BUILDINGS, rise, windowTop, windowSides, backdrop, windowUnder, rivets } from "./looks.js";

// What was picked when looks were stored by position.
const OLD_LOOKS = ["school", "school", "apartment", "hotel", "submarine", "rocket", "castle"];

// Where the sun is reckoned for: Tokyo on Japan time, else the time zone's meridian.
const ZONE = new Date().getTimezoneOffset();
const [LAT, LNG] = ZONE === -540 ? [35.68, 139.77] : [35, -ZONE / 4];
const clock = (ms) => { const d = new Date(ms); return `${d.getHours()}:${String(d.getMinutes()).padStart(2, "0")}`; };

// A room narrower than this cuts its name plate short.
const MIN_TILE = 100;

const LABEL = { working: "Working", blocked: "Needs you", done: "Done", idle: "Idle" };
const ORDER = { blocked: 0, done: 1, working: 2, idle: 3 };
const ACC = ["a", "b", "c", "d"];

const hash = (s) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h; };
const pick = (list, key) => list[hash(key) % list.length];

// The program table's key first: its `match` folds names like "kiro-cli" and
// "cursor-agent" into one key, which the agent's own report alone would miss.
const BODIES = ["claude", "codex", "crush", "kiro", "pi", "gemini", "cursor", "opencode",
  "amp", "grok", "antigravity", "kimi", "qoder", "hermes"];
const ALIAS = new Map([["omp", "pi"], ["agy", "antigravity"]]);
function body(a) {
  const key = String(a.program?.key || "").toLowerCase();
  if (BODIES.includes(key)) return key;
  const k = String(a.app || key).toLowerCase();
  if (ALIAS.has(k)) return ALIAS.get(k);
  // "pi" only whole: as a prefix it would catch unrelated names.
  return BODIES.find((b) => b !== "pi" && k.startsWith(b)) ?? (k === "pi" ? "pi" : "other");
}
const status = (a) => a.status ?? "idle";
// The same agent keeps the same hat color.
const sprite = (a) => `mods/classroom/sprites/${body(a)}-${pick(ACC, a.address)}-${status(a)}.svg`;

// The name a person gave the tab first, else the session the agent is on, else its program.
function nameOf(a, tabs) {
  const tab = tabs.get(a.tab);
  if (tab?.named && tab.name) return tab.name;
  return session(a) || a.program?.name || a.app || "Agent";
}

export default class Classroom extends View {
  init(_props, cx) {
    // This mod also draws a classroom's right-click menu, as a popup.
    if (props()?.role === "menu") { this.part = new Menu(); this.part.init(cx); return; }
    this.building = "school";
    try {
      const b = localStorage.getItem("building");
      this.building = BUILDING_LIST.some((x) => x.key === b) ? b : OLD_LOOKS[Number(localStorage.getItem("pattern") ?? 0) || 0] ?? "school";
    } catch {}
    this.folded = false;
    try { this.folded = localStorage.getItem("fold") === "1"; } catch {}
    // Day or night by the clock: checked once a minute, redrawn only when it turns.
    this.time = this.timeNow();
    cx.timer.every(60000, (cx) => { const now = this.timeNow(); if (now !== this.time) { this.time = now; cx.notify(); } });
    // The building list under its label: open while the pointer is on either.
    this.picking = false;
    this.overPick = false;
    this.overList = false;
    // The panel's size, and the art size and columns picked for it (see fit).
    this.box = null;
    this.fitIn = null;
    this.fitted = null;
    // The roster shown: only the hovered classroom's is built.
    this.open = null;
    this.overTile = null;
    this.overCard = false;
    // Working students move in steps, about 3 a second, and only while someone
    // works. A native loop would redraw the whole window about 30 times a second.
    this.step = 0;
    this.busy = false;
    cx.timer.every(320, (cx) => { if (this.busy) { this.step ^= 1; cx.notify(); } });
  }

  setBuilding(building) {
    this.building = building;
    try { localStorage.setItem("building", building); } catch {}
  }

  setFolded(folded) {
    this.folded = folded;
    try { localStorage.setItem("fold", folded ? "1" : "0"); } catch {}
  }

  // The plate over the rooms without agents: a press folds them away or shows them.
  // While folded it is outlined if the space you are in is among them.
  foldPlate(empty, p, t) {
    const here = this.folded && empty.some((s) => s.active);
    return h_flex().id("fold").h(17).px(6).gap(4).items_center().cursor_pointer()
      .bg(p.plate).border(1).border_color(here ? t.accent : p.ink)
      .text_size(10.5).font_semibold().text_color(p.ink).hover((st) => st.opacity(0.85))
      .on_click((_e, cx) => { this.setFolded(!this.folded); cx.notify(); })
      .child(svg(`mods/workspace-chrome/chevron-${this.folded ? "right" : "down"}.svg`).size(10).text_color(p.ink))
      .child(`Empty ${empty.length}`);
  }

  // The art's pixel size (k screen pixels on a 2x screen) and the columns for a panel:
  // the largest k from the usual one down to half of it at which the building fits,
  // with the usual columns if they fit, else more (no narrower than a name plate
  // needs), else fewer. If none fits, the smallest k and the lowest building; it scrolls.
  // Heights are counted as render draws them: art pixels from looks.js, and the
  // name plates (17), each floor's padding and the gaps around a room. The panel is
  // measured zoomed and the building is drawn before the zoom, so the panel is
  // divided by it; the usual columns still count the zoomed width, as they always have.
  // Rooms without agents count only by their plate: shown, they run on below and
  // scroll, so opening them never shrinks the art.
  fit(inp, box) {
    const { full, empty, inset, h, z } = inp;
    const Wz = box?.width ?? 268, W = Wz / z, H = (box?.height ?? Infinity) / z - 2;
    const kDef = Math.max(2, Math.round(3.2 * z)), kMin = Math.max(2, Math.ceil(kDef / 2));
    const colsDef = Math.max(1, Math.floor(Wz / 125));
    let best = null;
    for (let k = kDef; k >= kMin; k--) {
      const u = k / (2 * z), side = 8 + inset * u + 7 * u, gap = 5 * u;
      const colsHi = Math.max(colsDef, Math.floor((W - 2 * side + gap) / (MIN_TILE + gap)));
      const order = [colsDef];
      for (let c = colsDef + 1; c <= colsHi; c++) order.push(c);
      for (let c = colsDef - 1; c >= 1; c--) order.push(c);
      for (const cols of order) {
        const tileW = (W - 2 * side - (cols - 1) * gap) / cols;
        const perRow = Math.max(1, Math.floor((tileW - 10 * u) / (23 * u)));
        const floor = (n) => 17 + u * (22 + h.win + 18 * Math.max(1, Math.ceil(n / perRow)) + h.ledge);
        let total = 10 + u * (h.crown + h.base);
        for (let i = 0; i < full.length; i += cols) total += floor(Math.max(...full.slice(i, i + cols)));
        if (empty > 0) total += 17 + u * (6 + h.ledge);
        const f = { k, u, cols, perRow, total };
        if (total <= H) return f;
        if (k === kMin && (!best || total < best.total)) best = f;
      }
    }
    return best;
  }

  // The panel was resized: redraw only if it changes the art size or the columns.
  resized(size, cx) {
    const was = this.box;
    if (was && Math.abs(size.width - was.width) < 1 && Math.abs(size.height - was.height) < 1) return;
    this.box = { width: size.width, height: size.height };
    if (!this.fitIn) return;
    const f = this.fit(this.fitIn, this.box), now = this.fitted;
    if (!now || f.k !== now.k || f.cols !== now.cols || f.perRow !== now.perRow) cx.notify();
  }

  timeNow() {
    const now = Date.now();
    this.sun = sunTimes(now, LAT, LNG);
    return now >= this.sun[0] && now < this.sun[1] ? "day" : "night";
  }

  // When each space last changed. Herdr knows only changes since it started (a tab's
  // changed_at), so the latest seen is kept here and survives a restart; it is
  // written only when a space has changed again.
  remember(sp) {
    if (!this.seen) {
      this.seen = {};
      try { this.seen = JSON.parse(localStorage.getItem("changed") ?? "{}") || {}; } catch {}
    }
    let moved = false;
    for (const s of sp) {
      const at = Math.max(0, ...s.tabs.map((tb) => tb.changed_at ?? 0));
      if (at > (this.seen[s.id] ?? 0)) { this.seen[s.id] = at; moved = true; }
    }
    if (moved) {
      const live = new Set(sp.map((s) => s.id));
      for (const id of Object.keys(this.seen)) if (!live.has(id)) delete this.seen[id];
      try { localStorage.setItem("changed", JSON.stringify(this.seen)); } catch {}
    }
    return (s) => this.seen[s.id] ?? 0;
  }

  closePickSoon(cx) {
    cx.timer.after(300, (cx) => {
      if (this.picking && !this.overPick && !this.overList) { this.picking = false; cx.notify(); }
    });
  }

  // Day/Night follows the clock; the building opens a list under it.
  controls(t) {
    const label = (id) => h_flex().id(id).h(20).px(6).gap(5).items_center().rounded(5).cursor_pointer()
      .text_size(11).text_color(t.muted).hover((st) => st.bg(t.hover).text_color(t.foreground));
    const time = h_flex().id("time").h(20).px(6).gap(5).items_center().text_size(11).text_color(t.dim)
      .tooltip(`Sunrise ${clock(this.sun[0])} · Sunset ${clock(this.sun[1])}`)
      .child(svg(`mods/classroom/icons/time-${this.time}.svg`).size(11)).child(this.time === "night" ? "Night" : "Day");
    const name = BUILDING_LIST.find((b) => b.key === this.building)?.name ?? "";
    const trigger = label("building").when(this.picking, (el) => el.bg(t.selected).text_color(t.foreground))
      .on_hover((h, cx) => { this.overPick = h; if (!h) this.closePickSoon(cx); })
      .on_click((_e, cx) => { this.picking = !this.picking; cx.notify(); })
      .child(name).child(svg("mods/workspace-chrome/chevron-down.svg").size(11));
    const list = v_flex().id("building-list").w(150).p(4).gap(1).bg(t.popover).rounded(8).border(1).border_color(t.border)
      .on_hover((h, cx) => { this.overList = h; if (!h) this.closePickSoon(cx); })
      .children(BUILDING_LIST.map((b) => h_flex().id(`building-${b.key}`).h(26).px(8).gap(6).items_center().rounded(5).cursor_pointer()
        .text_size(12).text_color(t.foreground).hover((st) => st.bg(t.hover))
        .on_click((_e, cx) => { this.setBuilding(b.key); this.picking = false; cx.notify(); })
        .child(div().flex_1().child(b.name))
        .when(b.key === this.building, (el) => el.child(svg("mods/workspace-chrome/check.svg").size(12).text_color(t.accent)))));
    return h_flex().gap(2).items_center()
      .child(time)
      .child(Popup.new("building-pop", trigger).anchor("top_right").when(this.picking, (el) => el.content(list)));
  }

  // A short rest opens a roster; leaving both window and roster closes it, after a
  // moment so the pointer can cross from one to the other.
  enter(id, cx) {
    this.overTile = id;
    if (this.quiet === id) return;
    cx.timer.after(220, (cx) => { if (this.overTile === id && this.open !== id && this.quiet !== id) { this.open = id; cx.notify(); } });
  }
  leave(id, cx) {
    if (this.overTile === id) this.overTile = null;
    if (this.quiet === id) this.quiet = null;
    this.closeSoon(cx);
  }
  closeSoon(cx) {
    cx.timer.after(260, (cx) => {
      if (this.open && !this.overCard && this.overTile !== this.open) { this.open = null; cx.notify(); }
    });
  }

  // The right-click menu: what it offers is looked up first, as its height depends on it.
  // No roster over the menu: none opens on this classroom until the pointer leaves it.
  openMenu(s, cx) {
    this.open = null;
    this.quiet = s.id;
    cx.notify();
    cx.spawn(async () => {
      const info = await probe(s);
      openOverlay({ mod: "classroom", kind: "popup", width: MENU_WIDTH, height: menuHeight(menuItems(s, info)), props: { role: "menu", space: s.id, info } });
    });
  }

  // A shoulder badge: warning if anyone waits for you, else a check if anyone finished.
  badge(list, t) {
    const waits = list.some((a) => a.status === "blocked");
    const done = list.some((a) => a.status === "done");
    if (!waits && !done) return null;
    return h_flex().absolute().top(-9).right(-9).size(20).rounded(10).items_center().justify_center()
      .bg(waits ? t.blocked : t.done).border(2).border_color(t.chrome)
      .child(svg(`mods/classroom/icons/${waits ? "warn" : "check"}.svg`).size(12).text_color("#ffffff"));
  }

  // A student sitting at a desk: the desk hides its legs, its arms rest on it.
  // A working one hops between two spots on each step of the timer (see init).
  seat(a, p, c, dim) {
    const { u } = this;
    const kid = image(sprite(a, p)).w(19 * u).h(15 * u).when(dim, (el) => el.opacity(0.8));
    const hop = status(a) === "working" ? (this.step ? 1 : -1) : 0;
    return div().relative().w(22 * u).h(17 * u).flex_none()
      .child(div().absolute().top(hop > 0 ? -2 * u : 0).left(1.5 * u + hop * u).child(kid))
      .child(div().absolute().top(11 * u).left(2.5 * u).w(17 * u).h(2 * u).bg(p.deskTop))
      .child(div().absolute().top(13 * u).left(3.5 * u).w(15 * u).h(2 * u).bg(p.desk))
      .child(div().absolute().top(15 * u).left(4 * u).w(u).h(2 * u).bg(p.leg))
      .child(div().absolute().top(15 * u).left(17 * u).w(u).h(2 * u).bg(p.leg))
      .when(Boolean(p.win.lights), (el) => el
        .child(div().absolute().top(13.5 * u).left(7 * u).size(u).bg(p.lights[0]))
        .child(div().absolute().top(13.5 * u).left(10 * u).size(u).bg(p.lights[1])));
  }

  // A room: its name plate over a window dressed by the building (looks.js), its
  // students at their desks inside.
  tile(s, list, tabs, p, t, roomH) {
    const { u } = this, w = p.win;
    const lit = !p.off || list.some((a) => status(a) !== "idle");
    const c = lit ? p : { ...p, ...p.off };
    const plate = h_flex().justify_center()
      .child(div().max_w_full().px(6).h(17).flex().items_center().bg(p.plate).border(1).border_color(p.ink)
        .text_size(10.5).font_semibold().text_color(p.ink).truncate().child(s.name || "—"));
    const room = h_flex().relative().w_full().h(roomH).bg(c.glass)
      .when(Boolean(w.round), (el) => el.rounded((w.round - 1.5) * u).overflow_hidden())
      .when(Boolean(w.prop), (el) => el.child(backdrop(w.prop, c, u)))
      .child(h_flex().w_full().h_full().flex_wrap().content_end().justify_center().items_end().gap(u).px(4 * u).pb(u)
        .when(list.length === 0, (el) => el.child(h_flex().gap(4 * u).pb(u)
          .child(div().w(17 * u).h(2 * u).bg(p.deskTop).opacity(0.7)).child(div().w(17 * u).h(2 * u).bg(p.deskTop).opacity(0.7))))
        .children(list.map((a) => this.seat(a, p, c, !lit))))
      .children(windowSides(w.side, c, u));
    const on = s.active || this.open === s.id;
    const head = windowTop(w.top, c, u);
    const frame = v_flex().relative().w_full().gap(u).p(1.5 * u).bg(on ? t.accent : p.frame)
      .when(Boolean(w.round), (el) => el.rounded(w.round * u))
      .when(Boolean(head), (el) => el.child(head))
      .child(room)
      .when(Boolean(w.rivets), (el) => el.children(rivets(p, u)));
    const b = this.badge(list, t);
    const under = windowUnder(w.under, c, u, hash(s.id) % 3 === 0);
    const trigger = v_flex().id(`room-${s.id}`).relative().w_full().gap(2 * u).cursor_pointer()
      .on_hover((h, cx) => (h ? this.enter(s.id, cx) : this.leave(s.id, cx)))
      .on_click(() => run("space.select", { id: s.id }))
      .on_mouse_down("right", (_e, cx) => this.openMenu(s, cx))
      .child(plate)
      .child(v_flex().w_full().child(b ? frame.child(b) : frame).when(Boolean(under), (el) => el.child(under)));
    return Popup.new(`pop-${s.id}`, trigger).anchor("top_left")
      .when(this.open === s.id, (el) => el.content(this.roster(s, list, tabs, p, t)));
  }

  roster(s, list, tabs, p, t) {
    const head = h_flex().gap(6).items_center().pb(6).border_b(1).border_color(t.border)
      .child(div().flex_1().min_w(0).truncate().text_size(12.5).font_semibold().text_color(t.foreground).child(s.name || "—"))
      .when(Boolean(s.branch), (el) => el.child(div().max_w(120).truncate().text_size(11).text_color(t.dim).child(s.branch)));
    const row = (a) => h_flex().id(`st-${a.address}`).py(4).px(6).gap(8).items_center().rounded(6).cursor_pointer()
      .hover((st) => st.bg(t.hover))
      .on_click(() => run("pane.focus", { pane: a.pane }))
      .child(image(sprite(a, p)).w(19 * this.uDef).h(15 * this.uDef).flex_none())
      .child(div().flex_1().min_w(0).truncate().text_size(12).text_color(t.foreground).child(nameOf(a, tabs)))
      .child(div().flex_none().text_size(10.5).font_semibold().text_color(t[status(a)] ?? t.dim).child(LABEL[status(a)]));
    return v_flex().id(`roster-${s.id}`).w(280).p(8).gap(2).bg(t.popover).rounded(10).border(1).border_color(t.border)
      .on_hover((h, cx) => { this.overCard = h; if (!h) this.closeSoon(cx); })
      .child(head)
      .when(list.length === 0, (el) => el.child(div().py(6).text_size(11.5).text_color(t.dim).child("No agents")))
      .children(list.map(row));
  }

  render(cx) {
    if (this.part) return this.part.render(cx);
    const t = theme(), p = look(this.building, this.time), house = BUILDINGS[p.kind];
    // One pixel of the art is a whole number of screen pixels (4 on a 2x screen at the
    // usual size), so it stays crisp. The roster keeps the usual size.
    const z = settings()?.zoom ?? 1;
    this.uDef = Math.max(2, Math.round(3.2 * z)) / (z * 2);
    // One read of each per render: these copy every space and agent.
    const sp = spaces(), ag = agents();
    const tabs = new Map(sp.flatMap((s) => s.tabs.map((tb) => [tb.id, tb])));
    const by = new Map(sp.map((s) => [s.id, []]));
    for (const a of ag) by.get(a.space)?.push(a);
    for (const list of by.values()) list.sort((x, y) => (ORDER[status(x)] ?? 9) - (ORDER[status(y)] ?? 9) || (y.seq ?? 0) - (x.seq ?? 0));
    // Rooms with agents first, then empty ones; within each, the most recently
    // changed first, then the agents' order of change, then the spaces' order.
    const filled = (s) => (by.get(s.id).length > 0 ? 1 : 0);
    const changed = this.remember(sp);
    const recent = (s) => Math.max(0, ...by.get(s.id).map((a) => a.seq ?? 0));
    const rooms = [...sp].sort((x, y) => filled(y) - filled(x) || changed(y) - changed(x) || recent(y) - recent(x) || x.index - y.index);
    const count = { blocked: 0, done: 0, working: 0, idle: 0 };
    for (const a of ag) count[status(a)] += 1;
    this.busy = count.working > 0;

    // A floor per row of windows (about one per 125 pixels of width, see fit); the
    // windows of a floor share the height of its fullest classroom.
    const full = rooms.filter((s) => filled(s));
    const empty = rooms.slice(full.length);
    this.fitIn = { full: full.map((s) => by.get(s.id).length), empty: empty.length, inset: house.inset, h: rise(p), z };
    this.fitted = this.fit(this.fitIn, this.box);
    const { cols, perRow } = this.fitted;
    this.u = this.fitted.u;
    const { u } = this;
    const ins = house.inset * u, gap = 5 * u;
    const height = (n) => { const r = Math.max(1, Math.ceil(n / perRow)); return 8 * u + r * 17 * u + (r - 1) * u + u; };
    const floorsOf = (list) => { const out = []; for (let i = 0; i < list.length; i += cols) out.push(list.slice(i, i + cols)); return out; };
    const storey = (id, inner) => v_flex().id(id).w_full()
      .child(h_flex().w_full().px(ins).child(v_flex().flex_1().min_w(0).bg(p.wall).border_l(2 * u).border_r(2 * u).border_color(p.edge).child(inner)))
      .child(house.ledge(p, u, ins));
    const floor = (id, r) => {
      const roomH = Math.max(...r.map((s) => height(by.get(s.id).length)));
      return storey(id, h_flex().w_full().px(5 * u).pt(5 * u).pb(4 * u).gap(gap).items_start().children([
        ...r.map((s) => div().flex_1().min_w(0).child(this.tile(s, by.get(s.id), tabs, p, t, roomH))),
        ...Array.from({ length: cols - r.length }, () => div().flex_1().min_w(0)),
      ]));
    };
    const wall = v_flex().w_full()
      .children(floorsOf(full).map((r, i) => floor(`floor-${i}`, r)))
      .when(empty.length > 0, (el) => el.child(storey("fold-floor", h_flex().w_full().justify_center().py(3 * u).child(this.foldPlate(empty, p, t)))))
      .when(empty.length > 0 && !this.folded, (el) => el.children(floorsOf(empty).map((r, i) => floor(`empty-${i}`, r))));

    // The counts, then the controls; they go under the counts when the sidebar is narrow.
    const header = h_flex().flex_wrap().justify_between().px(12).pt(8).pb(6).gap_x(12).gap_y(4).items_center()
      .child(h_flex().h(20).gap(10).text_size(10.5).text_color(t.dim)
        .children(["blocked", "done", "working", "idle"].map((k) =>
          h_flex().gap(4).items_center().child(div().size(6).rounded(3).bg(t[k] ?? t.dim)).child(`${LABEL[k]} ${count[k]}`))))
      .child(this.controls(t));

    return v_flex().id("root").size_full().min_h(0).min_w(0)
      .child(header)
      .child(v_flex().id("school").flex_1().min_h(0).overflow_y_scrollbar()
        .on_size_change((size, cx) => this.resized(size, cx))
        .child(v_flex().w_full().px(8).pb(10).child(house.crown(p, u, ins)).child(wall).child(house.base(p, u, ins))));
  }
}
