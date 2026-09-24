---
title: "Developer API"
sidebar:
  order: 6
---

Add Lootrift as a `depend` or `softdepend`, then get the service:

```java
LootriftApi.get().ifPresent(lootrift -> {
    lootrift.giveKeys(player.getUniqueId(), "rare", 3);
    int keys = lootrift.keys(player.getUniqueId(), "rare");
    lootrift.open(player, "rare");
});
```

`LootriftApi` covers crate ids, virtual keys (read, give, take, set), physical keys, opening
counts, opening a crate with the usual animation and opening the preview. Unknown crates and
non-positive amounts throw `IllegalArgumentException`.

Events:

| Event | When |
|---|---|
| `CrateOpenEvent` | before a key is used, cancellable, `openings()` is above 1 for bulk openings |
| `CrateRewardEvent` | after each reward is delivered, with crate, reward id, rarity, amount and money |
