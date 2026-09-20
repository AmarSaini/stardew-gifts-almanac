"""Fetch the vanilla Fish page from the Stardew Valley Wiki and normalize it to build/fish.json.
Run manually when the wiki data changes:  python3 build/fish_data.py"""
import json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://stardewvalleywiki.com/mediawiki/api.php?action=parse&page=Fish&prop=wikitext&format=json"
w = json.loads(subprocess.run(["curl", "-sL", "-m", "60", API], capture_output=True, text=True).stdout)["parse"]["wikitext"]["*"]

def tables(txt): return re.findall(r"\{\|.*?\n\|\}", txt, re.S)

def clean(c):
    c = re.sub(r"<!--.*?-->", "", c, flags=re.S)
    c = re.sub(r"<section[^>]*/>", "", c)
    c = re.sub(r"\{\{(?:Season|Weather inline|Weather)\|([^}|]+)[^}]*\}\}", r"\1", c)
    c = re.sub(r"\[\[File:[^\]]*\]\]", "", c)
    c = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", c)
    c = re.sub(r"<br\s*/?>", "\n", c)
    return c.strip()

def rows(tbl):
    out = []
    for r in re.split(r"\n\|-\s*\n", tbl)[1:]:
        cells = []
        for line in r.split("\n"):
            if line.startswith("|") and not line.startswith("|}"):
                body = line[1:]
                m = re.match(r'\s*(?:class|style|rowspan|colspan)="[^"]*"(?:\s+\w+="[^"]*")*\s*\|(?!\|)(.*)', body)
                cells.append(m.group(1) if m else body)
            elif cells:
                cells[-1] += "\n" + line
        if cells: out.append(cells)
    return out

def price(c):
    m = re.search(r"Qualityprice\|[^|]+\|(\d+)", c); return int(m.group(1)) if m else None

def used(c):
    bundles = [b.strip().title() for b in re.findall(r"\{\{Bundle\|([^}|]+)", c)]
    loved = re.findall(r"\{\{NPC\|([^|}]+)\|loved gift", c)
    rec = [n.strip() for n in re.findall(r"\{\{Name\|([^}|]+)", c) if n.strip() != "Quests Icon"]
    return {"bundles": bundles, "loved": loved, "recipes": rec, "pond": "Fish Pond" in c}

SEAS = ["Spring", "Summer", "Fall", "Winter"]
def seasons(c):
    c = re.sub(r"\(.*?\)", "", clean(c), flags=re.S)
    return SEAS if "All Seasons" in c else [s for s in SEAS if s in c]

def hr(t):
    m = re.match(r"(\d+)(?::(\d+))?\s*(am|pm)", t.strip(), re.I)
    return int(m.group(1)) % 12 + (12 if m.group(3).lower() == "pm" else 0) + (int(m.group(2)) / 60 if m.group(2) else 0)

def times(c):
    c = clean(c).replace("\n", " ")
    if not c or re.search(r"any\s*time|^any$", c, re.I): return [[6, 26]]
    out = []
    for a, b in re.findall(r"(\d+(?::\d+)?\s*[ap]m)\s*[–\-]\s*(\d+(?::\d+)?\s*[ap]m)", c, re.I):
        s, e = hr(a), hr(b)
        out.append([s, e + 24 if e <= s else e])
    return out or [[6, 26]]

def weather(c):
    c = clean(c).lower()
    if "rain" in c and "sun" in c: return "any"
    return "rain" if "rain" in c else "sun" if "sun" in c else "any"

def groups(locs):
    g = []
    for l in " | ".join(locs).lower().split(" | "):
        if "ginger" in l or "volcano" in l or "pirate" in l:
            g.append("Ginger Island"); continue  # Ginger Island waters are their own filter
        if "ocean" in l or "beach" in l or "saltwater" in l or "east pier" in l: g.append("Ocean")
        if "river" in l or "waterfall north of joja" in l or "freshwater" in l: g.append("River")
        if "mountain lake" in l or "freshwater" in l: g.append("Mountain Lake")
        if "forest pond" in l or "forest waterfall" in l or "arrowhead" in l or "freshwater" in l: g.append("Forest Pond")
        if "secret woods" in l: g.append("Secret Woods")
        if "sewer" in l: g.append("Sewers")
        if "mines" in l or "ghost" in l: g.append("Mines")
        if "desert" in l: g.append("Desert")
        if "swamp" in l: g.append("Witch's Swamp")
        if "bug lair" in l: g.append("Bug Lair")
        if "forest farm" in l: g.append("Farm")
        if "night market" in l: g.append("Night Market")
    return sorted(set(g), key=g.index)

def split_loc(text):
    """Legendary rows say 'East Pier on The Beach. Requires level 5 fishing.' -> (loc, note)."""
    t = text.replace("''", "").strip()
    m = re.match(r"(.+?[a-z\)])\.\s+(.*)$", t, re.S)
    return (m.group(1), m.group(2).strip()) if m else (t, "")

start = w.index("==Fishing Pole Fish==")
T = [rows(t) for t in tables(w[start:])[:6]]
out = []
for kind, rs in zip(["pole", "night", "legendary", "legendary2", "crab", "other"], T):
    for r in rs:
        name = clean(r[1])
        f = {"name": name, "kind": kind, "price": price(r[3])}
        if kind in ("pole", "legendary", "legendary2"):
            raw = clean(r[6]); note = ""
            if kind != "pole": raw, note = split_loc(raw)
            raw = raw.replace("''", "")
            locs = [x.strip() for x in re.split(r"\n|,", raw) if x.strip()]
            req = [x for x in locs if x.lower().startswith("requires")]
            locs = [x for x in locs if x not in req]
            if req: note = (note + " " + ". ".join(req)).strip()
            diff = clean(r[11]); dm = re.match(r"(\d+)\s*(\w+)?", diff)
            f.update(loc=locs, note=note, groups=groups(locs), time=times(r[7]), timeRaw=clean(r[7]).replace("\n", " "),
                     seasons=seasons(r[8]), seasonNote=re.sub(r"\s+", " ", clean(r[8]).replace("\n", " ")), weather=weather(r[9]),
                     size=clean(r[10]), diff=int(dm.group(1)) if dm else None, behavior=(dm.group(2) or "") if dm else "", xp=int(clean(r[12]) or 0))
            f["used"] = used(r[13]) if len(r) > 13 else used("")
        elif kind == "night":
            diff = clean(r[7]); dm = re.match(r"(\d+)\s*(\w+)?", diff)
            f.update(loc=["Night Market submarine"], note="Winter 15–17, 5pm–2am", groups=["Night Market"], time=[[17, 26]], timeRaw="5pm – 2am",
                     seasons=["Winter"], seasonNote="Winter 15–17", weather="any", size=clean(r[6]), diff=int(dm.group(1)), behavior=dm.group(2) or "", xp=int(clean(r[8]) or 0), used=used(r[9]) if len(r) > 9 else used(""))
        elif kind == "crab":
            loc = clean(r[6])
            f.update(loc=[loc], groups=["Ocean"] if loc == "Ocean" else ["River", "Mountain Lake", "Forest Pond"], trap=clean(r[7]), size=clean(r[9]), used=used(r[10]) if len(r) > 10 else used(""))
        else:
            locs = [x.strip("* ").strip() for x in clean(r[4]).split("\n") if x.strip()]
            f.update(loc=locs, groups=groups(locs), used=used(r[5]))
        if name == "Green Algae": f["groups"] = ["River", "Mountain Lake", "Forest Pond"]  # 'everywhere but the ocean'
        out.append(f)

# legendary rows re-listed in later sections: keep first occurrence only
seen, dedup = set(), []
for f in out:
    if f["name"] in seen: continue
    seen.add(f["name"]); dedup.append(f)
json.dump(dedup, open(os.path.join(ROOT, "build", "fish.json"), "w"), indent=1, ensure_ascii=False)
print(len(dedup), "entries")
