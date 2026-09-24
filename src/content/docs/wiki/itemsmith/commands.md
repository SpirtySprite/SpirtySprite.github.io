---
title: "Commands and permissions"
sidebar:
  order: 1
---

## Commands

| Command | Effect |
|---|---|
| `/item` | opens the editor for the item in your hand |
| `/item edit <field> ...` | edits a field directly (see `/item help`) |
| `/item undo` | undoes the last change |
| `/item info` | summarises the item in your hand |

Aliases: `/itemedit`, `/ie`, `/itemeditor`, `/edititem`.

`/item edit` fields: `name`, `lore`, `enchant`, `flag`, `attribute`, `amount`, `maxstack`, `damage`,
`maxdamage`, `repaircost`, `enchantable`, `unbreakable`, `glider`, `fireresistant`, `hidetooltip`,
`glint`, `rarity`, `model`, `itemmodel`, `tooltipstyle`, `type`, `color`, `skull`, `texture`, `potion`,
`trim`, `book`.

## Permissions

| Permission | Default | Effect |
|---|---|---|
| `itemsmith.admin.item` | op | use `/item` |
