---
title: "Click actions"
sidebar:
  order: 2
---

Every action picks its click and its type. Actions on the same click run in order; `delay` counts in
ticks from the click. A `TAKE_MONEY` or `REQUIRE_PERMISSION` action that fails cancels all the
following ones.

| Key | Default | Effect |
|---|---|---|
| `click` | `RIGHT` | `LEFT`, `RIGHT` or `BOTH` |
| `sneak` | any | `true` sneaking only, `false` standing only |
| `type` | | see below |
| `value` | | text, command, key or destination depending on the type; a list gives several lines |
| `delay` | `0` | wait in ticks before the action |
| `permission` | none | action skipped without the permission, the following ones continue |
| `deny-message` | | message when the permission or the payment is missing |
| `amount` | | amount, effect level or number of particles |
| `duration` | `60` or `200` | ticks a title stays or an effect lasts |
| `subtitle`, `fade-in`, `fade-out` | `10`, `20` | title settings |
| `volume`, `pitch` | `1.0` | sound settings |

| Type | Value | Effect |
|---|---|---|
| `MESSAGE` | text | message to the player |
| `BROADCAST` | text | message to the whole server |
| `ACTIONBAR` | text | player's action bar |
| `TITLE` | text | title, with `subtitle` |
| `PLAYER_COMMAND` | command | run by the player |
| `CONSOLE_COMMAND` | command | run by the console |
| `SOUND` | `entity.player.levelup` or `ENTITY_PLAYER_LEVELUP` | sound for the player, resource pack sounds accepted |
| `TELEPORT` | `world x y z [yaw pitch]` | teleport |
| `SERVER` | server name | sends the player to another proxy server |
| `EFFECT` | `speed`, `haste`... | potion effect, `amount` for the level |
| `PARTICLE` | `HAPPY_VILLAGER`, `HEART`... | particles without extra data, visible to the player |
| `GIVE_MONEY` | optional message | credits `amount` |
| `TAKE_MONEY` | optional message | debits `amount`, otherwise blocks the rest |
| `REQUIRE_PERMISSION` | permission | blocks the rest without the permission |
| `SWING` | | the NPC swings its arm |

Texts accept `%player%`, `%npc%` and, when PlaceholderAPI is installed, all of its placeholders.
