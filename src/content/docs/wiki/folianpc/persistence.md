---
title: "Persistence and diagnostics"
sidebar:
  order: 9
---

## Persistence

The library stores nothing itself, on disk or otherwise. It's a library, not a plugin with a data
folder, so it makes no assumptions at all about your database engine, file format, or schema. Instead it
gives you a plain, serializable snapshot type and a way back from it:

```java
List<NpcData> saved = npcs.saveAll();   // typically on shutdown; or npc.data() for just one NPC
npcs.spawnAll(saved);                   // typically on startup; or npcs.spawn(data) for just one
```

`NpcData` is a plain record of primitive/simple values (id, name, type, world/x/y/z/yaw/pitch, skin,
mirror-skin flag, equipment map, nametag lines, appearance, pose, baby flag, tab-list flag, mob
variant, owner, nametag style), so it serializes cleanly with whatever you already use: Gson, Jackson, a config
library, a database row mapper, anything that can handle a POJO/record. Re-spawning from a saved
`NpcData` **keeps the original id**, so anything you have keyed on `npc.id()` elsewhere in your own
data still matches up correctly after a server restart.

`npc.owner(uuid)` / `npc.owner()` attach whoever the NPC is attributed to, typically its creator. This
is **purely informational**: FoliaNPC itself never reads this value for any permission decision, view
logic, or anything else internally. It exists solely so you can build your own permission checks on top
of it (e.g. "only the owner or a server admin may edit this NPC"), without having to maintain a separate
side-table mapping NPC id to creator yourself.

## Diagnostics

`npcs.capabilities()` returns a `Capabilities` record reporting which optional subsystems actually bound
successfully on this specific server: `skins`, `nametags`, `namePlateHiding`, `equipment`, `scale`,
`richText`, `baby`, `mobVariants`, `villagerData`. Every one of these is independently optional by design, if the reflection needed
for one of them can't resolve on a given server build, that one feature silently degrades to a no-op
rather than the whole library refusing to start, so a mismatched or unusually-patched server never turns
into a hard crash. Check `capabilities().missing()` (a `List<String>` of human-readable names) at
startup if you want to surface a single warning to your own users, or fall back to a different behavior,
rather than silently losing a feature with no indication anything's different. Anything that fails to
bind also logs its own warning line to the console at startup regardless of whether you check
`capabilities()` yourself.

| Capability | What losing it means |
|---|---|
| `skins` | `npc.skin(...)` has no visible effect; player NPCs render with the default Steve/Alex skin |
| `nametags` | Floating nametags (`npc.nametag(...)`) cannot be created at all |
| `namePlateHiding` | `nametagVisible(false)`, `glowColor`, and `collidable(false)` cannot suppress/set the team, so the vanilla plate and default collision behavior stay in effect regardless |
| `equipment` | `npc.equipment(...)` has no visible effect |
| `scale` | `npc.scale(...)` has no visible effect; the NPC always renders at 1.0 |
| `richText` | Gradients/hover text degrade to legacy section-sign color codes |
| `baby` | `npc.baby(...)` has no visible effect on any entity type |
| `mobVariants` | `npc.variant(...)` has no visible effect on any of cat/wolf/frog/rabbit/parrot/axolotl/mooshroom/horse |
| `villagerData` | `npc.villagerProfession(...)`/`villagerType(...)`/`villagerLevel(...)` have no visible effect |

`npcs.stats()` returns a `Stats` record: a cheap, instantaneous snapshot of current load, the live NPC
count, the number of viewer *pairings* (one NPC seen by 20 different players counts as 20, not 1), the
running total of packets sent since startup, and the duration of the most recent tick pass in
milliseconds. It's cheap enough to poll on a timer for a live admin dashboard or a `/npcs debug` command.

`npcs.diag()` returns a one-line human-readable string (`npcs=N trackedPlayers=M`) suitable for logging
or a quick chat message, without needing to format a `Stats` record yourself.

`npcs.setDebug(true)` turns on verbose logging: every time an NPC is newly shown to a viewer, and every
packet-send failure, is logged at a visible level instead of being silently handled. Leave this off in
production, it's meant for diagnosing a specific problem, not for routine operation.
