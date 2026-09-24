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

Rarities: `commun`, `peu-commun`, `rare`, `epique`, `legendaire`, `mythique`.

Opening animations: `csgo`, `roulette`, `cascade`, `roue`, `pulse`, `tombola`, `eclair`,
`horloge`, `vague`, `zoom`, `mosaique`, `instant`.

Bulk animations: `domino`, `inverse`, `avalanche`, `vague`, `spirale`, `explosion`, `implosion`,
`miroir`, `rideau`, `diagonale`, `scanner`, `rafale`.

Reward commands accept `<player>`. Every opening is written to `logs/caisses.log`.

`/crate reload` rereads `config.yml`, the language files and `crates.yml`. Changing `language`
takes full effect after a restart.
