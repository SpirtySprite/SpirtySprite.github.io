---
title: "Boss bars"
sidebar:
  order: 6
---

Per-player boss bars with placeholders, a dynamic progress and color, and an optional lifetime.
Bars are keyed by an id: showing a new bar with the same id replaces the old one.

```java
board.bossBar(player, "double-xp")
     .placeholders(true)
     .text("<gold>XP x2 <gray>ends in <white>%event_remaining%")
     .progress(p -> events.remainingRatio())
     .color(BossBar.Color.YELLOW)
     .refreshEvery(20)
     .hideAfter(20 * 60 * 5)
     .show();

board.hideBossBar(player, "double-xp");
```

Progress is clamped to 0..1 (NaN becomes 0). Bars are hidden automatically when the player quits.
