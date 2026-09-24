---
title: "Crate keys as rewards"
sidebar:
  order: 4
---

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
