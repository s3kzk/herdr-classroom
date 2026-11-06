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
svg(SUN, DAYSKY, "skyL-castle-day"); svg(DISC, {"R": "#f7e7a6"}, "skyL-castle-night")
both(CLOUD_JP, CASTLE, "skyR-castle")
ridge = canvas(36, 12)
for x in range(5, 31):
    ridge[6][x] = "K"; ridge[7][x] = "K"
put(ridge, 1, 0, mirror(SHACHI)); put(ridge, 28, 0, SHACHI); ridge = ridge + [["."] * 36]
put(ridge, 11, 6, GABLE)
both(rows(ridge), CASTLE, "ridge-castle", keep="Y")
both(PINE, CASTLE, "pineL-castle")
both(mirror(PINE), CASTLE, "pineR-castle")

# ---- オフィス ----
AC = [
    "OOOOOOOOOO",
    "oGGGGGGGGo",
    "oGgGgGgGgo",
    "oGGGGGGGGo",
    "oGgGgGgGgo",
    "oGGGGGGGGo",
    "OOOOOOOOOO",
    ".L......L.",
]
MAST = ["..R..", "..P..", ".PPP.", "..P..", "..P..", "..P..", "..P..", "..P..", "..P..", "..P..", "..P..", "..P..", ".PPP.", "PPPPP"]
BENCH = ["WWWWWWWWWW", "wwwwwwwwww", "L........L", "L........L"]
OFFICE = dict(O="#7d8791", o="#a9b2ba", G="#c9d0d6", g="#8d969e", L="#3a3f47", R="#ff4d4d", P="#5d6670",
              W="#b5835a", w="#8a5f3c", H="#7cc35a")
svg(SUN, DAYSKY, "skyL-office-day"); svg(birds, DAYSKY, "skyR-office-day")
svg(MOON, NIGHTSKY, "skyL-office-night"); svg(STARS, NIGHTSKY, "skyR-office-night")
both(rows(put(put(put(canvas(44, 14), 2, 6, AC), 14, 6, AC), 36, 0, MAST)), OFFICE, "roof-office", keep="R")
office_side = rows(put(put(canvas(18, 8), 0, 0, POT), 8, 4, BENCH))
both(office_side, {**OFFICE, "G": "#4f9a3c", "P": "#b5653a"}, "baseL-office")
both(mirror(office_side), {**OFFICE, "G": "#4f9a3c", "P": "#b5653a"}, "baseR-office")

# ---- 旅館 ----
# 鬼瓦を両端に載せた棟、赤い提灯、石灯籠、紅葉、竹。
def ridge_jp(w):
    cv = canvas(w, 5)
    for x in range(3, w - 3):
        cv[2][x] = "k"; cv[3][x] = "K"; cv[4][x] = "K"
    for x0 in (0, w - 3):
        for y in range(5):
            for x in range(x0, x0 + 3):
                cv[y][x] = "K"
        cv[1][x0 + 1] = "k"
    return rows(cv)


CHOCHIN = [".kkk.", "RRRRR", "RrRRR", "RRRRR", "RrRRR", "RRRRR", ".kkk.", "..k.."]
TORO = [
    "....S....",
    "..SSSSS..",
    ".SSSSSSS.",
    "SSSSSSSSS",
    "..sssss..",
    "..sYYYs..",
    "..sYYYs..",
    "..sssss..",
    ".SSSSSSS.",
    "...sss...",
    "...sss...",
    "...sss...",
    "..SSSSS..",
    ".SSSSSSS.",
]
MOMIJI = [
    "....RRRR......",
    "..RRrRRRRO....",
    ".RRRRRRrRRRR..",
    "RRrRRORRRRRRR.",
    "RRRRRRRRrRRRO.",
    ".RRORRRRRRRR..",
    "..RRRRTRRRR...",
    "....RTTR......",
    "......TT......",
    "......TT......",
    "......TT......",
    ".....TTT......",
    "....TTTT......",
]


def bamboo():
    cv = canvas(9, 14)
    for x in (1, 4, 7):
        for y in range(3, 14):
            cv[y][x] = "g" if y % 4 == 1 else "B"
    for x, y in ((0, 0), (2, 1), (3, 0), (5, 1), (6, 0), (8, 1), (0, 2), (2, 3), (5, 3), (8, 3), (3, 2), (6, 2)):
        cv[y][x] = "L"
    return rows(cv)


LEAF = [".R.", "RRR", ".R."]
leaves = rows(put(put(put(put(canvas(14, 10), 1, 0, LEAF), 8, 2, [".O.", "OOO", ".O."]), 4, 5, LEAF), 11, 7, [".O.", "OOO", ".O."]))
RYOKAN = dict(K="#3d4250", k="#5b6274", R="#d8402f", r="#ff8a5c", S="#9a968c", s="#7f7b72", Y="#3a3a3a",
              O="#f2a33a", T="#6b4a2e", B="#6f9a3f", g="#4f7a2c", L="#8fbf5a")
svg(SUN, DAYSKY, "skyL-ryokan-day"); svg(leaves, RYOKAN, "skyR-ryokan-day")
svg(MOON, NIGHTSKY, "skyL-ryokan-night"); svg(STARS, NIGHTSKY, "skyR-ryokan-night")
both(ridge_jp(36), RYOKAN, "ridge-ryokan")
both(CHOCHIN, RYOKAN, "lantern-ryokan", keep="Rrk")
ryokan_l = rows(put(put(canvas(24, 14), 0, 1, MOMIJI), 15, 0, TORO))
ryokan_r = mirror(rows(put(put(canvas(24, 14), 0, 0, bamboo()), 15, 0, TORO)))
both(ryokan_l, RYOKAN, "baseL-ryokan", Y="#ffd27a")
both(ryokan_r, RYOKAN, "baseR-ryokan", Y="#ffd27a")

# ---- 銭湯 ----
# 唐破風の屋根と煙突、♨ の看板、黄色い湯桶、瓶の牛乳の自販機。
KARAHAFU = [
    "......KKKK......",
    "...KKKkkkkKKK...",
    ".KKkkwwwwwwkkKK.",
    "KkwwwwwYYwwwwwkK",
    "Kwwwwwwwwwwwwwwk",
    "KKKKKKKKKKKKKKKK",
]


def chimney():
    cv = canvas(7, 20)
    for y in range(2, 20):
        for x in range(1, 6):
            cv[y][x] = "b" if (y % 3 == 0 or (x + (y // 3)) % 4 == 0) else "C"
    for x in range(7):
        cv[2][x] = "K"; cv[3][x] = "K"
    return rows(cv)


SMOKE = ["....DD....", "..DDDDDD..", ".DDDDDDDD.", "..DDDD.DD.", "......DDD.", ".......DD."]
ONSEN = [
    "...........",
    "..r..r..r..",
    ".r..r..r...",
    "..r..r..r..",
    ".r..r..r...",
    "r.........r",
    ".r.......r.",
    "..rrrrrrr..",
    "...........",
]
BUCKET = ["YYYYYY", "yYYYYy", ".yyyy."]
MILK = [
    "RRRRRRRRRR",
    "RWWWWWWWWR",
    "RWmWmWcWWR",
    "RWmWmWcWWR",
    "RWWWWWWWWR",
    "RWpWpWmWWR",
    "RWpWpWmWWR",
    "RWWWWWWWWR",
    "RRRRRRRRRR",
    "RRRRRRRdRR",
    "RkkkkkkkkR",
    "RRRRRRRRRR",
    ".LL....LL.",
]
SENTO = dict(K="#3d4250", k="#5b6274", W="#f4efe2", w="#a0683c", Y="#e6b450", C="#b5533c", b="#8a3a2a", D="#e9ecef",
             r="#d8402f", y="#d9a520", R="#3a7fd1", m="#ffffff", c="#a8693a", p="#f2a7b8", d="#24489a", L="#3a3f47")
svg(SUN, DAYSKY, "skyL-sento-day"); svg(CLOUD_JP, {"C": "#ffffff"}, "skyR-sento-day")
svg(MOON, NIGHTSKY, "skyL-sento-night"); svg(STARS, NIGHTSKY, "skyR-sento-night")
sento_roof = canvas(44, 20)
put(sento_roof, 26, 0, SMOKE); put(sento_roof, 34, 0, chimney()); put(sento_roof, 8, 14, KARAHAFU)
both(rows(sento_roof), SENTO, "roof-sento", keep="Y", D="#7d8191")
sign_cv = canvas(13, 11)
for y in range(11):
    for x in range(13):
        sign_cv[y][x] = "K" if y in (0, 10) or x in (0, 12) else "W"
put(sign_cv, 1, 1, ONSEN)
both(rows(sign_cv), SENTO, "sign-sento", keep="rW")
buckets = rows(put(put(put(canvas(14, 8), 4, 0, BUCKET), 1, 3, BUCKET), 7, 3, BUCKET))
buckets = rows(put([list(r) for r in buckets], 4, 6, ["......"]))
both(rows(put(put(canvas(20, 13), 0, 5, buckets), 0, 0, ["." * 20])), SENTO, "baseL-sento")
both(rows(put(put(canvas(17, 13), 0, 5, POT), 7, 0, MILK)), {**SENTO, "G": "#4f9a3c", "H": "#7cc35a", "P": "#b5653a"}, "baseR-sento", keep="Wmcp")

# ---- 街の遠景（Tokyo / Kyoto / Osaka / Mt.Fuji）----
# 建物の上に帯で描く。town-<街>-L / -R（左右の名所）と、富士だけ -C（中央の山）。
def tower_tokyo():
    W, H = 15, 32; cv = canvas(W, H); cx = 7
    for y in range(H):
        hw = round(0.4 + (y / (H - 1)) ** 1.7 * 7)
        c = "R" if (y // 4) % 2 == 0 else "W"
        cv[y][cx - hw] = c; cv[y][cx + hw] = c
        if y < 5: cv[y][cx] = "R"
        if y % 3 == 0 and 2 <= hw and y < 27:
            for x in range(cx - hw, cx + hw + 1):
                if (x + y) % 2 == 0: cv[y][x] = c
    for y, w in ((12, 3), (13, 3), (21, 5), (22, 5)):
        for x in range(cx - w, cx + w + 1): cv[y][x] = "D"
    return rows(cv)


def city_blocks():
    W, H = 30, 24; cv = canvas(W, H)
    for x0, w, h in ((0, 7, 14), (8, 6, 22), (15, 8, 17), (24, 6, 11)):
        for y in range(H - h, H):
            for x in range(x0, x0 + w):
                edge = x in (x0, x0 + w - 1) or y == H - h
                cv[y][x] = "B" if edge else ("w" if (y % 3 == 1 and (x - x0) % 2 == 1) else "b")
    for y in range(H - 22 - 4, H - 22): cv[y][11] = "P"
    return rows(cv)


def pagoda(tiers=5, w0=17):
    H = tiers * 5 + 6; cv = canvas(w0, H); cx = w0 // 2
    for y in range(6): cv[y][cx] = "Y"
    for i in range(tiers):
        y = 6 + i * 5; ew = 2 + i * 1.2; bw = 1 + i
        for x in range(round(cx - ew - 1), round(cx + ew + 2)):
            if 0 <= x < w0: cv[y][x] = "K"
        for x in range(round(cx - ew), round(cx + ew + 1)): cv[y + 1][x] = "k"
        cv[y][max(0, round(cx - ew - 1))] = "K"; cv[y - 1][max(0, round(cx - ew - 1))] = "K"
        cv[y - 1][min(w0 - 1, round(cx + ew + 1))] = "K"
        for yy in range(y + 2, y + 5):
            for x in range(cx - bw, cx + bw + 1): cv[yy][x] = "V" if x in (cx - bw, cx + bw) else "v"
    return rows(cv)


TORII = [
    "VV..............VV",
    "KKKKKKKKKKKKKKKKKK",
    ".VVVVVVVVVVVVVVVV.",
    "...V....VV....V...",
    ".VVVVVVVVVVVVVVVV.",
    "...V..........V...",
    "...V..........V...",
    "...V..........V...",
    "...V..........V...",
    "...V..........V...",
    "...V..........V...",
    "...V..........V...",
    "..KKK........KKK..",
]


def osaka_castle():
    W, H = 24, 26; cv = canvas(W, H); cx = W // 2
    for i, (y, w) in enumerate(((21, 11), (22, 11), (23, 12), (24, 12), (25, 12))):
        for x in range(cx - w, cx + w): cv[y][x] = "S" if (x + i) % 4 else "s"
    tiers = ((15, 8, 6), (9, 6, 5), (4, 4, 4))
    for y0, hw, h in tiers:
        for y in range(y0 + 1, y0 + h + 1):
            for x in range(cx - hw + 1, cx + hw - 1): cv[y][x] = "W" if (y + x) % 5 else "w"
        for x in range(cx - hw - 1, cx + hw + 1): cv[y0][x] = "G"
        for x in range(cx - hw, cx + hw): cv[y0 + 1][x] = "g"
        cv[y0 - 1][cx - hw - 1] = "G"; cv[y0 - 1][cx + hw] = "G"; cv[y0][cx - 1] = "Y"; cv[y0][cx] = "Y"
    for x in (cx - 3, cx + 2): cv[2][x] = "Y"; cv[3][x] = "Y"
    for x in range(cx - 3, cx + 3): cv[3][x] = "G" if cv[3][x] == "." else cv[3][x]
    return rows(cv)


def tsutenkaku():
    W, H = 13, 30; cv = canvas(W, H); cx = 6
    for y in range(0, 2): cv[y][cx] = "M"
    for y, w in ((2, 2), (3, 3)):
        for x in range(cx - w, cx + w + 1): cv[y][x] = "M"
    for y in range(4, 10):
        for x in range(cx - 4, cx + 5): cv[y][x] = "L" if y in (6, 7) and x % 2 == 0 else "M"
    for y in range(10, 24):
        for x in (cx - 2, cx + 2): cv[y][x] = "M"
        if y % 2 == 0:
            for x in range(cx - 1, cx + 2): cv[y][x] = "m"
        if 14 <= y <= 16:
            for x in range(cx - 2, cx + 3): cv[y][x] = "N"
    for y in range(24, 30):
        k = y - 23
        cv[y][max(0, cx - 2 - k)] = "M"; cv[y][min(W - 1, cx + 2 + k)] = "M"
        if y == 24:
            for x in range(cx - 3, cx + 4): cv[y][x] = "M"
    return rows(cv)


def fuji():
    W, H = 84, 32; cv = canvas(W, H); cx = 41.5
    for y in range(H):
        hw = 4 + y * 1.22
        for x in range(W):
            d = x - cx
            if abs(d) <= hw:
                snow = y < 10 + (2 if int(x) % 5 in (0, 1) else 0) - (1 if int(x) % 7 == 3 else 0)
                cv[y][x] = "S" if snow else ("f" if d > hw * 0.35 else "F")
    return rows(cv)


CHERRY = [r.replace("R", "P").replace("r", "p").replace("O", "o") for r in MOMIJI]
TOWN = dict(R="#e8553f", W="#f4f1e8", D="#e8553f", B="#4a5670", b="#6b7a94", w="#ffe9a8", P="#d64545",
            Y="#e6b450", K="#3d4250", k="#5b6274", V="#d8402f", v="#e8743f",
            S="#a19f97", s="#8d8b84", G="#3f8a6a", g="#2f6b52",
            M="#9aa3ad", m="#7d8791", L="#ffd75e", N="#3db7e0",
            F="#4a73b0", f="#3a5c94", T="#6b4a2e", p="#f7c6d9", o="#ffe3ee")
TOWN_PINK = {**TOWN, "P": "#f2a7c3"}
both(tower_tokyo(), TOWN, "town-tokyo-L", keep="RWD")
both(city_blocks(), TOWN, "town-tokyo-R", keep="wP")
both(pagoda(), TOWN, "town-kyoto-L")
both(rows(put(put(canvas(32, 14), 0, 1, MOMIJI), 14, 1, TORII)), {**TOWN, "R": "#d6402e", "r": "#f07a3a", "O": "#f2a33a"}, "town-kyoto-R")
both(osaka_castle(), TOWN, "town-osaka-L", keep="Y")
both(tsutenkaku(), TOWN, "town-osaka-R", keep="LN")
both(fuji(), TOWN, "town-fuji-C", S="#c9d3e6")
both(rows(put(canvas(14, 13), 0, 0, CHERRY)), TOWN_PINK, "town-fuji-L")
both(rows(put(put(canvas(30, 31), 0, 18, CHERRY), 13, 0, pagoda())), TOWN_PINK, "town-fuji-R")

# ---- 街の帯の追加の飾り：遠景（far）、M / N（左右寄り）、C（中央）、T（中央手前の列車）----
def far_city(seed, W=48, H=16):
    cv = canvas(W, H); x = 0; i = 0
    while x < W:
        w = 3 + (seed * (i + 3)) % 5; h = 5 + (seed * (i + 7) * 3) % (H - 4)
        for y in range(H - h, H):
            for xx in range(x, min(W, x + w)):
                cv[y][xx] = "w" if (y % 3 == 1 and (xx - x) % 2 == 1 and y > H - h) else "B"
        x += w + (i % 2); i += 1
    return rows(cv)


def far_hills(W=48, H=12):
    cv = canvas(W, H)
    for x in range(W):
        h1 = round(7 + 3 * math.sin(x / 6.0)); h2 = round(4 + 2 * math.sin(x / 4.0 + 1.3))
        for y in range(H - h1, H): cv[y][x] = "H"
        for y in range(H - h2, H): cv[y][x] = "h"
    return rows(cv)


def far_lake(W=48, H=5):
    cv = canvas(W, H)
    for y in range(H):
        for x in range(W): cv[y][x] = "a" if (x * 7 + y * 3) % 11 == 0 else "A"
    return rows(cv)


def skytree(H=40):
    W = 11; cv = canvas(W, H); cx = 5
    for y in range(H):
        hw = 0 if y < 6 else round((y - 6) / (H - 6) * 4.5)
        cv[y][cx - hw] = "M"; cv[y][cx + hw] = "M"
        if y % 4 == 0:
            for x in range(cx - hw, cx + hw + 1): cv[y][x] = "m"
    for y, w in ((14, 2), (15, 2), (21, 3), (22, 3)):
        for x in range(cx - w, cx + w + 1): cv[y][x] = "L"
    cv[0][cx] = "R"
    return rows(cv)


def neon(cols, H=16):
    W = len(cols) * 5; cv = canvas(W, H)
    for i, c in enumerate(cols):
        x0 = i * 5; top = (i * 3) % 5
        for y in range(top, H):
            for x in range(x0, x0 + 4):
                cv[y][x] = "K" if x in (x0, x0 + 3) or y in (top, H - 1) else (c if y % 2 else c.lower())
    return rows(cv)


def shinkansen(W=44, viaduct=True):
    H = 11 if viaduct else 7; cv = canvas(W, H)
    body = [
        "......" + "W" * (W - 6),
        "...WW" + "".join("d" if (x % 3 == 0) else "W" for x in range(W - 5)),
        ".WWWWW" + "W" * (W - 6),
        "WW" + "U" * (W - 2),
        "W" * W,
        "." + "g" * (W - 1),
    ]
    for y, r in enumerate(body): cv[y] = list(r)
    for x in range(1, W, 6): cv[6][x] = "k"
    if viaduct:
        for x in range(W): cv[7][x] = "G"
        for y in range(8, 11):
            for x in range(3, W - 1, 10):
                cv[y][x] = "G"; cv[y][x + 1] = "G"
    return rows(cv)


def ferris(R=11):
    W = 2 * R + 3; H = 2 * R + 6; cv = canvas(W, H); cx, cy = R + 1, R + 1
    ring(cv, cx, cy, R - 1, "M")
    for a in range(8):
        t = a * math.pi / 4
        line(cv, cx, cy, round(cx + (R - 1) * math.cos(t)), round(cy + (R - 1) * math.sin(t)), "m")
        x, y = round(cx + R * math.cos(t)), round(cy + R * math.sin(t))
        for dx in (0, 1):
            if 0 <= x + dx < W and 0 <= y < H: cv[y][x + dx] = "PYNV"[a % 4]
    line(cv, cx, cy, cx - 6, H - 1, "M"); line(cv, cx, cy, cx + 6, H - 1, "M")
    for x in range(cx - 8, cx + 9): cv[H - 1][x] = "K"
    return rows(cv)


SMALL_TORII = ["VV....VV", "KKKKKKKK", ".VVVVVV.", "..V..V..", "..V..V..", "..V..V..", ".KK..KK."]
senbon = canvas(34, 9)
for i in range(5):
    put(senbon, i * 6, 2 - (i % 2), SMALL_TORII if i % 2 == 0 else [r for r in SMALL_TORII])
senbon = rows(senbon)

FAR = dict(B="#3c4a6b", w="#ffe9a8", H="#7fa37a", h="#5f8a5c", A="#6fb2e0", a="#d6eefa")
BIGPAL = {**TOWN, "U": "#2f6fd1", "d": "#5a6a80", "g": "#9aa3ad", "k": "#3a3f47", "W": "#f7f8fa", "G": "#8d969e"}
# Tokyo
both(far_city(7), {**FAR, "B": "#4a5a80"}, "town-tokyo-far", keep="w")
both(skytree(), TOWN, "town-tokyo-N", keep="LR")
both(neon(["P", "N", "Y"]), {**TOWN, "P": "#ff4fa3", "p": "#ff8cc6", "N": "#37e0ff", "n": "#a6f3ff", "Y": "#ffd84a", "y": "#fff0a6", "K": "#2b2f45"}, "town-tokyo-M", keep="PpNnYy")
both(shinkansen(), BIGPAL, "town-tokyo-T", keep="d")
# Kyoto
both(far_hills(), FAR, "town-kyoto-far")
both(MOMIJI, {**TOWN, "R": "#d6402e", "r": "#f07a3a", "O": "#f2a33a"}, "town-kyoto-M")
both(mirror(MOMIJI), {**TOWN, "R": "#e8553f", "r": "#f2a33a", "O": "#ffd166"}, "town-kyoto-N")
both(senbon, TOWN, "town-kyoto-C")
# Osaka
both(far_city(5), {**FAR, "B": "#5a4a6b", "w": "#ffd27a"}, "town-osaka-far", keep="w")
both(neon(["Y", "P", "N", "P"]), {**TOWN, "P": "#ff5f6d", "p": "#ff9aa4", "N": "#37e0ff", "n": "#a6f3ff", "Y": "#ffd84a", "y": "#fff0a6", "K": "#2b2f45"}, "town-osaka-M", keep="PpNnYy")
both(ferris(), {**TOWN, "M": "#e8553f", "m": "#f4a08f", "P": "#ff8cc6", "Y": "#ffd84a", "N": "#37e0ff", "V": "#9b7bff", "K": "#3d4250"}, "town-osaka-C", keep="MPYNV")
# Mt.Fuji
both(far_lake(), FAR, "town-fuji-far")
both(rows(put(canvas(14, 13), 0, 0, CHERRY)), TOWN_PINK, "town-fuji-M")
both(shinkansen(56, viaduct=False), BIGPAL, "town-fuji-T", keep="d")

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
