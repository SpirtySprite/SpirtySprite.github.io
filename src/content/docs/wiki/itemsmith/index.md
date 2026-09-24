---
title: "Itemsmith"
description: "In-game item editor for Paper and Folia."
sidebar:
  order: 0
  label: "Introduction"
---

In-game item editor for Paper and Folia 1.21 and 26.x. Hold an item, type `/item` and edit everything
from a menu: name, description, enchantments, attributes, hide flags, model, tooltip style, rarity,
colour, player heads, durability and more. Every change can be undone.

## Installation

1. Drop `Itemsmith.jar` into `plugins/`.
2. Start the server. `config.yml` and the language files are created in `plugins/Itemsmith/`.

PlaceholderAPI is optional.

## Languages

Itemsmith ships in English and French. Set the language in `config.yml`:

```yaml
language: en
```

Use `fr` for French.

- `lang/messages_<language>.yml` holds every chat message. Edit it freely.
- `lang/<language>.yml` translates the menu and item texts. Add or override any entry to customise a
  label. Missing entries fall back to the original text.

To add a language, copy `lang/messages_en.yml` and `lang/en.yml` to `messages_<code>.yml` and
`<code>.yml`, translate them, and set `language: <code>`. Changing the language needs a restart.

Text input in game goes through a sign. All messages accept MiniMessage. `/item reload` rereads
`config.yml` and the language files.
