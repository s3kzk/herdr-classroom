# 校舎（school）の静止画の部品（時計塔・木・空の飾り）を昼と夜の 2 柄で生成する。
#   python3 -I scene.py <mods/classroom/icons>
import sys, os
out = sys.argv[1]
def svg(rows, pal, name):
    h = len(rows); w = max(len(r) for r in rows)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{pal[c]}"/>'
                    for y, r in enumerate(rows) for x, c in enumerate(r) if c in pal)
    open(os.path.join(out, name), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w*2}" height="{h*2}" shape-rendering="crispEdges">{rects}</svg>')
    return w, h
TOWER = [
 ".......h.......",
 ".......h.......",
 "......hRh......",
 ".....RRRRR.....",
 "....RRRRRRR....",
 "...RRRRRRRRR...",
 "..RRRRRRRRRRR..",
 ".EEEEEEEEEEEEE.",
 "..WWWWWWWWWWww.",
 "..WWWKKKKKWWww.",
 "..WWKFFFFFKWww.",
 "..WKFFFKFFFKww.",
 "..WKFFFKFFFKww.",
 "..WKFFFKKKFKww.",
 "..WKFFFFFFFKww.",
 "..WWKFFFFFKWww.",
 "..WWWKKKKKWWww.",
 "..WWWWWWWWWWww.",
 "..WWWWWWWWWWww.",
]
TREE = [
 "....GGGGGG....",
 "..GGGHHGGGGG..",
 ".GGHHGGGGHGGG.",
 "GGGGGGGGHHGGGG",
 "GGHGGGGGGGGHGG",
 "GHHGGGHGGGGGGG",
 ".GGGGHHGGGGHG.",
 "..GGGGGGGGGG..",
 "....GGTTGG....",
 "......TT......",
 "......TT......",
 ".....TTTT.....",
]
SUN = ["...Y...", ".Y.Y.Y.", "..YYY..", "YYYYYYY", "..YYY..", ".Y.Y.Y.", "...Y..."]
CLOUD = ["....CCC.......", "..CCCCCCC.CC..", ".CCCCCCCCCCCC.", "CCCCCCCCCCCCCC", ".DDDDDDDDDDDD."]
MOON = ["..MMM..", ".MM....", "MM.....", "MM.....", "MM.....", ".MM....", "..MMM.."]
STARS = ["....Y.........", "...YYY......Y.", "....Y.........", "..........Y...", ".Y.......YYY..", "..........Y...", "......Y......."]
PAL = {
 "day":    dict(R="#a8463c", h="#c8644f", E="#7a2f28", W="#fbf6ea", w="#e2d6bd", K="#33302a", F="#ffffff", G="#4f9a3c", H="#7cc35a", T="#7a5236", Y="#ffcf3f", C="#ffffff", D="#dbe8f2", M="#ffffff", P="#ffffff"),
 "night":  dict(R="#5a4b8f", h="#7464ad", E="#3a2f63", W="#565d86", w="#464c70", K="#1a1d30", F="#f5d67f", G="#1f4a33", H="#2f6a48", T="#3a2a22", Y="#f7e7a6", C="#ffffff", D="#ffffff", M="#f7e7a6", P="#ffffff"),
}
sizes = {}
for k, pal in PAL.items():
    sizes["tower"] = svg(TOWER, pal, f"tower-{k}.svg")
    sizes["tree"] = svg(TREE, pal, f"tree-{k}.svg")
    if k == "day": sizes["skyL"] = svg(SUN, pal, f"skyL-{k}.svg"); sizes["skyR"] = svg(CLOUD, pal, f"skyR-{k}.svg")
    if k == "night": svg(MOON, pal, f"skyL-{k}.svg"); svg(STARS, pal, f"skyR-{k}.svg")
print(sizes)
