# RA achievement list
This is basically a "copy" of [RA Tracker](https://github.com/colossus-gaming/retroachievements-layout-manager)'s achievement list, but with some differences.
Basically, I was a bit disapponted that we couldn't resize that window, so I tried to see if I could do something similar with that change. This was mostly for personal use, but I ended up trying to make it a bit more user friendly.

## Changes
- Able to change window size so you can see more or less achievement per row, and more rows at once
- Can open more than one list; this can be useful for multisets

- Doesn't have any kind of animation
- Doesn't have any kind of autoscroll (and scrolling is only possible if hovering over an area without badges)

## Known issues
- This is meant to be used for 1 user only; if you open an achievement list and change the username/ULID, the program will start to update for that new user while keeping the old user's list. Right now I don't have any plans to change that.
- Right now the API documentation don't mention any way to get a subset list from their subset ID, so you need to use their game ID. The easiest way is to hover over a subset link and see their URL with the game ID.
