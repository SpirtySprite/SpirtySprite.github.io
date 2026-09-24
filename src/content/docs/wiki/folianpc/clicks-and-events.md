---
title: "Clicks and events"
sidebar:
  order: 8
---

## Clicks

For the simple case, a one-shot listener:

```java
npc.onClick((player, clicked, type) ->
    player.sendMessage("You " + type + "-clicked " + clicked.name()));
```

For anything with ordering, delay, or conditions, use actions instead. They form an ordered list per
click type (`LEFT`/`RIGHT` are tracked completely separately), run in the order they were added, and
each one can carry its own delay:

```java
npc.addAction(ClickType.RIGHT, Actions.message("<green>Hello %player%!"))
   .addAction(ClickType.RIGHT, Actions.sound(Sound.ENTITY_VILLAGER_YES, 1f, 1f), 10L)
   .addAction(ClickType.RIGHT, Actions.consoleCommand("give %player% diamond 1"))
   .cooldown(2000);
```

The built-in actions are `message`, `actionBar`, `title`, `command`, `consoleCommand`, `teleport`,
`sound`, `give`, `emote`, `swing`, `connectToServer`, `requirePermission` and `requireSneaking`, plus
the combinators `chance`, `random`, `sequence`, `cooldown` and `oncePerPlayer`:

```java
npc.addAction(ClickType.RIGHT, Actions.cooldown(Duration.ofHours(24),
        Actions.sequence(
                Actions.give(new ItemStack(Material.DIAMOND, 3)),
                Actions.title("<gold>Daily reward", "<gray>See you tomorrow %player%"),
                Actions.emote(Emote.WAVE)),
        "<red>Come back in %seconds%s."));

npc.addAction(ClickType.RIGHT, Actions.random(
        Actions.message("<gray>Nice weather today."),
        Actions.message("<gray>Have you seen the rift?")));

npc.addAction(ClickType.RIGHT, Actions.chance(0.05, Actions.give(rareItem)));
npc.addAction(ClickType.RIGHT, Actions.oncePerPlayer(Actions.message("<aqua>First time here?")));
```

`cooldown` is per player and cancels the remaining actions of that click while it is running, so it can
guard a whole chain. `oncePerPlayer` is kept in memory only, so it resets on restart; persist the
information yourself if it has to survive one. `%player%` (the clicking player's name) and `%npc%` (the
NPC's display name) are substituted into any text-bearing action for you. Actions compose functionally:

```java
Actions.command("/warp shop")
       .when(ctx -> ctx.player().hasPermission("shop.use"))
       .then(Actions.message("<gray>Off you go."));
```

`Actions.connectToServer(name)` sends the clicking player to another backend server through a BungeeCord
or Velocity proxy, over the standard `BungeeCord` plugin-messaging channel. **Your own plugin must
register that outgoing channel first**, `Bukkit.getMessenger().registerOutgoingPluginChannel(plugin, "BungeeCord")`, FoliaNPC deliberately never
registers anything on your behalf that you didn't explicitly ask for; if you forget this step, the
action silently does nothing (the plugin-messaging channel simply isn't open, so the packet the proxy
would need to see never leaves the server, with no exception on your end).

An action is just a `NpcAction`, a lambda over a context (`NpcClickContext`) that carries the click
details plus thread-safe ways to schedule follow-up work, so you never have to reason about which Folia
thread you're currently on:

```java
npc.addAction(ClickType.RIGHT, ctx -> {
    ctx.player().sendMessage("clicked " + ctx.click() + (ctx.sneaking() ? " while sneaking" : ""));
    ctx.data().put("step", 1);                        // scratch map, shared with later actions in this one click
    ctx.runGlobal(() -> world.strikeLightning(loc));  // global-region-thread work (console commands, world edits)
    ctx.runAsync(() -> database.load(...));           // off the server threads entirely; never touch Bukkit here
    ctx.runLater(() -> ..., 20L);                      // delayed, still follows the player across regions
    ctx.cancelRemaining();                             // skip every action still queued after this one, for this click
});
```

A listener or action that throws an exception is caught, logged as a warning (naming the NPC), and
skipped, one buggy handler never breaks the rest of the chain or crashes anything. `cooldown(millis)`
is tracked per clicking player, not globally, and any click that lands inside another player's cooldown
window is simply dropped (no message, no event, nothing, treat it as if the click never happened).
`ctx.sneaking()` (and `event.isSneaking()` on the Bukkit event, below) exposes whether shift was held
during the click, which is the standard way to implement a shift-click as a secondary action distinct
from a normal click.

### Reach validation

A click is only actually acted on when the clicking player's last known tracked position is plausibly
near the NPC, this rejects an interact packet forged (by a modified client) to claim a click on an NPC
the player is nowhere near, since the raw interact packet itself carries no position for the server to
check against. This check fails **open** (i.e. the click is allowed through) when no tracked position is
known yet for that player at all, which is normal and expected in the very first instant after they join
before their first position snapshot has been taken, the alternative (failing closed) would silently
drop a player's very first legitimate click on any NPC visible immediately on spawn.

## Events

FoliaNPC fires ordinary Bukkit events, so other plugins (permission plugins, region-protection plugins,
anything) can react to NPCs they did not create themselves:

```java
@EventHandler
public void onNpcClick(NpcInteractEvent event) {
    if (!canInteractHere(event.getPlayer())) {
        event.setCancelled(true);   // stops both the NPC's own listener and every one of its actions
    }
    if (event.isSneaking() && event.getClick() == ClickType.RIGHT) {
        openAdminMenu(event.getPlayer(), event.getNpc());
    }
}

@EventHandler public void onSpawn(NpcSpawnEvent event) { ... }   // fires for every NPC registered, including ones you didn't create
@EventHandler public void onRemove(NpcRemoveEvent event) { ... } // fires once the NPC is already gone; not cancellable
```

`NpcInteractEvent` is `Cancellable` and fires **before** the NPC's own `onClick` listener and its
registered actions run, specifically so that a region-protection plugin (or anything else that doesn't
own the NPC) can veto an interaction by cancelling the event, cancelling stops the listener and every
action from running at all for that click. It fires on the clicking player's own region thread, the same
threading guarantee a vanilla Bukkit entity-interact event gives you, even though the underlying packet
was actually decoded on a netty I/O thread first and had to hop across before the event was ever raised.
