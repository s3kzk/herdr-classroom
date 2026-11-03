# Rooms

Your spaces are rooms in a pixel-art building, and every agent is an occupant sitting at a desk, dressed for what it is doing: a hard hat while it works, a raised hand or a big "!" when it needs you, confetti when it is done, a nightcap while it sleeps. Each agent kind has its own occupant, drawn after the icon Herdr ships for it. The building follows the time of day and is one of six: a school, an apartment, a hotel, a submarine, a rocket or a castle.

![Rooms](preview.png)

## What you see

- **Left sidebar, 268px:** the brand row (46px, shipped `workspace-chrome`), then the building and the agent list sharing the rest half and half, then the footer (69px, `workspace-chrome` with `{footer: true}`).
- **The building (`rooms` mod):**
  - A header row: counts per status (`Needs you`, `Done`, `Working`, `Idle`), `Day`/`Night`, and the building's name (a press lists the six buildings).
  - Under it the building art: a roof line and a clock tower or the building's own top, then floors of windows. One window is one space, with its name on a white plate above it.
  - Rooms with agents come first, the most recently changed first. Rooms without agents sit under a plate `› Empty N` that folds them away or shows them (`⌄ Empty N`).
  - Each room shows one desk per agent with its occupant behind it. Desks hide the occupants below row 11 of their 19×15 sprite.
  - A window's top-right corner carries a red `!` badge when someone in it waits for you, or a blue check when someone finished.
  - Night (between sunset and sunrise, reckoned for the local time zone) darkens the sky; a room whose occupants all sleep turns its lights off.
- **Right of it:** the shipped `pane` mod with the tabs bar above (`tabs-graph`, 42px, a copy of the shipped `tabs` with a Graph button) and the status bar below (`workspace-status`, 28px).
- **Right panel, 368px:** a stack of the shipped `files` and `changes` mods and `git-graph` (see Watch out).

## How it behaves

- **working:** yellow-or-other hard hat with a wrench and a sweat drop; the occupant hops between two spots about 3 times a second.
- **blocked:** eyes look up and a red `!` appears (Claw'd occupants also raise a hand); the room gets the red badge.
- **done:** `^ ^` eyes, blush, confetti; the room gets the blue check.
- **idle:** closed eyes, a starry nightcap, `Z` and a snot bubble.
- The same agent always wears the same hat color (4 colors, picked from its address).
- Hovering a window for 220ms opens a roster card: each occupant with its name and status. A click on a row focuses that agent's pane; a click on the window selects the space. Right-click opens a menu (open the folder, in VS Code, copy the path, open the repository with `gh browse`).
- The building scales its art in whole screen pixels (4, 3 or 2 per art pixel on a 2x screen) and its number of columns so that the rooms with agents fit the panel; empty rooms opened under the plate scroll instead of shrinking it.

## Built from

- `layouts/rooms.json`: the node tree above. It sets `terminal_opacity: 1` and `titlebar: "none"`.
- `mods/rooms/`:
  - `main.js` (the view, the fit, the roster), `looks.js` (six buildings' palettes and window dressing), `art.js` (sizes of the SVGs in `icons/`), `sun.js` (sunrise and sunset), `session.js` (an agent's session name from its terminal title), `menu.js` (the right-click popup).
  - `sprites/<body>-<hat>-<status>.svg`: 15 bodies × 4 hat colors × 4 statuses = 240 pictures. Bodies are `claude` and `other` (Claw'd, recolored) and `codex`, `crush`, `kiro`, `pi`, `gemini`, `cursor`, `opencode`, `amp`, `grok`, `antigravity`, `kimi`, `qoder`, `hermes`.
  - An occupant's body comes from `program.key` of the agent (the program table folds names like `kiro-cli` into `kiro`), else from the agent's reported `app`.
  - `tools/`: the Python scripts that draw every SVG (`occupants.py`, `scene.py`, `buildings.py`; see `tools/README.md`).
- `herdr` functions: `spaces()`, `agents()`, `theme()`, `settings()`, `props()`, `run("space.select" | "pane.focus")`, `openOverlay`, `exec` (menu only).
- Programs it runs, from the right-click menu only: `git rev-parse`, `gh browse`, `open`, `open -a "Visual Studio Code"`, `pbcopy`.

## Watch out

- The right panel uses `git-graph`, which is not in this repo: add it from github.com/rabeeh-ta/herdr-git-graph, or drop the `graph` block from the layout.
- The right-click menu is macOS-only (`open`, `pbcopy`, VS Code by app name).
- Every picture is static; the only motion is the working hop on a 320ms timer that runs only while someone works. Don't add native loops or per-frame animation.
- Sprites are 19×15 with the face in rows 4–10: the desk hides rows 11 and below in the room, but the roster card shows the whole sprite.
- GitHub Copilot agents show as the gray Claw'd (`other`) on purpose: GitHub asks for approval before its mascot is used in public.

## Done when

- `herdr-app check mods/rooms` and `herdr-app check mods/tabs-graph` pass, and `layout.switch {name: "rooms"}` shows the building with no errors in `herdr-app status`.
- With agents running, each sits in its space's room, dressed for its status, and the counts in the header match the agent list.
- Resizing the panel changes the art size or the columns without errors; opening `Empty N` lets the panel scroll.
- `python3 -I tools/occupants.py sprites` regenerates `sprites/` byte for byte.
