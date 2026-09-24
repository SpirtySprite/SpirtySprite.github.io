---
title: "Sidebars"
sidebar:
  order: 2
---

The right-hand board. There are four ways to drive one, from most convenient to most manual.

## 1. Fluent builder

```java
board.createBoard(player)
     .placeholders(true)              // resolve %built-ins% + PlaceholderAPI on strings
     .refreshEvery(4)                 // ticks between auto-refreshes of dynamic content
     .title("<gradient:#00c6ff:#0072ff><bold>MY SERVER</bold></gradient>")
     .blankLine()
     .line("<gray>Player: <white>%player%")
     .lines("<gray>Kills: <red>0", "<gray>Deaths: <red>0")   // several at once
     .blankLine()
     .line("<yellow>play.myserver.net")
     .build();                        // returns the live Sidebar
```

If any content is a placeholder string, an `Animation`, or a supplier, the board is **dynamic** and
FoliaBoard auto-refreshes it on the player's own thread, you never write a scheduler. Everything
else is painted once.

Titles and lines accept `String` (MiniMessage or legacy `&a` / `§a` / `&#ff00aa` codes), `Component`,
`Animation<Component>` or a per-player `Function<Player, String>`. Lines may also carry a
[number format](/wiki/foliaboard/tab-list/#number-formats).

Conditional lines only show when their predicate holds, and the rows below move up to fill the gap:

```java
board.createBoard(player)
     .placeholders(true)
     .title("&5&lNEXUS")
     .line("<gray>Money: <gold>%vault_eco_balance%")
     .lineIf(p -> p.hasPermission("staff"), "<red>Staff mode")
     .lineIf(p -> p.getWorld().getName().equals("event"), p -> "<aqua>Event: " + events.remaining())
     .build();
```

Refresh rate defaults to 3 ticks when an animation is present and 20 ticks for placeholder or
per-player content, so a board full of placeholders no longer resolves them six times a second.

## 2. Manual control

Full control, still safe from any thread:

```java
Sidebar sb = board.sidebar(player);         // get or create this player's sidebar
sb.title(mini("<gold>Kit Selector"));
sb.line(0, mini("<gray>Coins: <yellow>1500"));
sb.line(1, mini("<gray>Kills"), NumberFormat.fixed(mini("<red>12")));  // per-line number
sb.visible(false);                          // hide without discarding
sb.visible(true);
sb.clearLines();
sb.close();                                 // remove entirely (auto on quit)

// read-back:
Component title = sb.title();
List<Component> lines = sb.lines();
int count = sb.lineCount();
```

Only genuinely-changed lines produce packets, so frequent updates never flicker.

## 3. Global provider, one description for everyone

```java
board.setGlobalSidebar(SidebarProvider.of(
    p -> mini("<aqua>MY SERVER"),
    p -> List.of(mini("<gray>Online: <green>" + Bukkit.getOnlinePlayers().size())),
    10));   // refresh every 10 ticks
```

Or implement the interface for `visible(player)` control. FoliaBoard attaches a sidebar to every
player, refreshes it per player on the right thread, and cleans up on quit.

## 4. Global layout, same shape, per-player content

```java
board.setGlobalSidebar(Layout.named("main", b -> b
    .placeholders(true)
    .title("<aqua>MY SERVER")
    .line("<gray>Rank: <gold>%rank%")));
```

See [Layout profiles](/wiki/foliaboard/layout-profiles/#layout-profiles) for switching between several.

> **One driver per board.** A global provider/layout yields automatically to any explicit
> `createBoard(...).build()` or `applyLayout(...)` for that player, so they never fight.
