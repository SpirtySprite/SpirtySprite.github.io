---
title: "Importing from other plugins"
sidebar:
  order: 4
---

Keep the other plugin's folder in `plugins/`, then run `/crate import <source>`:

| Source | Reads |
|---|---|
| `crazycrates` | `plugins/CrazyCrates/crates/*.yml` (current and legacy prize formats) and virtual keys from `data.yml` |
| `excellentcrates` | `plugins/ExcellentCrates/crates/*.yml` and virtual keys from its SQLite database |

Each crate becomes a Lootrift crate with the same id, its name, icon, key item and rewards. Weights
keep their proportions and a rarity is picked from each reward's share unless the source names one.
Reward commands are kept, `%player%` becomes `<player>`. Key balances are added to the players'
Lootrift keys.

A crate whose id already exists in Lootrift is skipped, so running the import twice does not
duplicate anything. Anything that could not be carried over (items from other item plugins, prizes
with several items, MySQL key storage) is listed in the console after the import.
