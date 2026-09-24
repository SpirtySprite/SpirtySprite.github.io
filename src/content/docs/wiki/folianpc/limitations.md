---
title: "Limitations and building"
sidebar:
  order: 12
---

## Known limitations

- **No gravity, no physics.** Position never changes except through `teleport`, `walkTo`, or
  `navigateTo`. An NPC spawned in mid-air, or left standing where the ground is later removed, will
  float indefinitely, nothing in this library will ever move it on its own to compensate.
- `navigateTo`'s pathfinding is a simple bounded grid search (see [Movement](/wiki/folianpc/movement/)), not full mob
  AI: no doors, no ladders, no water, no multi-block structure awareness, and a bounded search radius and
  node budget that a sufficiently distant or maze-like target can exhaust.
- Typed mob-variant support covers baby state, villager profession/type/level, and cat/wolf/frog/
  rabbit/parrot/axolotl/mooshroom/horse coloring, see [Mob variants](/wiki/folianpc/appearance/#mob-variants-cat-wolf-frog-rabbit-parrot-axolotl-mooshroom-horse)
  and [Villager profession, type, and level](/wiki/folianpc/appearance/#villager-profession-type-and-level). This is the single
  most version-fragile part of the library: it depends on live server registry access and on specific
  NMS class names (`Identifier` vs. the older `ResourceLocation`, entity classes that have moved between
  packages across versions) that this library tries several known variants of but cannot guarantee for
  every future Minecraft release. Everything else (chicken/cow/pig/painting variants, and any field on
  any mob not listed above) has no typed API and falls back to the raw `metadata` escape hatch.
- Glow colour cannot be combined with a custom vanilla name-plate colour, an actual Minecraft engine
  constraint (both come from the same team-color slot), not something this library chooses to restrict.
- ViaVersion (or similar) can rewrite entity metadata when a client's version differs from the server's;
  nametags and skin layers are the parts most likely to be affected for cross-version clients.
- The reflection layer (`internal/protocol/nms`) has no automated test coverage, because it needs a live
  server to exercise real NMS classes. The unit test suite covers all the pure logic that can be tested
  without one, visibility, geometry, click routing, cooldowns, actions, nametag layout, events, skin
  caching, and the pathfinding algorithm itself (via a fake in-memory grid), but anything that actually
  talks to NMS, including skin mirroring's texture substitution, the pathfinder's real block reads, and
  every mob-variant/villager-data registry lookup, has to be verified in game on each supported
  Minecraft version. The manager-level wiring for mob variants and villager data (that the right value
  ends up in the right snapshot field, round-trips through `NpcData`, and doesn't force a respawn) is
  unit tested; only the actual registry resolution and packet construction is not.

## Building

```bash
mvn package
```

Produces a plain library jar with no plugin descriptor, and runs the full unit test suite as part of the
build, a failing test fails the build.

```bash
mvn install
```

Same, but also installs the jar to your local Maven repository so another local project (a plugin that
depends on this library, or a separate test harness) can resolve it as a Maven dependency without
needing it published anywhere.
