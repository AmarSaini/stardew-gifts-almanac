import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def slug(n): return re.sub(r"[^a-z0-9]+","-",n.lower()).strip("-")

V,S="vanilla","sve"
B,BE,T="bachelor","bachelorette","villager"
DATA=[
 ("Abigail",BE,V,["Amethyst","Banana Pudding","Blackberry Cobbler","Chocolate Cake","Pumpkin","Spicy Eel"]),
 ("Alex",B,V,["Complete Breakfast","Salmon Dinner"]),
 ("Caroline",T,V,["Fish Taco","Green Tea","Summer Spangle","Tropical Curry"]),
 ("Clint",T,V,["Any Gem (except Diamond)","Artichoke Dip","Fiddlehead Risotto"]),
 ("Demetrius",T,V,["Bean Hotpot","Ice Cream","Rice Pudding"]),
 ("Dwarf",T,V,["Any Gem (except Diamond)"]),
 ("Elliott",B,V,["Crab Cakes","Lobster","Pomegranate","Tom Kha Soup"]),
 ("Emily",BE,V,["Cloth","Parrot Egg","Survival Burger","Any Gem (except Diamond)"]),
 ("Evelyn",T,V,["Beet","Chocolate Cake","Diamond","Fairy Rose","Raisins","Stuffing","Tulip"]),
 ("George",T,V,["Fried Mushroom","Any Flower (except Poppy)"]),
 ("Gus",T,V,["Diamond","Escargot","Fish Taco","Orange","Tropical Curry"]),
 ("Haley",BE,V,["Fruit Salad","Pink Cake","Sunflower"]),
 ("Harvey",B,V,["Coffee","Pickles","Super Meal","Truffle Oil","Wine"]),
 ("Jas",T,V,["Fairy Rose","Pink Cake","Plum Pudding","Any Vegetable (except Hops/Wheat)"]),
 ("Jodi",T,V,["Chocolate Cake","Crispy Bass","Diamond","Eggplant Parmesan","Fried Eel","Pancakes","Rhubarb Pie","Vegetable Medley"]),
 ("Kent",T,V,["Fiddlehead Risotto","Roasted Hazelnuts"]),
 ("Krobus",T,V,["Diamond","Pumpkin","Seafoam Pudding","Void Mayonnaise"]),
 ("Leah",BE,V,["Goat Cheese","Poppyseed Muffin","Salad","Stir Fry","Truffle","Vegetable Medley","Wine"]),
 ("Leo",B,V,["Poi"]),
 ("Lewis",T,V,["Autumn's Bounty","Glazed Yams","Green Tea","Vegetable Medley"]),
 ("Linus",T,V,["Blueberry Tart","Dish O' The Sea","Yam"]),
 ("Marnie",T,V,["Diamond","Farmer's Lunch","Pink Cake","Pumpkin Pie"]),
 ("Maru",BE,V,["Cheese Cauliflower","Diamond","Miner's Treat","Pepper Poppers","Radioactive Bar","Rhubarb Pie"]),
 ("Pam",T,V,["Beer","Glazed Yams","Mead","Pale Ale","Parsnip","Piña Colada","Parsnip Soup"]),
 ("Penny",BE,V,["Diamond","Emerald","Poppy","Poppyseed Muffin","Red Plate","Roots Platter","Tom Kha Soup"]),
 ("Pierre",T,V,["Fried Calamari"]),
 ("Robin",T,V,["Goat Cheese","Peach","Spaghetti"]),
 ("Sam",B,V,["Maple Bar","Pizza","Any Vegetable (except Hops/Wheat)"]),
 ("Sandy",T,V,["Crocus","Mango Sticky Rice","Sweet Pea"]),
 ("Sebastian",B,V,["Frog Egg","Obsidian","Pumpkin Soup","Sashimi","Void Egg"]),
 ("Shane",B,V,["Beer","Pepper Poppers","Pizza"]),
 ("Vincent",T,V,["Cranberry Candy","Frog Egg","Ginger Ale","Pink Cake","Snail"]),
 ("Willy",T,V,["Catfish","Diamond","Gold Bar","Iridium Bar","Mead","Octopus","Sea Cucumber","Sturgeon"]),
 ("Wizard",T,V,["Book of Mysteries","Solar Essence","Super Cucumber","Void Essence"]),
 # Stardew Valley Expanded
 ("Andy",B,S,["Beer","Butterfish","Farmer's Lunch","Mead","King Salmon","Glazed Butterfish","Pale Ale"]),
 ("Claire",BE,S,["Apricot","Green Tea","Energy Tonic","Sunflower","Bruschetta","Ocean Stone","Glazed Butterfish"]),
 ("Gunther",T,S,["Bean Hotpot","Petrified Slime","Salmon Dinner","Elvish Jewelry","Ornamental Fan","Dinosaur Egg","Rare Disc","Ancient Sword","Dwarvish Helm","Dwarf Gadget","Golden Mask","Golden Relic","Star Shards"]),
 ("Lance",T,S,["Tropical Curry","Aged Blue Moon Wine","Golden Pumpkin","Swirl Stone","Void Shard","Galaxy Soul","Daggerfish","Torpedo Trout","Gemfish","Monster Mushroom","Green Mushroom"]),
 ("Marlon",T,S,["Roots Platter","Slime Egg","Aged Blue Moon Wine","Armor Elixir","Hero Elixir","Haste Elixir","Void Delight","Life Elixir"]),
 ("Martin",T,S,["Juice","Ice Cream","Big Bark Burger"]),
 ("Morgan",T,S,["Iridium Bar","Void Egg","Void Mayonnaise","Frog"]),
 ("Morris",T,S,["Aged Blue Moon Wine","Chowder","Golden Pumpkin","Lobster Bisque","Pearl","Prismatic Shard","Rabbit's Foot","Star Shards","Truffle Oil"]),
 ("Olivia",T,S,["Aged Blue Moon Wine","Blue Moon Wine","Wine","Golden Mask","Golden Relic","Chocolate Cake","Pink Cake"]),
 ("Scarlett",T,S,["Goat Cheese","Duck Feather","L. Goat Milk","Honey","Cherry","Maple Syrup","Glazed Yams","Pink Cake","Chocolate Cake","Jade","Rabbit's Foot"]),
 ("Sophia",T,S,["Grampleton Orange Chicken","Fairy Stone","Puppyfish","Fairy Rose"]),
 ("Susan",T,S,["Blackberry Cobbler","Blueberry Tart","Chocolate Cake","Cookie","Cranberry Candy","Ice Cream","Maple Bar","Pancakes","Pearl","Pink Cake","Poppyseed Muffin","Pumpkin Pie","Rhubarb Pie"]),
 ("Victor",T,S,["Battery Pack","Duck Feather","Lunarite","Spaghetti","Aged Blue Moon Wine","Blue Moon Wine","Butterfish"]),
]
BIRTHDAYS = {"Abigail": ["Fall", 13], "Alex": ["Summer", 13], "Andy": ["Spring", 23], "Caroline": ["Winter", 7], "Claire": ["Fall", 8], "Clint": ["Winter", 26], "Demetrius": ["Summer", 19], "Dwarf": ["Summer", 22], "Elliott": ["Fall", 5], "Emily": ["Spring", 27], "Evelyn": ["Winter", 20], "George": ["Fall", 24], "Gunther": ["Winter", 12], "Gus": ["Summer", 8], "Haley": ["Spring", 14], "Harvey": ["Winter", 14], "Jas": ["Summer", 4], "Jodi": ["Fall", 11], "Kent": ["Spring", 4], "Krobus": ["Winter", 1], "Lance": ["Spring", 8], "Leah": ["Winter", 23], "Leo": ["Summer", 26], "Lewis": ["Spring", 7], "Linus": ["Winter", 3], "Marlon": ["Winter", 19], "Marnie": ["Fall", 18], "Martin": ["Summer", 6], "Maru": ["Summer", 10], "Morgan": ["Fall", 7], "Morris": ["Spring", 2], "Olivia": ["Spring", 15], "Pam": ["Spring", 18], "Penny": ["Fall", 2], "Pierre": ["Spring", 26], "Robin": ["Fall", 21], "Sam": ["Summer", 17], "Sandy": ["Fall", 15], "Scarlett": ["Summer", 7], "Sebastian": ["Winter", 10], "Shane": ["Spring", 20], "Sophia": ["Winter", 27], "Susan": ["Fall", 28], "Victor": ["Summer", 23], "Vincent": ["Spring", 10], "Willy": ["Summer", 24], "Wizard": ["Winter", 17]}
UNIVERSAL=["Golden Pumpkin","Magic Rock Candy","Pearl","Prismatic Shard","Rabbit's Foot"]
ANY={"Any Gem (except Diamond)":"Emerald","Any Flower (except Poppy)":"Tulip","Any Vegetable (except Hops/Wheat)":"Parsnip"}

def has(kind,name): return os.path.exists(f"{ROOT}/assets/{kind}/{slug(name)}.png")
items={}; chars={}; missing=[]
for name,_,_,gifts in DATA:
    if has("characters",name): chars[name]=f"assets/characters/{slug(name)}.png"
    else: missing.append(("char",name))
    for g in gifts+[] :
        k=ANY.get(g,g)
        if has("items",k): items[k]=f"assets/items/{slug(k)}.png"
        else: missing.append(("item",k))
for g in UNIVERSAL:
    if has("items",g): items[g]=f"assets/items/{slug(g)}.png"
    else: missing.append(("item",g))
print("missing:",sorted(set(missing)))
tpl=open(f"{ROOT}/build/template.html").read()
out=tpl.replace("/*ASSETS*/",json.dumps({"characters":chars,"items":items},ensure_ascii=False)).replace("/*DATA*/",json.dumps(DATA,ensure_ascii=False)).replace("/*BDAYS*/",json.dumps(BIRTHDAYS))
open(f"{ROOT}/index.html","w").write(out)
print(len(chars),"portraits",len(items),"icons")
