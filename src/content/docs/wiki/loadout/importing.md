---
title: "Importing from other plugins"
sidebar:
  order: 3
---

Keep the other plugin's folder in `plugins/`, then run `/kit import <source>`:

| Source | Reads |
|---|---|
| `essentials` | `plugins/Essentials/kits.yml` (or the `kits` section of its `config.yml`), item aliases from `items.json`, and each player's last claim from `userdata/` |
| `ultimatekits` | `plugins/UltimateKits/kit.yml` and each player's last claim from `data.yml` |

Items keep their amount, name, lore and enchantments; Essentials `@` serialized items and
UltimateKits NBT items are restored exactly. Armor goes to its armor slot, everything else fills the
inventory in order. Delays become cooldowns, a negative delay becomes a single use kit, `$` lines
become money rewards and `/` lines become console commands with `<player>`. Last claims are carried
over so running cooldowns keep going.

A kit whose id already exists in Loadout is skipped, so running the import twice does not duplicate
anything. Anything that could not be carried over is listed in the console after the import.
