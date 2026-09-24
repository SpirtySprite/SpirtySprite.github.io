---
title: "Developer API"
sidebar:
  order: 5
---

Add Puppeteer as a `depend` or `softdepend`, then get the service:

```java
PuppeteerApi.get().ifPresent(puppeteer -> {
    puppeteer.location("guide").ifPresent(player::teleport);
    puppeteer.setEnabled("banker", false).thenRun(() -> getLogger().info("banker hidden"));
});
```

`PuppeteerApi` lists NPC ids, their state (`ACTIVE`, `PENDING` while the world is not loaded,
`DISABLED`, `UNKNOWN`), their location and click count. `move`, `setEnabled` and `reload` rewrite
`npcs.yml` off the main thread and return a `CompletableFuture`. Unknown ids throw
`IllegalArgumentException`.

`NpcClickEvent` fires when a player clicks an NPC, before its actions run. It carries the NPC id,
the side (`rightClick()`) and `sneaking()`. Cancelling it skips every action of that click.
