---
title: "Earning keys"
sidebar:
  order: 3
---

Besides `/cle give`, keys can come on their own. In `config.yml`:

```yaml
key-sources:
  playtime:
    enabled: true
    every-minutes: 60
    crate: common
    amount: 1
  drops:
    - trigger: kill
      target: ZOMBIE
      chance: 0.5%
      crate: common
    - trigger: mine
      target: DIAMOND_ORE
      chance: 2%
      crate: rare
```

- `playtime` gives keys to every online player after each `every-minutes` of play.
- `drops` roll a chance on each kill (`target` is an entity type) or each block mined (`target` is a
  block), and `*` matches anything. Blocks broken in creative mode never drop keys.
- Votes: point your vote plugin's reward command at `cle give %player% vote 1`.

`/crate reload` applies changes to these sources right away.
