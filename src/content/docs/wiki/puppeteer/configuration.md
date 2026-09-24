---
title: "Configuring NPCs"
sidebar:
  order: 1
---

## Global settings

| Key | Default | Effect |
|---|---|---|
| `settings.view-distance` | `48` | display distance in blocks, between 8 and 256 |
| `settings.default-cooldown-ms` | `500` | delay between two clicks when an NPC does not set one |
| `settings.skin-cache-minutes` | `30` | how long downloaded skins are kept |
| `settings.debug` | `false` | verbose FoliaNPC logging |
| `settings.nametag-style` | vanilla | default style of the lines above NPCs, same keys as `nametag-style` |

## NPC options

Every NPC lives under `npcs.<id>`, with an id made of lowercase letters, digits, `_` and `-`. Only
`location.world` is required.

| Key | Default | Effect |
|---|---|---|
| `enabled` | `true` | `false` keeps the definition without showing the NPC |
| `name` | the id | internal name, used by `%npc%` |
| `type` | `PLAYER` | `PLAYER` or any living entity (`VILLAGER`, `CAT`, `ZOMBIE`...) |
| `location` | | `world`, `x`, `y`, `z`, `yaw`, `pitch` |
| `skin` | none | player name, `https://` link, `mirror`, or a `value`/`signature`, `url`, `player`, `mirror` section |
| `nametag` | none | lines above the NPC, MiniMessage or `&` codes, per player placeholders |
| `nametag-refresh-ticks` | `0` | refreshes the lines for placeholders that change |
| `nametag-style.background` | `#000000` | line background colour, `#RRGGBB` or a name (`black`, `dark_purple`...) |
| `nametag-style.background-opacity` | `25` | background opacity in percent, `0` removes it |
| `nametag-style.text-opacity` | `100` | text opacity in percent, below `10` the text disappears |
| `nametag-style.shadow` | `false` | text shadow |
| `nametag-style.see-through` | `false` | lines visible through blocks |
| `look-at-players` | `true` | the NPC follows the nearest player with its eyes |
| `view-distance` | global | distance for this NPC, `0` uses the global value |
| `cooldown-ms` | global | delay between two clicks from the same player |
| `permission` | none | only players with the permission see the NPC |
| `pose` | `STANDING` | `STANDING`, `CROUCHING`, `SLEEPING`, `SWIMMING`, `SITTING`, `FALL_FLYING`, `DYING` |
| `baby` | `false` | baby version of mobs |
| `variant` | | number (rabbit, parrot, axolotl, horse) or name (`black` for a cat, a wolf, a frog) |
| `villager.profession`, `villager.type`, `villager.level` | | villager appearance, level 1 to 5 |
| `appearance.glowing`, `appearance.glow-color` | `false` | glowing outline and its colour (`aqua`, `gold`...) |
| `appearance.invisible` | `false` | invisible body, equipment and name still visible |
| `appearance.scale` | `1.0` | size between 0.1 and 16 |
| `appearance.skin-layers` | `true` | outer skin layers |
| `appearance.collidable` | `true` | players can push against the NPC |
| `appearance.show-in-tab` | `false` | appears in the player list |
| `appearance.nametag-visible` | auto | forces the vanilla name to show |
| `equipment.<slot>` | | material or full item (`material`, `name`, `lore`, `glow`, `item-model`...) for `hand`, `off-hand`, `head`, `chest`, `legs`, `feet`, `body` |
| `actions` | | list of actions run on click |
