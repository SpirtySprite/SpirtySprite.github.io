---
title: "Creating NPCs"
sidebar:
  order: 2
---

## Creating NPCs

The builder handles creation. Only `location` is required, everything else has a sensible default.

```java
Npc npc = npcs.builder()
    .name("Guard")                 // display name, and the vanilla name plate
    .type(EntityType.ZOMBIE)       // defaults to PLAYER
    .location(loc)
    .lookAtPlayers(true)
    .viewDistance(32)              // 0 or less uses the global default of 48
    .cooldown(1000)                // minimum milliseconds between clicks, per player
    .owner(player.getUniqueId())   // purely informational, see Persistence
    .spawn();
```

Every builder option has a matching setter on the live `Npc`, so anything you configure at spawn you can
also change afterwards:

```java
npc.name("Merchant").glowing(true).scale(1.5);
npcs.all();          // every live NPC, as a snapshot list safe to iterate
npcs.get(uuid);       // one by id, or null if it doesn't exist / has been removed
npc.remove();         // despawns for everyone and unregisters; the handle must not be reused after this
```

Renaming re-sends the NPC (a full despawn/respawn for every current viewer), because the name is
embedded in the tab-list profile the client received at spawn time and can't be patched afterwards.

### Visibility range

An NPC is shown to players within range (48 blocks by default) in the *same world* and hidden again the
moment they leave, either by walking away or by changing worlds. You do not manage this yourself, the
manager recalculates who should see what roughly ten times a second (every 2 game ticks) and sends only
the difference (newly-in-range players get a spawn packet, newly-out-of-range players get a despawn).
The range is adjustable globally with `npcs.viewDistance(64)` or per NPC with `.viewDistance(32)`; a
per-NPC value of 0 or less falls back to the current global default.

### Entity type

Player NPCs receive the full tab-list profile and can carry a skin. Any other `EntityType` is sent as a
plain spawn packet with no tab-list entry at all, so skins, skin layers, and the tab-list toggle never
apply to those, everything else (nametags, equipment, actions, glow, scale, pose, baby) works
identically for both.

The type can be changed after spawning, not just at creation:

```java
npc.type(EntityType.ZOMBIE);
```

This always triggers a full despawn/respawn for every current viewer, the entity type is part of the
spawn packet itself, so there is no way to patch it in place. Switching *from* `PLAYER` to something
else drops the skin/skin-layers/tab-list-listing visual effects for viewers until you switch back
(the underlying `Skin`/`mirrorSkin`/`showInTabList` state is preserved on the `Npc`, just not applied
while the type doesn't support it).

## Cloning

```java
Npc copy = npc.copy(otherLocation);
```

Spawns a new, fully independent NPC at `otherLocation` with the same configuration as the source: type,
skin, skin mirroring, equipment, nametag lines, appearance (glow/invisible/skin layers/scale/glow
color/collidable/nametag visibility), pose, baby state, cooldown, view distance, click listener, and
every registered action (for both `ClickType.LEFT` and `ClickType.RIGHT`, in the same order with the
same delays). The copy gets a brand-new random id and starts completely fresh at the *tracking* level:
no current viewers, no per-player interaction cooldowns, no `showTo`/`hideFrom` visibility overrides, those are runtime state tied to the original NPC's history, not configuration, so they are never copied.

Actions and the click listener are copied by reference (the same `NpcAction`/`NpcClickListener`
instances are reused on the copy) rather than being deep-cloned, since they're just functional
interfaces. This is safe as long as your actions don't close over the *specific* source `Npc` instance
expecting it to always be the one that was clicked, well-written actions read the NPC from
`ctx.npc()` rather than capturing one from an enclosing scope, and those work identically on a copy.
