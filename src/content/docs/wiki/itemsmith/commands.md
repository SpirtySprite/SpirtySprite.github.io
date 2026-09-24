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
| `/item redo` | redoes the last undone change |
| `/item save <id>` | saves the item in hand to the library |
| `/item load <id>`, `/item library` | takes a copy of a saved item, or browses them all |
| `/item delete <id>` | removes an item from the library |
| `/item give <player> <id> [amount]` | gives a saved item, from a player or the console |
| `/item export` | copies the vanilla `/give` command for the item in hand |
| `/item info` | summarises the item in your hand |

Aliases: `/itemedit`, `/ie`, `/itemeditor`, `/edititem`.

`/item edit` fields: `name`, `lore`, `enchant`, `flag`, `attribute`, `amount`, `maxstack`, `damage`,
`maxdamage`, `repaircost`, `enchantable`, `unbreakable`, `glider`, `fireresistant`, `hidetooltip`,
`glint`, `rarity`, `model`, `itemmodel`, `tooltipstyle`, `type`, `color`, `skull`, `texture`, `potion`,
`trim`, `book`.

The library lives in `plugins/Itemsmith/library.yml` and keeps every detail of each item. Because
`/item give` works from the console, a shop, a crate or a quest plugin can hand out library items
with one command.

## Permissions

| Permission | Default | Effect |
|---|---|---|
| `itemsmith.admin.item` | op | use `/item` |
