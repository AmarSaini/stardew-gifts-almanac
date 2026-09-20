"""Fetch the Stardew Valley Expanded fish table (SVE wiki) -> build/sve_fish.json, and download missing icons.
Run manually:  python3 build/sve_fish_data.py"""
import json, os, re, subprocess
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
API = "https://stardew-valley-expanded.fandom.com/api.php"

def curl(url): return subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, url], capture_output=True).stdout
w = json.loads(curl(API + "?action=parse&page=Fish&prop=wikitext&format=json"))["parse"]["wikitext"]["*"]
sec = w[w.index("== Types of Fish"):w.index("==Fish Ponds==")]

def cells(block):
    """Top-level {{TableRow|...}} cells, matching nested braces (cells can span lines)."""
    out, i = [], 0
    while True:
        i = block.find("{{TableRow|", i)
        if i < 0: return out
        j, depth = i + 2, 1
        while depth and j < len(block):
            if block.startswith("{{", j): depth += 1; j += 2
            elif block.startswith("}}", j): depth -= 1; j += 2
            else: j += 1
        body = block[i + len("{{TableRow|"):j - 2]
        body = re.sub(r"^data-sort-value=[^|]*\|", "", body)
        body = re.sub(r"\|data-sort-value=.*$", "", body, flags=re.S)
        out.append(body); i = j

def clean(c):
    c = re.sub(r"<nowiki>.*?</nowiki>", "", c)
    c = re.sub(r"\{\{icon\|[^}]*\}\}", "", c)
    c = re.sub(r"\[\[File:[^\]]*\]\]", "", c)
    c = re.sub(r"\[https?://\S+ ([^\]]+)\]", r"\1", c)
    c = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", c)
    c = re.sub(r"<br\s*/?>", "\n", c); c = re.sub(r"<[^>]+>", "", c); c = re.sub(r"\{\{[^}]*\}\}", "", c)
    return c.strip()

SEAS = ["Spring", "Summer", "Fall", "Winter"]
def hr(t):
    m = re.match(r"(\d+)(?::(\d+))?\s*(am|pm)", t.strip(), re.I)
    return int(m.group(1)) % 12 + (12 if m.group(3).lower() == "pm" else 0) + (int(m.group(2)) / 60 if m.group(2) else 0)
def times(c):
    out = []
    for a, b in re.findall(r"(\d+(?::\d+)?\s*[ap]m)\s*[–\-]\s*(\d+(?::\d+)?\s*[ap]m)", c, re.I):
        s, e = hr(a), hr(b); out.append([s, e + 24 if e <= s else e])
    return out or [[6, 26]]
def weather(c):
    c = c.lower()
    if "any" in c or ("sun" in c and "rain" in c): return "any"
    return "rain" if ("rain" in c or "storm" in c) else "sun" if "sun" in c else "any"

SHARED = {"mutant bug lair": ["Bug Lair"], "witch swamp": ["Witch's Swamp"], "the beach": ["Ocean"], "the mountain": ["Mountain Lake"], "the sewers": ["Sewers"], "pelican town": ["River"], "beach": ["Ocean"], "ocean": ["Ocean"], "mountain": ["Mountain Lake"], "town": ["River"], "forest": ["River", "Forest Pond"],
          "secret woods": ["Secret Woods"], "sewers": ["Sewers"], "swamp": ["Witch's Swamp"], "bug lair": ["Bug Lair"], "farm": ["Farm"],
          "ginger island": ["Ginger Island"], "fable reef": ["Ginger Island"]}
def groups(locs):
    g = []
    for l in locs:
        k = l.lower().strip("* ")
        hit = next((v for key, v in SHARED.items() if k == key or k.startswith(key + " (")), None)
        g += hit or ["Expanded areas"]
    return sorted(set(g), key=g.index)

out = []
for block in re.split(r"\{\{TableRowStart\}\}", sec)[1:]:
    c = cells(block)
    if len(c) < 13: continue
    name = clean(c[1]); img = re.search(r"\[\[File:([^|\]]+)", c[0]).group(1).replace("_", " ")
    price = re.search(r"(\d+)g", c[3]); locraw = clean(c[6])
    notes = []
    if "**" in locraw: notes.append("Requires seeing the Kittyfish introductory event.")
    elif "*" in locraw: notes.append("Requires completing the expanded Joja route storyline.")
    locs = [re.sub(r"[*]+", "", x.split("|")[-1]).replace("}}", "").replace("]]", "").strip() for x in re.split(r"\n|,", locraw) if x.strip()]
    s = clean(c[7]); seasons = SEAS if re.search(r"\ball\b|\bany\b", s, re.I) else [x for x in SEAS if x in s]
    minlvl = re.sub(r"\D", "", clean(c[10])); dm = re.match(r"(\d+)\s*(\w+)?", clean(c[11]))
    if minlvl and int(minlvl) > 0: notes.append(f"Requires fishing level {int(minlvl)}.")
    xp = re.sub(r"\D", "", clean(c[12]))
    used = clean(c[13]) if len(c) > 13 else ""
    recipes = [r.strip() for r in re.findall(r"\[\[(?!File:)([^\]|]+)", c[13])] if len(c) > 13 else []
    out.append({"name": name, "kind": "sve", "img": img, "price": int(price.group(1)) if price else None, "loc": locs, "groups": groups(locs),
                "note": " ".join(notes), "time": times(clean(c[8])), "timeRaw": clean(c[8]), "seasons": seasons, "seasonNote": re.sub(r"\s+", " ", s.replace("\n", " ")),
                "weather": weather(clean(c[9])), "size": "", "diff": int(dm.group(1)) if dm else None, "behavior": (dm.group(2) or "").lower() if dm else "",
                "xp": int(xp) if xp else None, "used": {"bundles": [], "loved": [], "recipes": recipes, "pond": False}})
json.dump(out, open(os.path.join(ROOT, "build", "sve_fish.json"), "w"), indent=1, ensure_ascii=False)
print(len(out), "SVE fish")

# ---- icons (fandom serves some as WebP under a .png name -> convert)
def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
need = [f for f in out if not os.path.exists(f"{ROOT}/assets/items/{slug(f['name'])}.png")]
urls = {}
for i in range(0, len(need), 40):
    q = "|".join("File:" + f["img"] for f in need[i:i + 40])
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "-G", API, "--data-urlencode", "action=query", "--data-urlencode", "titles=" + q,
                        "--data-urlencode", "prop=imageinfo", "--data-urlencode", "iiprop=url", "--data-urlencode", "format=json"], capture_output=True).stdout
    for p in json.loads(r)["query"]["pages"].values():
        if p.get("imageinfo"): urls[p["title"][5:]] = p["imageinfo"][0]["url"]
def dl(f):
    u = urls.get(f["img"]) or urls.get(f["img"].replace("_", " "))
    if not u: return f["name"], "no url"
    dest = f"{ROOT}/assets/items/{slug(f['name'])}.png"
    subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "-o", dest, u.replace(" ", "%20")])
    try:
        from PIL import Image
        im = Image.open(dest)
        if im.format != "PNG": im.convert("RGBA").save(dest, "PNG", optimize=True)
    except Exception as e: return f["name"], f"bad image: {e}"
    return f["name"], None
with ThreadPoolExecutor(6) as ex:
    bad = [r for r in ex.map(dl, need) if r[1]]
print("icons downloaded:", len(need) - len(bad), "| problems:", bad)
