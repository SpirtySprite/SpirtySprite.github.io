---
title: "Commands"
sidebar:
  order: 3
---

`/npc` (aliases `/npcs`, `/pnj`, permission `puppeteer.admin.npc`): `reload`, `list`, `info <id>`,
`create <id> [type]`, `delete <id>`, `movehere <id>`, `tp <id>`, `rename <id> <name>`,
`skin <id> <player|url|mirror|none>`, `copy <id> <new>`, `enable <id>`, `disable <id>`, `stats`.
In-game edits rewrite `npcs.yml` and reload only the NPC concerned. `/npc reload` also rereads
`config.yml` and the language files. Changing `language` takes full effect after a restart.
