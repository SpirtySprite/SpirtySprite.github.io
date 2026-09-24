---
title: "Lootrift"
description: "Animated crates for Paper and Folia."
sidebar:
  order: 0
  label: "Introduction"
---

Animated crates for Paper and Folia 1.21: virtual and physical keys, 12 opening animations, bulk
opening, particle effects around crate blocks, per player holograms, ModelEngine models, opening
milestones, a pity system, unique rewards, win history and a full in-game editor.

## Installation

1. Drop `Lootrift.jar` into `plugins/`.
2. Start the server: `config.yml`, `crates.yml` (four example crates) and the `lang/` folder are
   created in `plugins/Lootrift/`, along with the `lootrift.db` database.
3. Place a crate from `/crate admin`.

Optional: Vault (buying keys and money rewards), PlaceholderAPI, ModelEngine (crates as 3D models).

## Languages

`config.yml` holds `language: en`. English and French ship with the plugin (`en`, `fr`).

- `lang/messages_<language>.yml` holds the chat messages.
- `lang/<language>.yml` holds the menu and log texts, and can be edited to reword any of them.
- On first start, `crates.yml` is written in the configured language.

## Usage

Right click a placed crate to open it with a key, left click to preview its rewards. While
sneaking, bulk opening uses every key at once with a dedicated animation. Rewards that do not fit
in the inventory drop on the ground.
