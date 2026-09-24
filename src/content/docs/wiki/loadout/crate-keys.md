---
title: "Crate keys as rewards"
sidebar:
  order: 4
---

## Crate keys as rewards

Kits can give keys. They are delivered through a console command, which works with any crate
plugin:

```yaml
crate-keys:
  command: "cle give {player} {crate} {amount}"
  crates:
    common: "<green>Common Crate"
```

The default command is Lootrift's. If `crates` is empty and Lootrift is installed, the crate list
is read straight from `plugins/Lootrift/crates.yml`.

## Differences from the NexusSMP version

Fragment costs and rewards are not available: a kit that costs fragments cannot be claimed. Team
kits behave like personal kits. When the inventory is full, extra items drop at the player's feet.
