# rooms mod の建物ごとの静止画（空・屋上・入口まわりの飾り）を生成し、
# icons/ にある全 SVG の大きさを art.js に書き出す。
#   python3 -I buildings.py <mods/rooms>
import sys, os, re, math

root = sys.argv[1]
icons = os.path.join(root, "icons")


def svg(rows, pal, name):
    h = len(rows); w = max(len(r) for r in rows)
    assert all(len(r) == w for r in rows), (name, [len(r) for r in rows])
    missing = {c for r in rows for c in r if c != "." and c not in pal}
    assert not missing, (name, missing)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{pal[c]}"/>'
                    for y, r in enumerate(rows) for x, c in enumerate(r) if c != ".")
    with open(os.path.join(icons, name + ".svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w*2}" height="{h*2}" shape-rendering="crispEdges">{rects}</svg>')


def canvas(w, h):
    return [["."] * w for _ in range(h)]


def put(cv, x0, y0, rows):
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != ".":
                cv[y0 + y][x0 + x] = c
    return cv


def rows(cv):
    return ["".join(r) for r in cv]


def mirror(rs):
    return [r[::-1] for r in rs]


def ring(cv, cx, cy, r, c):
    for y in range(len(cv)):
        for x in range(len(cv[0])):
            if abs(math.hypot(x - cx, y - cy) - r) < 0.55:
                cv[y][x] = c


def line(cv, x0, y0, x1, y1, c):
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        cv[round(y0 + (y1 - y0) * i / n)][round(x0 + (x1 - x0) * i / n)] = c


# ---- 空の飾り ----
SUN = ["...Y...", ".Y.Y.Y.", "..YYY..", "YYYYYYY", "..YYY..", ".Y.Y.Y.", "...Y..."]
MOON = ["..MMM..", ".MM....", "MM.....", "MM.....", "MM.....", ".MM....", "..MMM.."]
STARS = ["....Y.........", "...YYY......Y.", "....Y.........", "..........Y...", ".Y.......YYY..", "..........Y...", "......Y......."]
BIRD = [".BB.BB.", "B..B..B"]
DISC = ["..RRR..", ".RRRRR.", "RRRRRRR", "RRRRRRR", "RRRRRRR", ".RRRRR.", "..RRR.."]
SATURN = [
    "......PPPP......",
    "....PPPPPPpp....",
    "...PPPPPPPPpp...",
    "RRRRRRRRRRRRRRRR",
    ".RRPPPPPPPPPpRR.",
    "...PPPPPPPPpp...",
    "....PPPPPPpp....",
    "......PPPP......",
]
CLOUD_JP = [
    ".....CCCC.......",
    "...CC....CC.CCC.",
    "..C..CCC..CC...C",
    ".CCCCCCCCCCCCCC.",
    "CCCCCCCCCCCCCCCC",
]
CLOUD = ["....CCC.......", "..CCCCCCC.CC..", ".CCCCCCCCCCCC.", "CCCCCCCCCCCCCC", ".DDDDDDDDDDDD."]
FISH = [
    "...OOO..O",
    ".OOoOOOOO",
    "OkOoOOOO.",
    ".OOoOOOOO",
    "...OOO..O",
]
JELLY = [
    "..JJJJJ..",
    ".JJjJJJJ.",
    "JJjJJJJJJ",
    "JJJJJJJJJ",
    "J.J.J.J.J",
    "J.J.J.J.J",
    ".J.J.J.J.",
    ".J...J...",
    "...J...J.",
]
BUBBLE = [".b.", "b.b", ".b."]

# ---- アパート ----
TANK = [
    "...CCCCCC...",
    ".CCDDDDDDCC.",
    "CDDDDDDDDDDC",
    "CTTTTTTTTTTC",
    "CTtTTTTTTTTC",
    "CTtTTTTTTTTC",
    "CTtTTTTTTTTC",
    "CTTTTTTTTTTC",
    "CDDDDDDDDDDC",
    ".CCCCCCCCCC.",
    "..L......L..",
    "..LL....LL..",
    "..L.LLLL.L..",
    "..L......L..",
]
HUT = [
    "OOOOOOOOOOOO",
    "oWWWWWWWWWWo",
    "oWWWWWWWWWWo",
    "oWWdddWWWWWo",
    "oWWdddWWggWo",
    "oWWdddWWggWo",
    "oWWdddWWWWWo",
    "oWWdhdWWWWWo",
    "oWWdddWWWWWo",
]
ANTENNA = [
    "....P....",
    "A.A.P.A.A",
    "AAAAPAAAA",
    "A.A.P.A.A",
    "....P....",
    ".A.APA.A.",
    ".AAAPAAA.",
    ".A.APA.A.",
    "....P....",
    "....P....",
    "....P....",
    "....P....",
    "...PPP...",
    "..PPPPP..",
]
MAILBOX = [
    "KKKKKKKKKK",
    "KMMKMMKMMK",
    "KmmKmmKmmK",
    "KKKKKKKKKK",
    "KMMKMMKMMK",
    "KmmKmmKmmK",
    "KKKKKKKKKK",
    ".L......L.",
]
VENDING = [
    "RRRRRRRRRR",
    "RWWWWWWWWR",
    "RWcWbWyWWR",
    "RWcWbWyWWR",
    "RWWWWWWWWR",
    "RWgWcWbWWR",
    "RWgWcWbWWR",
    "RWWWWWWWWR",
    "RRRRRRRRRR",
    "RRRRRRRdRR",
    "RRRRRRRdRR",
    "RkkkkkkkkR",
    "RRRRRRRRRR",
    ".LL....LL.",
]
POT = [
    "..G...",
    ".GGG.G",
    "GGHGGG",
    ".GGGG.",
    "..GG..",
    ".PPPP.",
    ".PPPP.",
    "..PP..",
]


def bicycle():
    cv = canvas(18, 10)
    ring(cv, 3, 6, 3, "W"); ring(cv, 14, 6, 3, "W")
    for a, b in [((3, 6), (8, 6)), ((8, 6), (6, 2)), ((6, 2), (3, 6)), ((6, 2), (12, 2)), ((12, 2), (8, 6)), ((12, 2), (14, 6))]:
        line(cv, *a, *b, "B")
    for x in (5, 6, 7): cv[1][x] = "S"
    cv[1][12] = "H"; cv[0][12] = "H"; cv[0][13] = "H"
    for y in (2, 3, 4):
        for x in (14, 15, 16): cv[y][x] = "Q"
    return rows(cv)


# ---- ホテル ----
STAR = ["..Y..", ".YYY.", "YYYYY", ".YYY.", ".Y.Y."]


def sign():
    cv = canvas(35, 12)
    for x in range(35):
        for y in (0, 8):
            cv[y][x] = "B" if x % 2 == 0 else "G"
    for y in range(1, 8):
        cv[y][0] = "B" if y % 2 == 0 else "G"; cv[y][34] = "B" if y % 2 == 0 else "G"
        for x in range(1, 34): cv[y][x] = "N"
    for i in range(5): put(cv, 3 + i * 6, 2, STAR)
    for y in range(9, 12):
        cv[y][8] = "L"; cv[y][26] = "L"
    return rows(cv)


TOPIARY = [
    "..GGGG..",
    ".GHGGGG.",
    "GHGGGGGG",
    "GGGGGGHG",
    ".GGGGGG.",
    "..GGGG..",
    "...TT...",
    "..GGGG..",
    ".GHGGGG.",
    "..GGGG..",
    ".PPPPPP.",
    "..PPPP..",
]
LAMP = [".LLL.", "LYYYL", "LYYYL", ".LLL.", "..L..", "..L..", "..L..", "..L..", "..L..", "..L..", "..L..", "..L..", ".LLL.", "LLLLL"]

# ---- 潜水艦 ----
SAIL = [
    "..........p.........",
    "..........pp........",
    "..........p.........",
    "....hhhhhhphhhh.....",
    "...hSSSSSSSSSSSS....",
    "..hSSSSSSSSSSSSSS...",
    "..SSwSSwSSwSSSSSS...",
    "..SSSSSSSSSSSSSSS...",
    "FFSSSSSSSSSSSSSSSFF.",
    "..SSSSSSSSSSSSSSS...",
    "..SSSSSSSSSSSSSSS...",
    "..SSSSSSSSSSSSSSS...",
]
SEAWEED = [
    "..G...",
    ".GG...",
    ".G..G.",
    "..G.GG",
    "..GG.G",
    ".GG..G",
    ".G..GG",
    ".G.GG.",
    "..GG..",
    "..G.G.",
    ".GG.GG",
    ".G...G",
    ".G..GG",
    ".GG.G.",
]
CHEST = [
    "..BBBBBB..",
    ".BbbbbbbB.",
    "BBBBYYBBBB",
    "BbbbYYbbbB",
    "BbbbbbbbbB",
    "BbbbbbbbbB",
    "BBBBBBBBBB",
]
ROCK = ["..RRR..", ".RRrRR.", "RRRRRRr", "RRRRRRR"]
STARFISH = ["..P..", "PPPPP", ".PPP.", ".P.P.", "P...P"]

# ---- ロケット ----
TIP = [".L.", "LYL", ".L.", ".P.", ".P.", ".P."]
FIN = [
    ".......F",
    "......fF",
    "......fF",
    ".....fFF",
    ".....fFF",
    "....fFFF",
    "....fFFF",
    "...fFFFF",
    "...fFFFF",
    "..fFFFFF",
    "..fFFFFF",
    ".fFFFFFF",
    ".fFFFFFF",
    "fFFFFFFF",
    "fFFFFFFF",
    "fFFF....",
]
FLAME = [
    "yyyyyyyyyy",
    "yYYYYYYYYy",
    ".yYWWWWYy.",
    ".yYYWWYYy.",
    "..oyYYyo..",
    "..oyYYyo..",
    "...oyyo...",
    "....oo....",
    "....rr....",
]

# ---- お城 ----
SHACHI = [".....YY", "....YY.", "....Y..", "...YY..", "..YYY..", ".YYYY..", "YkYYY..", "YYYY..."]
GABLE = [
    "......Y.......",
    ".....KWK......",
    "....KWWWK.....",
    "...KWWYWWK....",
    "..KWWWWWWWK...",
    ".KWWWWWWWWWK..",
    "KKKKKKKKKKKKK.",
]
PINE = [
    ".....GGGG.....",
    "..GGGGGHGGG...",
    ".GGHGGGGGGGG..",
    "......TT......",
    "...GGGGTGGGGG.",
    ".GGGHGGGGGHGGG",
    "....TTTT......",
    "..GGGGGTTGGG..",
    "GGHGGGGGGGGHGG",
    ".......TT.....",
    "......TTT.....",
    ".....TTTT.....",
]

# ---- 書き出し ----
# 学校以外の建物は昼と夜の 2 枚ずつ: <部品>-<建物>-day / -night。夜は色を夜空の紺へ寄せ、
# 光るもの（灯った窓・ランプ・看板・自販機・炎・くらげ）だけ元の色のまま残す。
NAVY = (29, 33, 64)


def dimc(h, k):
    rgb = (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
    return "#%02x%02x%02x" % tuple(round(v + (n - v) * k) for v, n in zip(rgb, NAVY))


def night(pal, keep="", k=0.55, **over):
    out = {c: (v if c in keep else dimc(v, k)) for c, v in pal.items()}
    out.update(over)
    return out


def both(rs, pal, name, keep="", **over):
    svg(rs, pal, f"{name}-day")
    svg(rs, night(pal, keep, **over), f"{name}-night")


DAYSKY = dict(Y="#ffcf3f", C="#ffffff", D="#dbe8f2", B="#f4f1e8")
NIGHTSKY = dict(M="#f7e7a6", Y="#f7e7a6")
birds = rows(put(put(canvas(16, 7), 0, 1, BIRD), 8, 4, BIRD))

APT = dict(Y="#ffcf3f", B="#f4f1e8", C="#5d6670", D="#aab6bf", T="#cfd8de", t="#ffffff", L="#5d6670",
           O="#8d959d", o="#c9c2b6", W="#ece6dc", d="#7a8590", h="#e6c47a", g="#cfe3ee", A="#5d6670", P="#5d6670",
           K="#6b7380", M="#c3c9d1", m="#3a3f47", R="#3a6fd1", c="#e74c3c", b="#3d7be0", y="#f5c242",
           k="#24489a", G="#4f9a3c", H="#7cc35a", Q="#9aa1a8", S="#3a3f47")
svg(SUN, DAYSKY, "skyL-apartment-day"); svg(birds, DAYSKY, "skyR-apartment-day")
svg(MOON, NIGHTSKY, "skyL-apartment-night"); svg(STARS, NIGHTSKY, "skyR-apartment-night")
both(rows(put(put(put(canvas(44, 14), 1, 5, HUT), 17, 0, TANK), 33, 0, ANTENNA)), APT, "roof-apartment", g="#ffd98a")
both(rows(put(put(canvas(29, 12), 0, 2, bicycle()), 19, 4, MAILBOX)), {**APT, "W": "#3a3f47"}, "baseL-apartment")
VEND = {**APT, "W": "#f4f7fb", "R": "#3a6fd1", "d": "#24489a", "g": "#2ecc71", "P": "#b5653a"}
both(rows(put(put(canvas(17, 14), 0, 6, POT), 7, 0, VENDING)), VEND, "baseR-apartment", keep="Wcbyg")

HOTEL = dict(Y="#ffd75e", B="#fff3c4", G="#e6b450", N="#1d2340", L="#3b3f5c")
SIDE = dict(Y="#ffd75e", G="#3f7f45", H="#5fa35a", T="#6b4a2e", P="#c9a24a", L="#2b2f45")
svg(SUN, DAYSKY, "skyL-hotel-day"); svg(CLOUD, DAYSKY, "skyR-hotel-day")
svg(MOON, NIGHTSKY, "skyL-hotel-night"); svg(STARS, NIGHTSKY, "skyR-hotel-night")
svg(sign(), {**HOTEL, "B": "#d9d2b8", "Y": "#e6c45a"}, "sign-hotel-day")
svg(sign(), HOTEL, "sign-hotel-night")
side = rows(put(put(canvas(15, 14), 0, 0, LAMP), 7, 2, TOPIARY))
for name, rs in (("baseL-hotel", side), ("baseR-hotel", mirror(side))):
    svg(rs, {**SIDE, "Y": "#e8e2c8"}, f"{name}-day")
    svg(rs, night(SIDE, "Y"), f"{name}-night")

SUB = dict(O="#ff9f43", o="#ffffff", k="#262626", J="#f7a6d8", j="#ffd6ef", b="#bfe8ff",
           S="#4d6170", h="#6d8494", w="#ffd98a", F="#33434f", p="#33434f",
           G="#3f9a6a", B="#7a4a2a", Y="#f2c14e", R="#6f7a85", r="#8f9aa5", P="#ff8a7a")
both(rows(put(put(canvas(16, 10), 0, 0, FISH), 7, 5, FISH)), SUB, "skyL-submarine")
both(rows(put(put(put(canvas(14, 12), 5, 0, JELLY), 0, 6, BUBBLE), 2, 9, BUBBLE)), SUB, "skyR-submarine",
     J="#7ff3ff", j="#d6fbff", b="#7ff3ff")
both(SAIL, SUB, "sail-submarine", keep="w")
both(rows(put(put(canvas(18, 14), 0, 0, SEAWEED), 8, 7, CHEST)), {**SUB, "b": "#a8693a"}, "baseL-submarine")
both(rows(put(put(put(canvas(19, 14), 0, 10, ROCK), 7, 9, STARFISH), 13, 0, SEAWEED)), SUB, "baseR-submarine")

ROCKET = dict(P="#f4c26b", p="#d9a04a", R="#e9dcc0", Y="#fff3c4", L="#8d99a6",
              F="#d6453d", f="#a8322c", y="#ffb340", W="#fff6d6", o="#ff7a2f", r="#e8462a",
              C="#e4e7ec", D="#c3cad3")
svg(SUN, DAYSKY, "skyL-rocket-day"); svg(CLOUD, DAYSKY, "skyR-rocket-day")
svg(SATURN, ROCKET, "skyL-rocket-night"); svg(STARS, ROCKET, "skyR-rocket-night")
both(TIP, {"L": "#8d99a6", "Y": "#ff5f5f", "P": "#8d99a6"}, "tip-rocket", keep="Y")
both(FIN, {"F": "#d6453d", "f": "#a8322c"}, "finL-rocket")
both(mirror(FIN), {"F": "#d6453d", "f": "#ef6b5f"}, "finR-rocket")
flame = {"y": "#ffb340", "Y": "#ffd75e", "W": "#fff6d6", "o": "#ff7a2f", "r": "#e8462a"}
svg(FLAME, flame, "flame-rocket-day"); svg(FLAME, flame, "flame-rocket-night")
both(CLOUD, {"C": "#e4e7ec", "D": "#c3cad3"}, "smoke-rocket")

CASTLE = dict(R="#e8553f", C="#f4efe2", Y="#e6b450", k="#262626", K="#2e2e33", W="#f4f0e6",
              G="#2f6b3a", H="#4f8f4a", T="#6b4a2e")
svg(DISC, CASTLE, "skyL-castle-day"); svg(DISC, {"R": "#f7e7a6"}, "skyL-castle-night")
both(CLOUD_JP, CASTLE, "skyR-castle")
ridge = canvas(36, 12)
for x in range(5, 31):
    ridge[6][x] = "K"; ridge[7][x] = "K"
put(ridge, 1, 0, mirror(SHACHI)); put(ridge, 28, 0, SHACHI); ridge = ridge + [["."] * 36]
put(ridge, 11, 6, GABLE)
both(rows(ridge), CASTLE, "ridge-castle", keep="Y")
both(PINE, CASTLE, "pineL-castle")
both(mirror(PINE), CASTLE, "pineR-castle")

# ヘッダーの昼夜の印（一色。描く側が文字色で塗る）
svg(SUN, {"Y": "#000000"}, "time-day")
svg(MOON, {"M": "#000000"}, "time-night")

# icons/ の全 SVG の大きさ（viewBox）を art.js に。描く側はこれで縦横比を合わせる。
sizes = {}
for f in sorted(os.listdir(icons)):
    if f.endswith(".svg"):
        m = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(os.path.join(icons, f)).read())
        if m:
            sizes[f[:-4]] = (int(m.group(1)), int(m.group(2)))
with open(os.path.join(root, "art.js"), "w") as f:
    f.write("// Generated: each picture in icons/ and its size in art pixels (viewBox).\n")
    f.write("export const ART = {\n" + "".join(f'  "{k}": [{w}, {h}],\n' for k, (w, h) in sizes.items()) + "};\n")
print(len(sizes), "pictures")
