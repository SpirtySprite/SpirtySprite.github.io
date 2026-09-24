---
title: "Configuration"
sidebar:
  order: 2
---

`crates.yml` holds the global settings (`settings`) and one section per crate under `crates`.
Everything can also be set from `/crate admin`, which rewrites the file.

| Crate key | Effect |
|---|---|
| `name`, `icon`, `key` | name, menu icon and key appearance |
| `block` or `model` | placed block or ModelEngine model (`blueprint`, animations, scale) |
| `animation`, `bulk-animation` | single and bulk opening animation |
| `rolls` | number of rewards per opening |
| `price`, `daily-key` | key price through Vault, free daily key |
| `permission`, `cooldown-seconds` | access and delay between two openings |
| `pity` | reward of a minimum rarity guaranteed after `after` unlucky openings |
| `milestones` | money bonus and message after a number of openings, repeatable |
| `hologram` | lines above the crate |
| `effects` | particles around the block |
| `rewards` | rewards: item, `weight`, `rarity`, `min-amount`, `max-amount`, `money`, `commands`, `unique`, `announce` |

## Seasonal crates

A crate can open only between two dates, for events or limited seasons:

```yaml
crates:
  christmas:
    season:
      from: 2026-12-24
      until: 2026-12-27 00:00
```

Dates are `yyyy-MM-dd` or `dd/MM/yyyy`, with an optional `HH:mm`. Outside the window the crate
refuses to open and tells the player when it opens or when it closed. Times use
`settings.timezone` (for example `Europe/Paris`), or the server's zone when it is not set.

## Reward types

A reward can combine an item, money, experience and commands:

```yaml
rewards:
  ruby:
    custom-item: "itemsadder:ruby"
    weight: 20
    rarity: rare
  pouch:
    material: GOLD_NUGGET
    give-item: false
    money: "100-500"
    xp: 30
  rank:
    material: NAME_TAG
    give-item: false
    commands:
      - "lp user <player> parent addtemp vip 7d"
```

- `custom-item` takes an item from `itemsadder:<id>`, `nexo:<id>`, `oraxen:<id>` or
  `mmoitems:<type>:<id>`. The plugin only needs to be installed; if the item is missing, the console
  says so and the reward falls back to its `material`.
- `money` is a fixed amount or a range. A range is drawn each time, and the chat shows the amount won.
- `xp` gives experience points.
- `commands` run from the console with `<player>` replaced, so any plugin can be a reward:
  LuckPerms ranks and permissions, other crate keys, titles.

Rarities: `commun`, `peu-commun`, `rare`, `epique`, `legendaire`, `mythique`.

Opening animations: `csgo`, `roulette`, `cascade`, `roue`, `pulse`, `tombola`, `eclair`,
`horloge`, `vague`, `zoom`, `mosaique`, `instant`.

Bulk animations: `domino`, `inverse`, `avalanche`, `vague`, `spirale`, `explosion`, `implosion`,
`miroir`, `rideau`, `diagonale`, `scanner`, `rafale`.

Reward commands accept `<player>`. Every opening is written to `logs/caisses.log`.

`/crate reload` rereads `config.yml`, the language files and `crates.yml`. Changing `language`
takes full effect after a restart.
