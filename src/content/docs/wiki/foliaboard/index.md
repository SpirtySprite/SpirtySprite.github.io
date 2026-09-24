---
title: "FoliaBoard"
description: "Packet-level scoreboards, nametags and tab lists for Paper and Folia."
sidebar:
  order: 0
  label: "Introduction"
---

A **Folia-native, packet-level scoreboard API** for Paper & Folia. It removes the single hardest part
of scoreboards on Folia, knowing *which thread* may touch a player's board and not racing when they
move between regions, and gives you a fluent, MiniMessage-first API where **every call is safe from
any thread**.

```java
FoliaBoard board = FoliaBoard.create(this);

board.createBoard(player)
     .placeholders(true)
     .title("<gradient:#00c6ff:#0072ff><bold>MY SERVER</bold></gradient>")
     .blankLine()
     .lines("<gray>Player: <white>%player%",
            "<gray>Online: <green>%online%",
            "<gray>Ping: <aqua>%ping%ms")
     .blankLine()
     .line("<yellow>play.myserver.net")
     .build();
```

- **Zero threading work.** Call from the main thread, an async task, a region thread, anywhere.
- **Zero third-party deps.** Packets are built and sent directly. No ProtocolLib, no MegaVex.
- **MiniMessage everywhere.** Any `String` argument is parsed as MiniMessage (gradients, hover, click…).
- **Runs on Paper too.** The same jar works on plain Paper (everything just runs on the main thread).
- **Validated live on Folia 1.21.11.**


## Why it exists

Packet scoreboard libraries are excellent but warn that their board/team objects are **not
thread-safe**. On Folia that warning is the whole game: there is no main thread, players tick on
**region threads**, they **migrate** between regions, and join/quit fires on region threads.

FoliaBoard's core idea: confine every mutation of a player's board to that player's
[`EntityScheduler`](https://docs.papermc.io/folia/reference/region-logic), Folia's scheduler that
follows the entity across regions and runs its tasks strictly sequentially. That yields thread-safety
with **zero locks**, and it's all hidden. You describe *what* to show; FoliaBoard handles *where* and
*when* it's safe to send the packets.
