---
title: "Importing from other plugins"
sidebar:
  order: 4
---

Keep the other plugin's folder in `plugins/`, then run `/npc import <source>`:

| Source | Reads |
|---|---|
| `citizens` | `plugins/Citizens/saves.yml`: name, type, location, skin, look close and command trait |
| `fancynpcs` | `plugins/FancyNpcs/npcs.yml`: display name, type, location, skin, glow, scale, equipment and actions |
| `znpcsplus` | `plugins/ZNPCsPlus/data/*.yml`: hologram lines, type, location, skin, look and actions |

Commands become `CONSOLE_COMMAND` or `PLAYER_COMMAND` actions on the same click, messages become
`MESSAGE` actions, FancyNpcs waits become action delays, and player placeholders become `%player%`.
Imported NPCs are enabled right away, so disable the old plugin to avoid seeing each NPC twice.

An NPC whose id already exists in Puppeteer is skipped, so running the import twice does not
duplicate anything. Anything that could not be carried over (costs, op commands, random actions,
ZNPCsPlus database storage) is listed in the console after the import.
