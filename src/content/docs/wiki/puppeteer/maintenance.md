---
title: "Updates and building"
sidebar:
  order: 6
---

## Updates and metrics

On start Puppeteer checks the latest GitHub release and tells the console and players with
`puppeteer.admin.npc` when a newer version exists. Set `update-checker: false` in `config.yml` to
turn it off. Anonymous usage statistics go through bStats and follow the global bStats opt-out in
`plugins/bStats/config.yml`.

## Building

```bash
mvn package
```

The plugin is in `target/Puppeteer.jar`. Java 21 is required.
