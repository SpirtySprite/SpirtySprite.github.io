---
title: "Events and async utilities"
sidebar:
  order: 8
---

## Events & hooks

**Line processor**, rewrite every line/title of every board just before it's sent:

```java
board.addLineProcessor((viewer, index, line) ->
    index == LineProcessor.TITLE ? line
        : line.decoration(TextDecoration.ITALIC, false));   // e.g. kill stray italics
```

**Bukkit events:**

```java
@EventHandler
public void onCreate(SidebarCreateEvent e) {
    getLogger().info("Board created for " + e.getPlayer().getName());
}

@EventHandler
public void onLayout(LayoutApplyEvent e) {          // cancellable + swappable
    if (e.getPlayer().hasPermission("vip")) e.setLayout(board.layout("vip_lobby"));
}
```

Both fire on the player's region thread (synchronous Folia-safe events).


## Async utilities

Folia-safe helpers for *your* surrounding work (FoliaBoard's own calls are already thread-safe):

```java
AsyncUtil.async(plugin, () -> {                       // off any game thread
    int coins = db.loadCoins(uuid);
    AsyncUtil.onPlayer(plugin, player, () ->           // hop to the player's region thread
        board.createBoard(player).line("<gold>Coins: " + coins).build());
});

AsyncUtil.asyncLater(plugin, task, Duration.ofSeconds(5));
AsyncUtil.global(plugin, () -> { /* global game state */ });
boolean folia = AsyncUtil.isFolia();
```
