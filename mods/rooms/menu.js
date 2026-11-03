// A room's right-click menu, opened as a popup overlay of this mod
// (props { role: "menu", space }). ↑/↓ move, Enter runs, Esc closes.
// An item is { label, icon, run, line? }; `line` draws a separator above it.
import { div, svg } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { props, closeOverlay, openOverlay, run, theme, spaces, panes, agents, exec, knownAgents } from "herdr";

const ICON = (name) => `mods/workspace-chrome/${name}.svg`;

// Where a space is now: its first terminal's live folder, else where it was made.
function place(s) {
  const tabs = new Set((s.tabs ?? []).map((c) => c.id));
  return panes().find((p) => tabs.has(p.tab) && p.cwd)?.cwd || s.folder;
}

export const MENU_WIDTH = 240;
// The popup's height for a list: rows, separators and padding.
export const menuHeight = (list) => list.length * 31 + list.filter((it) => it.line).length * 9 + 10;

// What the menu offers for a space, given what is known when it opens.
export function menuItems(s, { folder, git, agent }) {
  const mine = agents().filter((a) => a.space === s.id);
  const first = (st) => mine.filter((a) => a.status === st).sort((x, y) => (y.seq ?? 0) - (x.seq ?? 0))[0];
  const waiting = first("blocked"), done = first("done");
  const list = [
    { label: "Go to space", icon: "chevron-right", run: () => run("space.select", { id: s.id }) },
    ...(waiting ? [{ label: "Go to agent that needs you", icon: "circle-check", run: () => run("pane.focus", { pane: waiting.pane }) }] : []),
    ...(done ? [{ label: "Go to finished agent", icon: "check", run: () => run("pane.focus", { pane: done.pane }) }] : []),
    { label: agent ? `New tab with ${agent.name}` : "New agent tab", icon: "plus", line: true,
      run: () => run("tab.new", { space: s.id, ...(folder ? { folder } : {}), ...(agent ? { argv: agent.run } : {}) }) },
    { label: "New terminal tab", icon: "terminal", run: () => run("tab.new", { space: s.id, ...(folder ? { folder } : {}) }) },
    ...(git ? [{ label: "New worktree", icon: "git-branch", run: () => openOverlay({ mod: "worktree", kind: "dialog", width: 440, height: 260, props: { space: s.id, action: "new" } }) }] : []),
  ];
  if (folder && !s.machine) {
    list.push(
      { label: "Open in Finder", icon: "folder", line: true, run: () => exec("open", [folder]).catch(() => null) },
      { label: "Open in VS Code", icon: "file-text", run: () => exec("open", ["-a", "Visual Studio Code", folder]).catch(() => null) },
      ...(git ? [{ label: "Open on GitHub", icon: "git-compare", run: () => exec("gh", ["browse"], { cwd: folder }).catch(() => null) }] : []),
      { label: "Copy path", icon: "files", run: () => exec("sh", ["-c", 'printf %s "$1" | pbcopy', "sh", folder]).catch(() => null) },
    );
  }
  list.push(
    { label: "Rename", icon: "square-pen", line: true, run: () => run("space.rename", { id: s.id }) },
    // space.close asks the person first.
    { label: "Close", icon: "x", run: () => run("space.close", { id: s.id }) },
  );
  return list;
}

// What the menu needs to know before it opens (its height depends on it): the
// space's folder, whether it is a git checkout, and the agent picked most.
export async function probe(s) {
  const folder = place(s), on = s.machine ? { on: s.machine } : {};
  const [top, list] = await Promise.all([
    folder ? exec("git", ["rev-parse", "--show-toplevel"], { cwd: folder, ...on }).catch(() => null) : null,
    knownAgents(on).catch(() => []),
  ]);
  const a = list.find((x) => x.installed);
  return { folder, git: top?.code === 0, agent: a ? { name: a.name, run: a.run } : null };
}

export class Menu {
  init(cx) {
    this.at = 0;
    this.handle = cx.focus_handle();
    this.handle.focus();
  }

  items() {
    const p = props() ?? {}, s = spaces().find((x) => x.id === p.space);
    return s ? menuItems(s, p.info ?? {}) : [];
  }

  choose(i) {
    const it = this.items()[i];
    if (!it) return;
    closeOverlay(props()?.overlay);
    it.run();
  }

  render() {
    const t = theme(), list = this.items();
    return v_flex().id("rooms-menu").track_focus(this.handle).w_full().min_h(0).p(5).bg(t.popover).text_size(12.8)
      .on_key_down((e, cx) => {
        if (!list.length) return;
        if (e.key === "down") this.at = (this.at + 1) % list.length;
        else if (e.key === "up") this.at = (this.at + list.length - 1) % list.length;
        else if (e.key === "enter") this.choose(this.at);
        else if (e.key === "escape") closeOverlay(props().overlay);
        else return;
        cx.notify();
      })
      .children(list.map((it, i) => v_flex()
        .when(Boolean(it.line), (el) => el.child(div().mx(7).my(4).h(1).bg(t.border)))
        .child(h_flex().id(`cm-${i}`).h(31).px(8).gap(9).rounded(7).items_center().cursor_pointer()
          .text_color(it.icon === "x" ? t.blocked : t.foreground)
          .when(i === this.at, (el) => el.bg(t.selected)).hover((st) => st.bg(t.hover))
          .on_click(() => this.choose(i))
          .child(svg(ICON(it.icon)).size(14).flex_none().text_color(it.icon === "x" ? t.blocked : t.muted))
          .child(div().flex_1().truncate().child(it.label)))));
  }
}
