---
title: "Movement and pathfinding"
sidebar:
  order: 3
---

```java
npc.teleport(location);      // instant, works across worlds
npc.walkTo(location, 4.0);   // walk in a straight line at 4 blocks per second
npc.stopWalking();
```

`teleport` is instant and works across worlds. It re-sends the NPC to every current viewer (a full
despawn/respawn), which produces a brief visual flicker on a long jump, there's no interpolation, the
NPC simply appears at the new spot. Teleporting also immediately cancels any in-progress `walkTo` or
`navigateTo`.

`walkTo` moves in a perfectly straight line at the given speed (blocks per second), with **no
pathfinding, no obstacle avoidance, and no gravity**: it will walk through walls, off the edges of
cliffs, and straight across gaps that a real mob would fall into. If your use case can guarantee open,
flat ground between the NPC and its destination (e.g. a fixed patrol route you designed by hand), this
is the cheapest option, it costs nothing but simple linear interpolation, computed on the same thread
that already ticks the NPC, no block reads at all. A target in a different world silently falls back to
a `teleport` instead of attempting to walk.

## Pathfinding with `navigateTo`

```java
npc.navigateTo(target, 4.0).thenAccept(found -> {
    if (!found) plugin.getLogger().warning("no route to " + target);
});
```

`navigateTo` computes an actual route instead of a straight line, using a simple grid-based A* search
over the live block data around the NPC:

- It considers the 8 horizontal directions from each grid column, checking that both the "feet" and
  "head" blocks are passable and the block below is solid ground.
- It can **step up** one block and **step down/fall** up to three blocks to handle uneven terrain
  (stairs, single-block ledges, shallow drops).
- Diagonal moves are rejected if they would cut through a solid wall corner (both of the two flanking
  columns must be open, not just the diagonal target itself).
- The search is bounded by both a maximum radius (128 blocks from the start by default) and a maximum
  number of expanded nodes (4000 by default), so an unreachable or maze-like goal fails predictably
  instead of hanging.
- Step-up legs are given an extra waypoint that arcs slightly above the landing height, so the NPC
  visibly hops onto the block instead of gliding up it in a straight diagonal line.
- Both `walkTo` and `navigateTo`-driven movement face the direction of travel while the NPC is actually
  moving, **even if `lookAtPlayers(true)` is set**, the travel-facing rotation takes priority for the
  duration of the walk, and `lookAtPlayers` resumes control the instant the NPC arrives and stops.

This is a simple grid search, not real mob AI: it has no concept of doors, ladders, water, minecarts, or
multi-block structures, and it will not squeeze through a 1-wide gap it hasn't explicitly modeled as
open. See [Troubleshooting](/wiki/folianpc/troubleshooting/) if a route you'd expect to succeed keeps failing, or if a
route that should be blocked isn't.

`navigateTo` returns a `CompletableFuture<Boolean>` because the search itself has to run on a specific
thread (see below) rather than synchronously on the caller's thread. `false` means the NPC did not
move at all, either no route was found within the search bounds, or `target` is in a different world
(cross-world routes are not supported by `navigateTo`; use `teleport` or `walkTo` for that case, exactly
as with plain `walkTo`). Call `stopWalking()` at any time to cancel a route in progress, exactly as you
would cancel a plain `walkTo`.

**Threading detail, because this bit us during development and is worth being explicit about:** reading
block data (`World.getBlockAt(...)`) is only legal, on Folia and Folia forks, from the region thread
that actually owns the chunk in question, *not* from the global region thread, which some other
Folia-aware code (including earlier versions of this library) mistakenly treats as a safe place to do
arbitrary world reads. Doing so throws (on Canvas, a Folia fork, this surfaces as
`IllegalStateException: Thread failed main thread check: Cannot read world asynchronously`; other forks
may phrase it differently, but the underlying rule is the same). `navigateTo` schedules its search via
`Bukkit.getRegionScheduler().execute(plugin, npcLocation, ...)`, tied to the NPC's own current location,
which is guaranteed correct for reads within that region. If the route wanders into a neighboring region
that hasn't merged with the NPC's own, block reads there are best-effort rather than strictly
guaranteed-safe, the same tradeoff every Folia-aware plugin accepts for any feature that can span
region boundaries. In practice, regions are large relative to typical NPC walk distances, so this only
matters for very long routes near a region boundary on a busy, heavily-split server.

## General movement notes

The floating nametag (if any) and held/worn equipment move together with the NPC during both `walkTo`
and `navigateTo`, they are separate entities from the NPC's own, but the manager moves all of them in
lockstep every step.
