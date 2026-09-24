---
title: "Updates and building"
sidebar:
  order: 7
---

## Updates and metrics

On start Lootrift checks the latest GitHub release and tells the console and players with
`lootrift.admin.crates` when a newer version exists. Set `update-checker: false` in `config.yml` to
turn it off. Anonymous usage statistics go through bStats and follow the global bStats opt-out in
`plugins/bStats/config.yml`.

## Building

```bash
mvn package
```

The plugin is built to `target/Lootrift.jar`. Java 21 is required.
