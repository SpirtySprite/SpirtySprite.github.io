---
title: "Reloading and building"
sidebar:
  order: 7
---

## Reloading, updates and metrics

`/kit reload` rereads `config.yml`, the language files and `kits.yml`. Changing `language` takes
full effect after a restart.

On start Loadout checks the latest GitHub release and tells the console and players with
`loadout.admin.kits` when a newer version exists. Set `update-checker: false` in `config.yml` to
turn it off. Anonymous usage statistics go through bStats and follow the global bStats opt-out in
`plugins/bStats/config.yml`.

## Building

```bash
mvn package
```

The plugin is built to `target/Loadout.jar`. Java 21 is required.
