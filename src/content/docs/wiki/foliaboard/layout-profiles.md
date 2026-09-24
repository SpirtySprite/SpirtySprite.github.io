---
title: "Layout profiles"
sidebar:
  order: 3
---

## Layout profiles

A **layout** is a reusable, named board template you can apply to any player and switch between
instantly (lobby ↔ minigame, per-world boards, …). It's just a recorded recipe of builder calls.

```java
Layout lobby = Layout.named("lobby", b -> b
    .placeholders(true)
    .title(Animations.cycle(Duration.ofMillis(400), mini("<aqua>LOBBY"), mini("<white>LOBBY")))
    .blankLine()
    .line("<gray>Rank: <gold>%rank%")
    .line("<gray>Coins: <yellow>%coins%"));

Layout minigame = Layout.named("minigame", b -> b
    .title("<red><bold>SKYWARS</bold>")
    .line("<gray>Kills", NumberFormat.fixed(mini("<red>0"))));

board.registerLayout(lobby).registerLayout(minigame);

board.applyLayout(player, "lobby");          // switch instantly, any time
board.setWorldLayout("minigame_world", "minigame");  // auto-applied on join & world change
board.unregisterLayout("minigame");          // remove a layout
```

- Applying a layout **replaces** the previous board cleanly (no stale leftover lines).
- Leaving a world-layout world for one with no layout **clears** the board.
- Fires a cancellable [`LayoutApplyEvent`](/wiki/foliaboard/events/#events--hooks) so other plugins can override per rank/region.


## Remembering a player's layout

Optionally persist which layout a player was on, so it's re-applied on their next join with no
join-listener glue. Back the store with anything (a map, a config, a database, a storage plugin):

```java
board.setLayoutStore(new LayoutStore() {
    public CompletableFuture<Void> remember(UUID player, String layout) { return db.putAsync(player, layout); }
    public CompletableFuture<String> lastLayout(UUID player) { return db.getAsync(player); }
});
```

When set, `applyLayout(...)` records the layout name, and FoliaBoard re-applies it on join (unless a
global or per-world layout already drives that player's board).
