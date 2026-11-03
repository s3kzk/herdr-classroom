# 部屋にいる住人（19x15 マスのドット絵）を、体 × 小物の色 4 つ × 状態 4 つで生成する。
#   python3 -I tools/occupants.py sprites
# claude と other（表に無いエージェントと Copilot）は Claude Code の起動画面の Claw'd（端末の ▐▛███▜▌ /
# ▝▜█████▛▘ / ▘▘ ▝▝ を 1x2 の画素に展開した 16x10）を色違いにしたもの。ほかの 13 体は Herdr 同梱の
# アイコン（~/.config/herdr-app/icons）の形と色を手本に起こした。1 色だけのアイコンの配色は自分で決めた。
# 部屋では机が 11 行目から下を隠す。顔は 4〜10 行目に、状態の小物は 0〜4 行目に置く。
# 名簿のポップアップは机なしで全体を出すので、隠れる行も描く。
import sys, os
out = sys.argv[1]
OX, OY, W, H = 1, 5, 19, 15

# ---- Claw'd: 腕で挙手・万歳する ----
def base():
    g = {}
    for r in (0, 1, 2, 3, 6, 7):
        for c in range(2, 14): g[(r, c)] = "B"
    for r in (4, 5):
        for c in range(0, 16): g[(r, c)] = "B"
    for r in (8, 9):
        for c in (3, 5, 10, 12): g[(r, c)] = "B"
    for r in (2, 3): g[(r, 4)] = g[(r, 11)] = "K"
    return g
def helmet(g):
    for c in range(1, 15): g[(-1, c)] = "H"
    for c in range(3, 13): g[(-2, c)] = "H"
    for c in range(5, 11): g[(-3, c)] = "H"
    g[(-2, 7)] = g[(-2, 8)] = "O"
    for r in range(0, 5): g[(r, 16)] = "G"
    g[(-1, 15)] = g[(-2, 15)] = g[(-1, 17)] = g[(-2, 17)] = "G"
    g[(1, 0)] = g[(2, 0)] = "S"
def confetti(g):
    for (r, c), v in {(-5, 3): "R", (-4, 6): "N", (-5, 9): "Y", (-3, 11): "R", (-4, 13): "C",
                      (-5, 16): "N", (-3, 4): "Y", (-5, -1): "C", (-2, 8): "N", (-4, 17): "Y"}.items():
        g[(r, c)] = v
def hat(g, dz=0):
    for c in range(1, 15): g[(-1, c)] = "V"
    for c in range(4, 12): g[(-2, c)] = "V"
    for c in range(5, 11): g[(-3, c)] = "V"
    for c in range(7, 11): g[(-4, c)] = "V"
    g[(-5, 10)] = g[(-5, 11)] = "V"; g[(-4, 12)] = "W"
    for p in ((-1, 3), (-2, 6), (-1, 9), (-3, 9), (-2, 10), (-1, 13)): g[p] = "W"
    for p in ((-4, 14), (-4, 15), (-4, 16), (-3, 15), (-2, 14), (-2, 15), (-2, 16)): g[p] = "Z"   # Z
    for p in ((1, 15), (2, 14), (2, 16), (3, 15)): g[(p[0], p[1] + dz)] = "S"                    # 鼻ちょうちん
    g[(2, 15 + dz)] = "L"
def working():  # 工事中: ヘルメットとスパナ、汗
    g = base(); helmet(g); return g
def blocked():  # 「はい！」: 右手を挙げて目は上を見る
    g = base()
    for r in (4, 5): g.pop((r, 14)); g.pop((r, 15))
    for r in range(-3, 6): g[(r, 14)] = "B"
    g[(-3, 15)] = "B"
    for r in (2, 3): g[(r, 4)] = g[(r, 11)] = "B"
    for r in (1, 2): g[(r, 4)] = g[(r, 11)] = "K"
    for r in (-5, -4, -3, -1): g[(r, 17)] = "R"                                                   # !
    return g
def done():  # 万歳と紙吹雪、^ ^ の目と照れ
    g = base()
    for r in (4, 5):
        for c in (0, 1, 14, 15): g.pop((r, c))
    for r in range(-2, 6): g[(r, 1)] = g[(r, 14)] = "B"
    g[(-2, 0)] = g[(-2, 15)] = "B"
    for r in (2, 3): g[(r, 4)] = g[(r, 11)] = "B"
    g[(3, 3)] = g[(2, 4)] = g[(3, 5)] = "K"
    g[(3, 10)] = g[(2, 11)] = g[(3, 12)] = "K"
    g[(4, 3)] = g[(4, 12)] = "P"
    confetti(g); return g
def idle():  # おやすみ: 星柄のとんがり帽子（夢の中で魔法使い）と閉じた目
    g = base()
    for r in (2, 3): g[(r, 4)] = g[(r, 11)] = "B"
    g[(3, 3)] = g[(3, 4)] = g[(3, 11)] = g[(3, 12)] = "K"
    hat(g); return g
CLAWD = {"working": working, "blocked": blocked, "done": done, "idle": idle}

# ---- 同梱アイコンを手本にした体: 腕が無いので、状態は目と小物だけで描き分ける ----
# 体は絵の座標（列 0〜18・行 top〜14。top の既定は 5）で書き、"." は空き。4 行目から始まる体は、ヘルメットと帽子のつばがてっぺんに重なる。顔（目）は状態ごとに描き足す。
CAST = {
    # 上から下へ薄紫から青に変わる雲。顔は「>_」。
    "codex": dict(top=4, rows=[
        "......TTT..TTTT....",
        "....TTTTTTTTTTTT...",
        "..TTTTTTTTTTTTTTT..",
        "..MMMMMMMMMMMMMM...",
        ".MMMMMMMMMMMMMMMM..",
        ".NNNNNNNNNNNNNNNN..",
        "..NNNNNNNNNNNNNN...",
        "..XXXXXXXXXXXXXXX..",
        "...XXXXXXXXXXXXX...",
        "....XXXX..XXXXX...."],
        eyes=None, ink="E", blush=((10, 3), (10, 11)),
        col={"T": "#B1A7FF", "M": "#93A0FF", "N": "#6E80FF", "X": "#3941FF", "E": "#FFFFFF"}),
    # 顔の付いたピンクのドット絵のハート。
    "crush": dict(rows=[
        "...PPPP....PPPP....",
        "..PPPPPP..PPPPPP...",
        "..PPPPPPPPPPPPPP...",
        "..PPPPPPPPPPPPPP...",
        "..PPPPPPPPPPPPPP...",
        "..PPRPPPKKPPPRPP...",
        "...PPPPPPPPPPPP....",
        "....PPPPPPPPPP.....",
        "......PPPPPP.......",
        "........PP........."],
        eyes=((8, 6), (8, 11)), ink="K", skin="P", blush=None,
        col={"P": "#FF6DAA", "K": "#111111", "R": "#FF13A9"}),
    # 白い幽霊。目は右寄り。昼の明るい窓に埋もれないよう、同梱の絵の地の紫で縁取った。
    "kiro": dict(rows=[
        ".....OOOOOOOO......",
        "....OWWWWWWWWO.....",
        "...OWWWWWWWWWWO....",
        "...OWWWWWWWWWWO....",
        "...OWWWWWWWWWWO....",
        "..OWWWWWWWWWWWO....",
        ".OWWWWWWWWWWWWO....",
        ".OWWWWWWWWWWWWO....",
        "..OWWOWWWOWWWO.....",
        "...OO.OOO.OOO......"],
        eyes=((8, 9), (8, 12)), ink="K", skin="W", blush=((10, 8), (10, 13)),
        col={"W": "#FFFFFF", "O": "#9046FF", "K": "#111111"}),
    # 4 つの角の星。色は内蔵の表のタイル色。
    "gemini": dict(top=4, rows=[
        "........BB.........",
        ".......BBBB........",
        "......BBBBBB.......",
        ".....BBBBBBBB......",
        ".BBBBBBBBBBBBBBBB..",
        "....BBBBBBBBBB.....",
        "......BBBBBB.......",
        ".......BBBB........",
        "........BB.........",
        "........BB.........",
        "..................."],
        eyes=((7, 7), (7, 10)), ink="K", blush=((9, 5), (9, 12)),
        col={"B": "#8E75B2", "K": "#1C1D21"}),
    # 3 面に陰を付けた六角形の箱。同梱の絵は 1 色なので、灰色の濃淡は自分で決めた。
    "cursor": dict(top=4, rows=[
        "........TT.........",
        "......TTTTTT.......",
        "....TTTTTTTTTT.....",
        "..TTTTTTTTTTTTTT...",
        "..LLTTTTTTTTTTDD...",
        "..LLLLTTTTTTDDDD...",
        "..LLLLLLTTDDDDDD...",
        "..LLLLLLLDDDDDDD...",
        "...LLLLLLDDDDDD....",
        ".....LLLLDDDD......",
        ".......LLDD........"],
        eyes=((7, 6), (7, 11)), ink="K", blush=((9, 6), (9, 11)),
        col={"T": "#E6E6E6", "L": "#9B9B9B", "D": "#3A3A3A", "K": "#1C1D21"}),
    # 太い枠の四角。枠の内側が暗い画面で、目はそこに出る。
    "opencode": dict(top=4, rows=[
        "...OOOOOOOOOOOO....",
        "...OWWWWWWWWWWO....",
        "...OWWWWWWWWWWO....",
        "...OWWDDDDDDWWO....",
        "...OWWDDDDDDWWO....",
        "...OWWDDDDDDWWO....",
        "...OWWDDDDDDWWO....",
        "...OWWDDDDDDWWO....",
        "...OWWWWWWWWWWO....",
        "...OWWWWWWWWWWO....",
        "...OOOOOOOOOOOO...."],
        eyes=((8, 7), (8, 10)), ink="W", blush=((10, 6), (10, 11)),
        col={"O": "#1C1D21", "W": "#FFFFFF", "D": "#1C1D21"}),
    # 4x4 のドットで描いた π をそのまま 3 倍にした形。穴が口になる。
    "pi": dict(top=4, rows=[
        "..OOOOOOOOOOO......",
        "..OSSSSSSSSSO......",
        "..OSSSSSSSSSO......",
        "..OSSSSSSSSSO......",
        "..OSSSDDDSSSO......",
        "..OSSSDDDSSSO......",
        "..OSSSDDDSSSOOOO...",
        "..OSSSSSSOOOSSSO...",
        "..OSSSSSSO.OSSSO...",
        "..OSSSSSSO.OSSSO...",
        "..OSSSOOOO.OSSSO..."],
        eyes=((6, 5), (6, 9)), ink="O", blush=((8, 4), (8, 10)),
        col={"O": "#1C1D21", "S": "#FFFFFF", "D": "#1C1D21"}),
    # 赤い角丸の体に、同梱の絵の斜めの 3 本線。
    "amp": dict(top=4, rows=[
        "....RRRRRRRRRR.....",
        "...RRRRWRRWRRWR....",
        "..RRRRWRRWRRWRRR...",
        "..RRRWRRWRRWRRRR...",
        "..RRRRRRRRRRRRRR...",
        "..RRRRRRRRRRRRRR...",
        "..RRRRRRRRRRRRRR...",
        "..RRRRRRRRRRRRRR...",
        "..RRRRRRRRRRRRRR...",
        "...RRRRRRRRRRRR....",
        "....RRRRRRRRRR....."],
        eyes=((8, 6), (8, 11)), ink="K", blush=((10, 4), (10, 13)),
        col={"R": "#F34E3F", "W": "#FFFFFF", "K": "#1C1D21"}),
    # 輪と斜めの線。白い玉に暗い輪で描いた（同梱の絵は 1 色）。
    "grok": dict(top=4, rows=[
        ".....OOOOOOOO......",
        "...OOWWWWWWWOOO....",
        "..OWWWWWWWWWOWWO...",
        "..OWWWWWWWWOWWWO...",
        ".OWWWWWWWWOWWWWWO..",
        ".OWWWWWWWOWWWWWWO..",
        ".OWWWWWWOWWWWWWWO..",
        "..OWWWWOWWWWWWWO...",
        "..OWWWOWWWWWWWWO...",
        "...OOOWWWWWWWOO....",
        ".....OOOOOOOO......"],
        eyes=((7, 6), (7, 12)), ink="O", blush=((9, 5), (9, 13)),
        col={"O": "#1C1D21", "W": "#FFFFFF"}),
    # 虹色のアーチ。色は同梱の絵の赤・黄・緑・青。
    "antigravity": dict(top=4, rows=[
        "......YYYYYY.......",
        "....GGRRRRRRBB.....",
        "...GGGRRRRRRBBB....",
        "...GGGRRRRRRBBB....",
        "..GGGGRRRRRRBBBB...",
        "..GGGG......BBBB...",
        "..GGGG......BBBB...",
        "..GGG........BBB...",
        "..GGG........BBB...",
        "..GG..........BB...",
        "..GG..........BB..."],
        eyes=((6, 7), (6, 10)), ink="K", blush=None,
        col={"Y": "#FFE432", "R": "#FC413D", "G": "#00B95C", "B": "#3186FF", "K": "#1C1D21"}),
    # 青い角丸の体に、白い K。色は同梱の絵の青と白。
    "kimi": dict(top=4, rows=[
        "....BBBBBBBBBB.....",
        "...BBBBBWBWBBBB....",
        "..BBBBBBWWBBBBBB...",
        "..BBBBBBWBWBBBBB...",
        "..BBBBBBBBBBBBBB...",
        "..BBBBBBBBBBBBBB...",
        "..BBBBBBBBBBBBBB...",
        "..BBBBBBBBBBBBBB...",
        "..BBBBBBBBBBBBBB...",
        "...BBBBBBBBBBBB....",
        "....BBBBBBBBBB....."],
        eyes=((8, 6), (8, 11)), ink="K", blush=((10, 4), (10, 13)),
        col={"B": "#1783FF", "W": "#FFFFFF", "K": "#1C1D21"}),
    # 暗い角丸の体に、白い木の葉の切れ込み（口）。夜の暗い窓に埋もれないよう明るい縁を付けた。
    "qoder": dict(top=4, rows=[
        "....RRRRRRRRRR.....",
        "...RKKKKKKKKKKR....",
        "..RKKKKKKKKKKKKR...",
        "..RKKKKKKKKKKKKR...",
        "..RKKKKKKKKKKKKR...",
        "..RKKKKKKKKWWKKR...",
        "..RKKKKKKKWWKKKR...",
        "..RKKKKKKKKKKKKR...",
        "..RKKKKKKKKKKKKR...",
        "...RKKKKKKKKKKR....",
        "....RRRRRRRRRR....."],
        eyes=((7, 6), (7, 11)), ink="W", blush=((9, 5), (9, 12)),
        col={"R": "#BCBCBC", "K": "#1C1D21", "W": "#FFFFFF"}),
    # おかっぱの髪に白いヘアバンドの女の子。同梱の絵は 1 色なので、髪を暗く、顔を白くした。
    "hermes": dict(top=4, rows=[
        ".....HHHHHHHH......",
        "....HWWWWWWWWH.....",
        "...HHHHHHHHHHHH....",
        "...HHFHHFFHHFHH....",
        "..HHHFFFFFFFFHHH...",
        "..HHHFFFFFFFFHHH...",
        "..HHHFFFFFFFFHHH...",
        "..HHHHFFFFFFHHHH...",
        "..HHHH.FFFF.HHHH...",
        "......FFFFFF.......",
        ".....FFFFFFFF......"],
        eyes=((8, 6), (8, 11)), ink="H", blush=((10, 5), (10, 12)),
        col={"H": "#1C1D21", "W": "#FFFFFF", "F": "#FFFFFF"}),
}
def cast_base(b):  # 体の画素は小文字で持ち、小物（大文字）と記号が重ならないようにする
    g = {}
    for y, line in enumerate(CAST[b]["rows"]):
        for x, v in enumerate(line):
            if v != ".": g[(y + CAST[b].get("top", 5) - OY, x - OX)] = v.lower()
    return g
def at(g, y, x, v): g[(y - OY, x - OX)] = v
def face(g, b, how):
    d = CAST[b]
    ink = d["ink"].lower()
    if b == "codex":
        if how in ("normal", "up"):
            k = -1 if how == "up" else 0
            for y, x in ((7, 5), (8, 6), (9, 5), (9, 8), (9, 9), (9, 10)): at(g, y + k, x, ink)   # >_
        elif how == "happy":
            for y, x in ((8, 4), (7, 5), (8, 6), (8, 9), (7, 10), (8, 11)): at(g, y, x, ink)
        else:
            for y, x in ((8, 5), (8, 6), (8, 9), (8, 10)): at(g, y, x, ink)
        return
    for i, (y, x) in enumerate(d["eyes"]):
        if how == "normal": at(g, y, x, ink); at(g, y + 1, x, ink)
        elif how == "up": at(g, y - 1, x, ink); at(g, y, x, ink)
        elif how == "happy":
            at(g, y + 1, x - 1, ink); at(g, y, x, ink); at(g, y + 1, x + 1, ink)
        else:
            for dx in ((-1, 0) if i == 0 else (0, 1)): at(g, y + 1, x + dx, ink)
def cast_working(b):
    g = cast_base(b); face(g, b, "normal"); helmet(g); return g
def cast_blocked(b):  # 腕が無いので、「!」を 2 マス幅にして目立たせる
    g = cast_base(b); face(g, b, "up")
    for y in (0, 1, 2, 4):
        for x in (16, 17): at(g, y, x, "R")
    return g
def cast_done(b):
    g = cast_base(b); face(g, b, "happy")
    for y, x in CAST[b]["blush"] or (): at(g, y, x, "P")
    confetti(g); return g
def cast_idle(b):
    g = cast_base(b); face(g, b, "closed"); hat(g, 1); return g
CAST_POSES = {"working": cast_working, "blocked": cast_blocked, "done": cast_done, "idle": cast_idle}

CLAWD_BODIES = {"claude": "#D97757", "other": "#8FA3BF"}
# 小物の色違い（同じエージェントはいつも同じ色）: ヘルメット H・帽子 V
ACC = {"a": ("#F2B630", "#5B4BB7"), "b": ("#F28C30", "#3C5BB8"), "c": ("#E8E8E8", "#8A3FA8"), "d": ("#4FB0E8", "#2F6F8F")}
FIX = {"K": "#111111", "P": "#F59AAE", "S": "#8FD3FF", "W": "#FFF7C2", "G": "#A9ADB5", "O": "#C0602A",
       "R": "#E5484D", "Z": "#CFE3FF", "L": "#E8F6FF", "N": "#4C7DFF", "Y": "#FFD43B", "C": "#3BC9A0"}

def write(name, g, col):
    for (r, c) in g: assert 0 <= c + OX < W and 0 <= r + OY < H, (name, r, c)
    rects = "".join(f'<rect x="{c + OX}" y="{r + OY}" width="1" height="1" fill="{col[v]}"/>' for (r, c), v in sorted(g.items()))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}" shape-rendering="crispEdges">{rects}</svg>'
    open(os.path.join(out, name), "w").write(svg)

n = 0
for pose, fn in CLAWD.items():
    g = fn()
    for b, bc in CLAWD_BODIES.items():
        for a, (hc, vc) in ACC.items():
            write(f"{b}-{a}-{pose}.svg", g, dict(FIX, B=bc, H=hc, V=vc)); n += 1
for pose, fn in CAST_POSES.items():
    for b, d in CAST.items():
        g = fn(b)
        for a, (hc, vc) in ACC.items():
            col = dict(FIX, H=hc, V=vc, **{k.lower(): v for k, v in d["col"].items()})
            write(f"{b}-{a}-{pose}.svg", g, col); n += 1
print(n)
