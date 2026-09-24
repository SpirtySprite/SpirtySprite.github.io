---
title: "Commands and permissions"
sidebar:
  order: 1
---

## Commands

| Command | Effect |
|---|---|
| `/kit` | kit menu |
| `/kit <kit>` | claims a kit |
| `/kit preview <kit>` | contents preview |
| `/kit tryon <kit>` | tries the gear on before claiming it |
| `/kit gift <player> <kit>` | gifts a kit |
| `/kit share <kit>` | posts a clickable preview of the kit in chat, once every 30 seconds |
| `/kit all` | claims every available kit |
| `/kit collection`, `/kit mastery`, `/kit history` | progression and history |
| `/kit admin` | admin menu |
| `/kit create <id>`, `/kit edit <kit>`, `/kit capture <kit>` | create, edit, capture your inventory into a kit |
| `/kit delete <kit>`, `/kit stock <kit>` | delete, manage the stock |
| `/kit give <player> <kit>`, `/kit voucher <player> <kit>` | give a kit or a voucher |
| `/kit reset <player> <kit\|all>`, `/kit player <player>` | a player's cooldowns |
| `/kit ceremony ...` | test an opening ceremony |
| `/kit reload` | reloads `kits.yml` |

The French subcommands (`apercu`, `offrir`, `tout`, `creer`, ...) keep working.

## Permissions

| Permission | Default | Effect |
|---|---|---|
| `loadout.kit.use` | everyone | `/kit` and claiming kits |
| `loadout.kit.gift` | everyone | gifting a kit |
| `loadout.admin.kits` | op | administration |
| `loadout.kit.bypass` | no | bypasses cooldown, price, conditions and permissions |
| `loadout.kit.bypass.cooldown`, `.cost`, `.requirements`, `.permission` | no | each bypass on its own |
| `loadout.alerts.kits` | op | configuration alerts |
