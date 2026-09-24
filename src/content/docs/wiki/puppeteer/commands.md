---
title: "Commands"
sidebar:
  order: 4
---

`/npc` (aliases `/npcs`, `/pnj`, permission `puppeteer.admin.npc`): `reload`, `list`, `info <id>`,
`create <id> [type]`, `delete <id>`, `movehere <id>`, `tp <id>`, `rename <id> <name>`,
`skin <id> <player|url|mirror|none>`, `copy <id> <new>`, `enable <id>`, `disable <id>`, `stats`,
`path add|clear <id>`, `forget <id> [player]` (resets the `once` actions of an NPC, for one player or
everyone), `import <source>`.
In-game edits rewrite `npcs.yml` and reload only the NPC concerned. `/npc reload` also rereads
`config.yml` and the language files. Changing `language` takes full effect after a restart.
