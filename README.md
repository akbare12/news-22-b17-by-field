[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b17-by-field/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b17-by-field/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026

A one-page newspaper image summing up Sunday 22 November 2026: **48 stories
· 7 regions · 6 fields**, grouped by field with a colour bar (War & Security 18,
Politics 6, Sport 7, Markets 5, Society 8, Health & Science 4).

Lead stories: COP31 collapses with no deal in Antalya; Russia fires 186 drones
at Ukraine overnight, 161 shot down or jammed; Iran claims two US Patriot
radars were hit in Bahrain (labelled CLAIM — Bahrain denies a military
strike). A kanon number strip (186 / 161 / 720/9 / 98.79% / $120bn / 35% /
44h / 50 / 258 / 11,613), a "The Day in UTC" timeline, a world map with 48
numbered pins, and a red DATE CHECK box (wires read up to 23:00 UTC, LEFT OUT
with dates, NOT YET) close the page.

## How it is built

`draw.py` (Pillow, standard library only besides Pillow for drawing) draws
`entry.png` (1024×1024) from the story list in the file. `main.py` copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the PNG header,
dimensions and sha256 match. Nothing is ever written next to `main.py`.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

AP · Reuters · BBC · CNN · Guardian · France 24 · Al Jazeera · Yonhap ·
Anadolu · Detiknews · WHO · SpaceX. Certainty chips: CONFIRMED = 2+ outlets,
REPORTED = carried by the wires today, CLAIM = one side, unverified,
OFFICIAL = recorded result, FORECAST = not yet decided. Scenes are drawn
illustrations, not photographs.

SPDX-License-Identifier: MIT
