---
title: "Loadout"
description: "Kits with progression for Paper and Folia."
sidebar:
  order: 0
  label: "Introduction"
---

Kits for Paper and Folia 1.21: cooldowns, prices, conditions, mastery tiers, streaks, collection,
a featured kit, giftable kit vouchers, trying gear on before claiming, animated opening ceremonies
and a full in-game editor. Fourteen example kits ship with the plugin.

## Installation

1. Drop `Loadout.jar` into `plugins/`.
2. Start the server: `config.yml`, `kits.yml`, the `lang/` folder and the `loadout.db` database
   are created in `plugins/Loadout/`.

Optional: Vault (paid kits and money rewards), PlaceholderAPI (`%loadout_...%` placeholders and
conditions), Lootrift or any other crate plugin (keys as rewards).

## Languages

`config.yml` holds `language: en`. English and French ship with the plugin (`en`, `fr`).

- `lang/messages_<language>.yml` holds the chat messages.
- `lang/<language>.yml` holds the menu and log texts, and can be edited to reword any of them.
- On first start, `kits.yml` is written in the configured language.
