---
title: "API reference"
sidebar:
  order: 10
---

## API reference

| Type | Key members |
|---|---|
| `FoliaBoard` | `create(plugin)`, `tab(p)`, `setGlobalTab/clearGlobalTab`, `bossBar(p, id)`, `hideBossBar`, `createBoard(p)`, `createNametag(p)`, `sidebar(p)`, `removeSidebar(p)`, `setGlobalSidebar(provider\|layout)`, `clearGlobalSidebar()`, `registerLayout/unregisterLayout/layout/applyLayout`, `setWorldLayout/clearWorldLayout`, `setLayoutStore`, `nametag(p)`, `belowName()`, `tabList()`, `tabName/resetTabName/tabOrder`, `tabNameFor/resetTabNameFor/perViewerTabSupported`, `tabHeaderFooter/clearTabHeaderFooter`, `addLineProcessor`, `placeholders()`, `stats()`, `close()` |
| `ScoreboardAPI` | `init(plugin)`, `get()`, `shutdown()`, `createBoard(p)`, `createNametag(p)`, `sidebar(p)` |
| `BoardBuilder` | `placeholders(bool)`, `refreshEvery(ticks)`, `title(...)`, `line(...)`, `lineIf(...)`, `lines(...)`, `blankLine()`, `build()` |
| `TabBuilder` / `TabList` / `TabLayout` | `header`, `footer`, `name`, `order`, `orderByPermission`, `placeholders`, `refreshEvery`, `resetOnClose`, `build()`, `refresh()`, `close()` |
| `BossBarBuilder` / `ManagedBossBar` | `text`, `progress`, `color`, `overlay`, `placeholders`, `refreshEvery`, `hideAfter`, `show()`, `refresh()`, `hide()` |
| `Sidebar` | `title(...)`, `line(...)`, `lines(...)`, `removeLine`, `clearLines`, `visible(...)`, `title()`, `lines()`, `lineCount()`, `close()` |
| `NametagBuilder` | `prefix/suffix/color/nametagVisibility/collision`, `tabSort(int)`, `perViewer(resolver)`, `apply()` |
| `Nametag` | `prefix/suffix/color/…`, `perViewer(resolver)`, `apply()`, `remove()` |
| `ScoreObjective` | `title(...)`, `score(player\|entry, v)`, `remove(entry)`, `scoreFor/removeFor(viewer,…)`, `hide()`, `show()` |
| `SidebarProvider` | `title(p)`, `lines(p)`, `visible(p)`, `refreshIntervalTicks()`, `of(...)` |
| `Layout` | `named(name, recipe)`, `applyTo(board, p)` |
| `NumberFormat` | `blank()`, `fixed(c)`, `styled(style)`, `defaultFormat()` |
| `Animations` | `cycle`, `frames`, `scrollText`, `pulseColor`, `typewriter`, `gradientWave`, `blink`, `sequence`, `mini` |
| `Placeholders` | `register(key, fn[, ttl])`, `unregister`, `invalidate`, `forget`, `cachePlaceholderApi`, `convertLegacyColors`, `apply`, `component`, `value` |
| `Text` / `Legacy` | `mini`, `parse`, `cached`, `plain`, `escape`, `toMini` / `toMini`, `strip`, `hasCodes` |
| `AsyncUtil` | `async`, `asyncLater`, `onPlayer`, `global`, `isFolia` |
| events / hooks | `SidebarCreateEvent`, `LayoutApplyEvent`, `LineProcessor` |


## Version support & the honest caveat

- Requires **Paper/Folia 1.20.6+**, **Java 21**. Targets the Mojang-mapped runtime and modern
  per-score display-component packets. **Validated live end-to-end on Folia 1.21.11.**
- The packet layer (`NmsPacketAdapter`) reaches into server internals by reflection, and adapts at
  load to whether score-packet fields are `Optional<…>` or `@Nullable`. It's the **only**
  version-specific file, and it fails **loudly at load** (never mid-game) if a handle can't resolve.
  If a future Minecraft release moves a field or changes a packet's shape, that one file is where you
  adjust it.


## Building from source

```bash
mvn clean package
```

- `foliaboard-core/target/foliaboard-core-1.0.0.jar`, the library (depend on this).
- `foliaboard-demo/target/FoliaBoard-1.0.0.jar`, a standalone demo plugin. Drop it into `plugins/`,
  join, and use `/fbdemo lobby|minigame` to see everything at once. Add `-Dfoliaboard.debug=true` to
  log every scoreboard packet.

See [`foliaboard-demo/.../ExamplePlugin.java`](https://github.com/SpirtySprite/FoliaBoard-API/blob/main/foliaboard-demo/src/main/java/net/foliaboard/example/ExamplePlugin.java)
for a complete, runnable example.
#
