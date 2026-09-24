---
title: "Puppeteer"
description: "Packet NPCs for Paper and Folia described in YAML."
sidebar:
  order: 0
  label: "Introduction"
---

Packet-based NPCs for Paper and Folia 1.21 and 26.x, fully described in `npcs.yml`. They exist only as
packets: no real entity, no server tick, Folia-native. Players with skins, villagers, cats, zombies or
any living entity, with nametag lines, equipment, poses, animations and click actions.

`/npc reload` compares every NPC with the live one and only recreates those that changed. An NPC whose
world is not loaded yet waits and appears on its own when the world loads. NPCs restricted to a
permission are only visible to players who have it, with no delay.

## Installation

1. Drop `Puppeteer.jar` into `plugins/`.
2. Start the server: `config.yml`, `npcs.yml` (with a few disabled examples) and the language files are
   created in `plugins/Puppeteer/`.

Optional: PlaceholderAPI (placeholders in texts), Vault (`GIVE_MONEY` and `TAKE_MONEY` actions).

## Languages

Puppeteer ships in English and French. Set the language in `config.yml`:

```yaml
language: en
```

Use `fr` for French. On first start, the example `npcs.yml` is written in the chosen language.

- `lang/messages_<language>.yml` holds every chat message. Edit it freely.
- `lang/<language>.yml` translates the menu and item texts. Add or override any entry to customise a
  label. Missing entries fall back to the original text.

To add a language, copy `lang/messages_en.yml` and `lang/en.yml` to `messages_<code>.yml` and
`<code>.yml`, translate them, and set `language: <code>`. Changing the language needs a restart.
