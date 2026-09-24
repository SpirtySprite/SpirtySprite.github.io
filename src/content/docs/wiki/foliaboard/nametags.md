---
title: "Nametags"
sidebar:
  order: 4
---

Control the text around a player's name (above their head **and** in the tab list): prefix, suffix,
name colour, visibility, collision, and tab-list sort, sent as a scoreboard team, so it doesn't fight
Bukkit teams. Updates use team-*modify*, so they never flicker.

```java
board.createNametag(player)
     .prefix("<gold>[VIP] ")
     .suffix(" <gray>★")
     .color(NamedTextColor.YELLOW)
     .tabSort(10)                       // lower sorts higher in the tab list (0, 9999)
     .nametagVisibility(Nametag.Visibility.ALWAYS)
     .collision(Nametag.Collision.NEVER)
     .apply();
```

## Per-viewer nametags

Show a target's name differently to different viewers, classic ally/enemy colouring:

```java
board.createNametag(player)
     .prefix("<gold>[VIP] ")
     .perViewer((viewer, target, style) -> {
         if (areAllies(viewer, target))  style.color(NamedTextColor.GREEN).prefix("<green>✦ ");
         else                            style.color(NamedTextColor.RED).prefix("<red>☠ ");
     })
     .apply();
```

The resolver runs per viewer on that viewer's thread; it starts from the global defaults. Call
`.apply()` again whenever relationships change (e.g. on a timer, or on a team-join event).
