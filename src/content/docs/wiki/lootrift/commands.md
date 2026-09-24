---
title: "Commands and permissions"
sidebar:
  order: 1
---

## Commands

| Command | Effect |
|---|---|
| `/crate admin` | admin menu: create, edit, place and remove crates |
| `/crate apercu <crate>` | reward preview |
| `/crate ouvrir <crate>` | opens a crate without a block |
| `/crate historique` | win history |
| `/crate give <crate>` | gives you the crate block to place |
| `/crate reload` | reloads `crates.yml` |
| `/cle give <player> <crate> [amount]` | gives virtual keys |
| `/cle take`, `/cle set` | removes or sets keys |
| `/cle physique <player> <crate> [amount]` | gives keys as items |
| `/cle all <crate> [amount]` | gives keys to every online player |

`/cle` is also available as `/key` and `/keys`, `/crate` as `/crates`.

## Permissions

| Permission | Default | Effect |
|---|---|---|
| `lootrift.admin.crates` | op | `/crate` and `/cle` |
| `lootrift.crates.bypass-cooldown` | op | bypasses the delay between two openings |
| `lootrift.alerts.caisses` | op | alerts for undelivered rewards |
