---
title: "Appearance and equipment"
sidebar:
  order: 7
---

## Appearance

```java
npc.glowing(true)
   .glowColor(NamedTextColor.AQUA)   // outline colour, and the vanilla name-plate colour
   .invisible(true)                  // hides the body, keeps armour and the nametag
   .skinLayers(false)                // disables hat/jacket/sleeves on player NPCs
   .scale(1.6)                       // render size; 1.0 is normal, requires 1.20.5+
   .collidable(false)                // players pass through it instead of bumping into it
   .showInTabList(true)              // player NPCs only; off by default
   .pose(NpcPose.SITTING);

npc.swing();          // one-shot arm-swing animation, useful as click feedback
npc.swingOffHand();
```

`glowing`, `invisible`, and `skinLayers` all travel together in a single entity-metadata packet, so
changing any of them is a cheap live update with no respawn.

`glowColor` and `collidable` are **team properties** in vanilla Minecraft, there is no other mechanism
to set an entity's glow color or disable player collision, so setting either one (to a non-default
value) forces the NPC onto its own scoreboard team, exactly like hiding the nametag does (see
[Nametags](/wiki/folianpc/nametags/) above for the wire-name consequence of that). As a direct result: **an NPC with a
non-null `glowColor` cannot simultaneously show a custom-colored vanilla name plate**, because glow color
*is* the team's name-plate color and there's only one team-color slot. Use a floating nametag for
independent text color instead, which is almost certainly what you wanted anyway if you're setting a
glow color in the first place.

`showInTabList` controls the tab-list entry independently of the vanilla name plate. It's `false` (not
listed) by default specifically so that spawning many NPCs doesn't clutter every player's tab list with
entries that aren't real players. Toggling it re-sends the NPC (full despawn/respawn), because the
listed/unlisted flag lives in the same tab-list packet as the profile and skin. It only has any effect
on `PLAYER`-type NPCs, other entity types never receive a tab-list entry regardless of this setting.

All of the cosmetic state above (everything except pose and baby, see below) is available as a single
immutable `NpcAppearance` object, which is also exactly what `NpcData` stores for persistence:

```java
otherNpc.appearance(npc.appearance());   // copy one NPC's full look onto another
```

### Baby / adult state

```java
npc.baby(true);
```

`baby` only takes effect on entity types that actually support an adult/baby distinction in vanilla, zombies, villagers, most animals, and so on, and is a **harmless no-op** on anything that doesn't
(players, skeletons, and any other type with no such concept). Whether a given `EntityType` qualifies is
decided by checking Bukkit's own `org.bukkit.entity.Ageable` interface hierarchy (via
`EntityType.getEntityClass()`), not a hand-maintained list of mob names, so it stays correct
automatically as Mojang adds new ageable mobs in future versions, with zero maintenance burden on this
library's side. Toggling it is a plain metadata push, not a respawn. `Capabilities.baby` reports whether
the underlying metadata field could be resolved on this server at all; see
[Troubleshooting](/wiki/folianpc/troubleshooting/) if it reports `false` unexpectedly.

### Mob variants (cat, wolf, frog, rabbit, parrot, axolotl, mooshroom, horse)

```java
npc.variant("black");       // Cat, Wolf, Frog: a named registry entry
npc.variant(2);             // Rabbit, Parrot, Axolotl, Mooshroom, Horse: a raw ordinal
```

Which overload actually applies is decided by `npc.type()`, exactly like `baby`, calling either one on
an entity type it doesn't apply to is a harmless no-op, and the value you set is retained even while
it's inapplicable, in case you later change the type to something it does apply to.

**`Cat`, `Wolf`, and `Frog`** use `variant(String)`, as of the versions this was implemented against,
their coloring is a live server **registry** lookup (a `Holder<CatVariant>` etc.), not a fixed ordinal,
because vanilla itself moved these to data-driven registries that a resource/data pack can add entries
to. A bare name like `"black"` is resolved with the `minecraft:` namespace assumed; use `"mymodpack:custom_cat"`
explicitly for anything from a data pack. An unknown name silently fails to apply (see
[Troubleshooting](/wiki/folianpc/troubleshooting/)) rather than throwing.

**`Rabbit`, `Parrot`, `Axolotl`, `Mooshroom`, and `Horse`** use `variant(int)`, these are still plain
integer-coded fields in vanilla, so there's no registry to look up, just a raw ordinal written straight
to the entity's own variant field. This library does not maintain a name-to-ordinal table for these
(unlike the registry-backed ones, there's no live authority to ask, and the meanings are baked into the
client), so you'll need to look up or test the specific ordinal-to-appearance mapping for the version(s)
you support. `npc.variant()` reads back whatever raw int was last set; `npc.variantName()` reads back
whatever registry name was last set, the two are stored independently, so switching an NPC's type back
and forth doesn't lose either one.

`Capabilities.mobVariants` reports whether *any* of the above resolved on this server, it's one combined
flag covering all eight mob types rather than one flag each, consistent with how `Capabilities.equipment`
already covers every equipment slot as a single flag.

### Villager profession, type, and level

```java
npc.villagerProfession("farmer")   // e.g. "farmer", "librarian", "cartographer", "none", ...
   .villagerType("plains")         // the biome-flavoured skin tint, e.g. "plains", "desert", "taiga"
   .villagerLevel(3);              // 1-5; the copper/iron/gold/emerald badge, clamped to at least 1
```

Only applies to `EntityType.VILLAGER`; a no-op on everything else, same as the other variant methods.
Unlike the coloring mobs above, villager data is a genuine **composite** value, profession and type are
each their own registry lookup (again resolved against the live server registry, so data-pack-added
professions/types work by name automatically), and the three together are packed into one `VillagerData`
object written as a single metadata field. All three of `villagerProfession`, `villagerType`, and
`villagerLevel` must resolve to something for *any* of them to apply, if either the profession or type
name doesn't exist in the registry, nothing is sent for that update at all (the previous value, if any,
is simply left in place) rather than sending a partially-valid `VillagerData`. There is no built-in list
of valid profession/type names in this library; the vanilla ones haven't changed in a long time (farmer,
librarian, cartographer, cleric, armorer, weaponsmith, toolsmith, butcher, leatherworker, fletcher,
fisherman, shepherd, mason, nitwit, none for profession; plains, desert, savanna, snow, swamp, taiga,
jungle for type) but any data pack on the server can add more.

`npc.mobVariant()` / `npc.mobVariant(MobVariant)` read/write all five of the above (the int variant, the
named variant, and the three villager fields) as one immutable `MobVariant` object in a single call,
mirroring how `appearance()`/`appearance(NpcAppearance)` work for cosmetic state, handy for copying one
NPC's variant configuration onto another, or restoring it from your own storage in one shot instead of
five separate calls. `Capabilities.villagerData` reports whether this specific subsystem resolved.

### Everything else: chicken/cow/pig variants, painting variants, and other mob-specific fields

A handful of other mobs (chicken, cow, pig, painting frames) also moved to the same kind of live-registry
variant system as cat/wolf/frog in recent versions, but don't have a typed method here yet, the
registry-lookup machinery `variant(String)` relies on is shared internally, so adding another mob to that
list is a small, low-risk addition if you need one; it just hasn't been done. Everything else, anything
not listed above, on any entity type, has no typed API at all and falls back to the raw metadata escape
hatch:

```java
npc.metadata(17, MetadataType.INT, 3);    // a simple int-valued field, by raw index, for a mob not listed above
npc.metadata(17, MetadataType.INT, null); // clear it
```

`BYTE`, `INT`, `BOOLEAN`, and `FLOAT` are supported, this covers flag bytes and simple integer/float
variants, but not composite/registry-backed fields, which this raw path has no way to represent at all.
**This is a genuinely dangerous escape hatch if you get the index wrong**: entity metadata indices are
assigned per entity class, in registration order, and are *not* validated against the entity type you're
targeting. Writing to an index that doesn't correspond to what you think it does on that particular
entity type will silently write garbage into whatever field actually lives at that index for that type, there is no error, no warning, just a corrupted or nonsensical-looking NPC. Indices also **change between
Minecraft versions**, so any index you hardcode should be treated as tied to a specific version range,
not assumed portable. A value that doesn't fit its declared `MetadataType` (e.g. a `String` passed as
`INT`) is silently skipped rather than breaking the rest of the NPC's metadata packet, but a well-typed
*wrong* value at a plausible-looking index will not be caught, verify visually in-game after using this,
on every Minecraft version you support.

## Equipment

```java
npc.equipment(EquipmentSlot.HEAD, helmet);
npc.equipment(EquipmentSlot.HAND, sword);
npc.equipment(EquipmentSlot.HAND, null);   // clears the slot (an ItemStack of AIR also clears it)
```

Works identically on player and mob NPCs, and applies live without a respawn, a single equipment packet
per change. `EquipmentSlot.BODY` (horse/wolf armor, on 1.20.5+) is supported where the running server's
NMS classes expose it; on older servers that slot is silently ignored rather than throwing, consistent
with this library's overall "degrade a feature rather than break the NPC" philosophy.
