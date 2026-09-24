---
title: "Troubleshooting"
sidebar:
  order: 11
---

Concrete symptoms, ordered roughly by how often they come up, and what's actually going on when you hit
them.

## The NPC never appears at all

- Check `npcs.capabilities()`, if `skins` is `false` for a `PLAYER`-type NPC you set a skin on, the
  *NPC itself* still spawns, just with no skin, so a totally invisible NPC is not a capabilities issue.
- Check the NPC's world and position against `npc.viewDistance()` (or the global default, 48) versus
  where you're actually standing, the manager's visibility pass is distance-and-world-based and will
  correctly *not* show an NPC that's genuinely out of range or in a different world.
- Check you actually called `.spawn()` on the builder, or that `manager.create(...)`/`FoliaNpc.spawn(...)`
  didn't throw before returning.
- Check the plugin holding the `FoliaNpc` instance is actually enabled, if `plugin.isEnabled()` is
  `false` (mid-shutdown, or a plugin load-order issue), every scheduler dispatch this library makes
  silently no-ops rather than throwing, so nothing will ever be sent to anyone.
- If you're testing immediately after a fresh player join, remember the very first visibility pass for a
  newly-joined player happens on the next tick after their join event, not synchronously during it, give it a fraction of a second.

## The NPC appears, but has no skin / the wrong skin

- `skin()`/`mirrorSkin()` only apply to `EntityType.PLAYER` NPCs. Check `npc.type()`.
- Check `capabilities().skins()`, if it's `false`, the profile-with-textures reflection path never
  resolved on this server build, and skins can never apply regardless of anything else you do.
- `fetchSkin`/`fetchSkinFromUrl` are asynchronous, if you call `npc.skin(...)` at all before the future
  completes, you'll briefly see the default skin. This is expected; there's no synchronous skin-fetch
  path by design (Mojang's API is a real network call).
- A skin fetch that fails (bad player name, Mojang API down, Mineskin rate limit) never caches the
  failure, but it also never retroactively applies once it *does* succeed unless you called `.thenAccept`
  on the returned future in the first place, check you're not silently swallowing the future.
- Mirror mode (`mirrorSkin(true)`) overrides whatever static skin is set, for every viewer, using *their
  own* skin, if you expected a specific static skin and instead everyone sees themselves, mirror mode is
  almost certainly still on.

## The floating nametag doesn't show, or the vanilla plate doesn't hide

- Check `capabilities().nametags()` for floating text, and `capabilities().namePlateHiding()` for
  suppressing the vanilla plate, both are independently optional and can fail on an unusual server build
  without breaking anything else.
- An **empty** list (`npc.nametag(List.of())`) is treated as "no floating nametag" and restores the
  vanilla plate, this is intentional, not a bug, see [Nametags](/wiki/folianpc/nametags/).
- If you're using a placeholder resolver and the text looks stale, check whether you're calling
  `refreshNametag()` (or have `autoRefreshNametag` set) after the underlying value actually changes, nametag text is not re-resolved automatically on every tick, only on an explicit refresh.

## Scale/baby/glow/collidable don't do anything

- Check the relevant `Capabilities` flag first (`scale`, `baby`), both rely on server-specific
  reflection that can fail independently of everything else.
- `baby` is a no-op on any entity type that doesn't support an adult/baby distinction in vanilla, see
  [Baby / adult state](/wiki/folianpc/appearance/#baby--adult-state) for exactly how that's determined. Setting it on a `PLAYER`
  or `SKELETON` NPC, for example, is expected to visibly do nothing.
- `glowColor` cannot be combined with a custom vanilla name-plate color, see [Appearance](/wiki/folianpc/appearance/#appearance).
  This is an actual Minecraft engine limitation, not something this library can work around.

## `variant`/`villagerProfession`/`villagerType`/`villagerLevel` don't do anything

- Check `Capabilities.mobVariants` / `Capabilities.villagerData` first, this is, by a wide margin, the
  most version-fragile part of the entire library (see [Design](/wiki/folianpc/#design) and
  [Known limitations](/wiki/folianpc/limitations/#known-limitations)): it depends on live server registry access, and on this exact
  class name existing (`net.minecraft.resources.Identifier` in current versions, `ResourceLocation` in
  older ones), either flag reporting `false` means that resolution failed on this server build entirely,
  and every method in this family is a guaranteed no-op regardless of anything else.
- Calling `variant(int)` on a `Cat`/`Wolf`/`Frog`, or `variant(String)` on anything else, is a no-op, check which overload applies to your entity type in [Mob variants](/wiki/folianpc/appearance/#mob-variants-cat-wolf-frog-rabbit-parrot-axolotl-mooshroom-horse).
- For the registry-backed ones (cat/wolf/frog coloring, villager profession/type), an unrecognized name
  silently fails to apply rather than throwing, double check spelling, and remember a bare name is
  assumed to be in the `minecraft:` namespace.
- For villager specifically: profession, type, *and* level all have to resolve for any of them to take
  effect. If you set a valid profession but a typo'd type, **neither** applies, not just the type, see
  [Villager profession, type, and level](/wiki/folianpc/appearance/#villager-profession-type-and-level).
- For the plain-int mobs (rabbit/parrot/axolotl/mooshroom/horse), remember there's no validation of the
  *value* at all beyond "is this entity type one of these five", an out-of-range ordinal is written
  as-is and however the client happens to render it (typically it clamps or shows the last valid variant,
  but this isn't something this library controls).

## `showInTabList` doesn't show the NPC in the tab list

- It only applies to `PLAYER`-type NPCs. Other entity types never get a tab-list entry at all, by
  design, regardless of this flag.
- Toggling it triggers a full respawn, if you don't see it take effect, confirm the toggle call is
  actually being reached (log it) rather than assuming the respawn itself failed.

## Actions/click listener don't fire

- Check `cooldown()`, a click inside another click's cooldown window for the *same player* is dropped
  silently, with no event, no log line, nothing observable at all by design.
- Check whether another plugin is cancelling `NpcInteractEvent`, cancelling it stops both your listener
  and every action for that click; add a low-priority listener of your own that logs
  `event.isCancelled()` to confirm.
- Check the clicking player's tracked position isn't wildly stale relative to the NPC (see
  [Reach validation](/wiki/folianpc/clicks-and-events/#reach-validation)), this only rejects genuinely implausible clicks and fails open
  when no position is known yet, but a player who just teleported through some other plugin without
  triggering a position refresh could theoretically be affected until their next tracked update.
- `Actions.connectToServer` requires you to have registered the `BungeeCord` outgoing plugin-messaging
  channel yourself, see [Clicks](/wiki/folianpc/clicks-and-events/#clicks). This is the single most common reason that specific action
  appears to silently do nothing.

## `navigateTo` always returns `false`

- Confirm `target` is in the *same world* as the NPC, cross-world routes are rejected immediately,
  before any search even runs, exactly like `walkTo` falling back to a teleport.
- The goal itself must be a standable position (solid ground below, open space at foot and head height), a route search that starts or ends inside a wall, or hovering in mid-air with nothing solid
  underneath, cannot succeed no matter how open the terrain in between is.
- The search is bounded (128 blocks radius, 4000 expanded nodes, both by default), a genuinely distant
  or maze-like target can exhaust the budget and fail even though a route technically exists; this is a
  deliberate tradeoff to keep worst-case search cost predictable, not a bug.
- A route that has to squeeze through a gap narrower than the search's model of "open" (diagonal
  corner-cutting is deliberately rejected, see [Movement](/wiki/folianpc/movement/)) will correctly fail to find a path
  through that gap even if a real player could walk through it.

## `navigateTo` throws, or logs a Folia/Canvas thread-check exception

If you see anything resembling `Cannot read world asynchronously` or `Thread failed main thread check`
coming out of `RoutePlanner`/`BukkitWorldSampler`/`AStar`, you're running a version of this library
older than the fix described in [Movement](/wiki/folianpc/movement/), upgrade. If you're seeing it on a code path
*other* than `navigateTo` after modifying this library yourself, you've most likely added a new
world/block read scheduled via `Schedulers.global(...)` instead of `Schedulers.onRegion(...)`, the
global region thread is legal for entity-agnostic, world-agnostic work only.

## `FoliaNpc.create()` throws `IllegalStateException`

This means either the running server reports a version older than 1.20.6, or one of the *mandatory*
(non-optional) reflection lookups the packet layer needs to bind at all, entity spawn/move/remove
packets, the tab-list update packet, the basic entity-metadata packet, failed to resolve. Unlike the
individually-optional `Capabilities` (skins, nametags, scale, etc.), these are load-bearing for the
entire library and there is no degraded mode: either the whole thing works, or `create()` refuses to
start rather than handing you a `FoliaNpc` that would silently do nothing. Check your actual server
version and build against the exact error message, which names the specific NMS class or field that
could not be found.

## Everything looks slightly wrong only for some players

If nametags, skin layers, or other metadata-driven visuals misbehave *specifically* for players on a
different Minecraft client version than the server, look at ViaVersion (or a similar cross-version
compatibility layer) first, it rewrites entity metadata packets in flight to match what the older/newer
client expects, and that rewriting can miss or mistranslate fields this library sends that weren't
present in the version ViaVersion is translating for. This is a limitation of running a cross-version
setup at all, not something specific to FoliaNPC.

## Duplicate NPCs or dead clicks after a PlugMan reload

Fixed: `close()` now removes every NPC and nametag line from every client directly, without going
through the scheduler (which refuses tasks once Bukkit has marked the plugin disabled, before
`onDisable` even runs). FoliaNPC also closes itself on its owner's `PluginDisableEvent`, so a plugin that
forgets to call `close()` still unloads cleanly. Reloading with PlugMan no longer leaves ghost NPCs on
the client, and clicks keep working without rejoining.

## Memory or thread-count grows across repeated `/reload`s

Confirm `close()` is actually being called in your plugin's `onDisable()`, see [Quick start](/wiki/folianpc/getting-started/#quick-start).
Skipping it leaves the injected netty packet-read handler attached to every still-connected player's
pipeline, and leaves the skin-fetch HTTP client's background thread pool running indefinitely, both of
which outlive the reload and accumulate with each subsequent one.
