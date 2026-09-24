---
title: "Threading"
sidebar:
  order: 10
---

Folia's one hard rule, which this entire library exists to work correctly under: **you may only touch a
player or any other real entity from the region thread that currently owns it.** Touching one from the
wrong thread, including the "global" region thread, and including a background thread from your own
async work, throws or silently corrupts state, depending on exactly what you touched.

The library handles this for you internally wherever it can:

- Player positions are snapshotted onto a plain data object (`PlayerTracker.Tracked`) on the player's own
  region thread, and the manager's per-tick visibility pass only ever reads those already-safe
  snapshots, it never calls back into a live `Player`/`Entity` object from the wrong thread.
- Every packet is sent on the *receiving* player's own region thread, scheduled via
  `entity.getScheduler()`.
- Anything that needs to touch **world/block data** rather than an entity (currently: only
  `navigateTo`'s route search) is scheduled via the **region** scheduler tied to a specific location,
  which is the correct primitive for that, not the global region thread, which is legal for
  entity-agnostic, world-agnostic work like dispatching a console command, but is **not** legal for
  reading blocks (see [Movement](/wiki/folianpc/movement/) for the specific exception this throws if you get it wrong).
- Console commands and anything else that isn't tied to one specific player or one specific chunk run on
  the **global** region scheduler.

In your own action code (see [Clicks](/wiki/folianpc/clicks-and-events/#clicks)), always prefer the `NpcClickContext` helpers
(`ctx.run`, `ctx.runLater`, `ctx.runGlobal`, `ctx.runAsync`) over calling Bukkit's own scheduler
directly, they already know which of the above categories your work falls into and route it correctly,
without you having to reason about Folia's region model yourself. The `Npc` handle itself is safe to
call from **any** thread at any time; every mutable field behind it is `volatile` or an appropriately
concurrent collection specifically so that holding an `Npc` reference and calling setters on it from,
say, an async database callback, is always safe.
