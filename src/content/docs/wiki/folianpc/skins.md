---
title: "Skins"
sidebar:
  order: 5
---

A skin is Mojang's signed texture pair (`value` + `signature`). Fetch one by player name or UUID; both
calls are asynchronous (they hit Mojang's public API over HTTPS) and cached:

```java
npcs.fetchSkin("Notch").thenAccept(npc::skin);
npcs.fetchSkinFromUrl("https://.../skin.png").thenAccept(npc::skin);   // generated via Mineskin
npcs.skinCacheTtl(Duration.ofHours(1));                                // default is 30 minutes
```

Applying a skin re-sends the NPC (a full despawn/respawn for current viewers), so it's safe to call at
any time, including before the NPC has ever been shown to anyone. If you already have the raw
value/signature pair from somewhere else, skip the network call entirely and build one directly:
`new Skin(value, signature)`.

Failed lookups are **never cached**, a single Mojang API blip (rate limiting, a timeout, a transient
5xx) does not permanently break that name/UUID's skin for the rest of the server's uptime; the next call
simply retries the network request. All requests, including the URL/Mineskin path, time out after ten
seconds. Skins apply **only to `PLAYER`-type NPCs**; setting one on any other entity type is harmless
but has no visible effect, and it's preserved (not discarded) if you later switch the type back to
`PLAYER`.

## Mirroring

```java
npc.mirrorSkin(true);   // each viewer now sees the NPC wearing their own current skin
```

Each viewer's own skin is read directly off their live Bukkit profile (`Player.getPlayerProfile()`) at
the moment they're shown the NPC, there is **no network fetch and no caching involved at all**, unlike
`fetchSkin`. The static skin set with `npc.skin(...)` is retained underneath and comes back immediately
for every viewer as soon as mirroring is turned back off; the two are not mutually destructive. Mirroring
only applies to `PLAYER`-type NPCs, same restriction as static skins.
