---
title: "Visibility"
sidebar:
  order: 4
---

By default an NPC is shown to anyone within range, in the same world. You can override that per player,
which is how you gate an NPC behind a permission check, a quest step, or an A/B test:

```java
npc.hideFrom(player);         // never shown to this player, however close they are
npc.showTo(player);           // always shown to this player, ignoring the distance check
npc.resetVisibility(player);  // drop the override, return to the normal distance check
```

Overrides take effect on the next visibility pass (within ~100ms), not instantly, and only affect the
one player they were set for. `showTo` ignores distance but never crosses worlds, a player standing in
the nether will never see an overworld NPC no matter how forcefully you `showTo` them. Overrides are
**cleared automatically when a player disconnects** (this is deliberate, a permission or quest state
that changed while they were offline shouldn't silently resurrect a stale override), so if you want an
override to persist across sessions, re-apply it yourself on their next join, sourced from your own
storage. `UUID`-based overloads exist for setting overrides on players who are currently offline.

For a rule rather than a list of players, give the NPC a condition. It is evaluated for players in range
on each visibility pass, a per-player override still wins over it, and a condition that throws simply
hides the NPC from that player instead of breaking the pass:

```java
npc.visibleWhen(player -> player.hasPermission("rank.vip"));
npc.visibleWhen(player -> quests.step(player) >= 3);
npc.visibleWhen(null);  // back to everyone in range
```

Teleports are tracked too: after `/spawn`, `/warp` or any other teleport, NPCs at the destination
appear and NPCs at the origin disappear without waiting for the player to take a step.

Visibility overrides are **not** included in `NpcData` / `npc.data()`, they are runtime-only state by
design, precisely because they're meant to be re-derived from your own permission/quest logic on each
join rather than snapshotted and blindly restored.
