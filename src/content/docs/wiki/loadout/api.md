---
title: "Developer API"
sidebar:
  order: 6
---

Add Loadout as a `depend` or `softdepend`, then get the service:

```java
LoadoutApi.get().ifPresent(loadout -> {
    if (loadout.available(player, "daily")) {
        loadout.claim(player, "daily");
    }
    loadout.giveVouchers(player, "vip", 1);
});
```

`LoadoutApi` covers kit ids, availability, cooldowns, use counts, claiming with every rule applied,
giving a kit while skipping the rules, vouchers, resets and opening the menu or a preview. Unknown
kits and non-positive amounts throw `IllegalArgumentException`.

Events:

| Event | When |
|---|---|
| `KitClaimEvent` | before anything is paid or given, cancellable, with the kit, the source and the price |
| `KitClaimedEvent` | after the kit was delivered, with the items given and the new mastery level |

The source is one of `menu`, `command`, `voucher`, `gift`, `first-join`, `respawn`, `bulk` or
`admin`.
