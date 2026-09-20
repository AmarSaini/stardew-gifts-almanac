# Stardew Almanac

A static, mobile-friendly Stardew Valley cheatsheet (vanilla + Stardew Valley Expanded).
Tabs: **Gifts** (every villager's loved gifts and birthdays) and **Fishing** (season / weather / time / location filters).

## Structure
- `index.html` – generated; this is what gets deployed (Netlify publishes the repo root, no build step).
- `assets/` – all sprites, the backdrop and fonts, self-hosted (no runtime requests to the wikis).
- `build/template.html` – the page source (HTML/CSS/JS). Edit this, then rebuild.
- `build/build.py` – gift/villager data + assembles `index.html`:  `python3 build/build.py`
- `build/fish_data.py` – pulls the fish tables from the Stardew Valley Wiki into `build/fish.json`:  `python3 build/fish_data.py`

Sprites and data come from the Stardew Valley Wiki and the SVE wiki. Fan-made, not affiliated with ConcernedApe.
