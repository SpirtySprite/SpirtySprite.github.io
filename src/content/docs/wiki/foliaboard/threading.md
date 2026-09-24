---
title: "Threading and performance"
sidebar:
  order: 9
---

## Threading model

- **Public API is callable from any thread.** Mutations to a player's board are queued and applied on
  that player's region thread, in order, so nothing races.
- **On Paper** (non-Folia) everything runs on the main thread, the same code, no branches.
- **You never schedule anything** for scoreboard work. For your own logic, use `AsyncUtil`.

Internally: each `Sidebar` keeps *desired* state (written under a lock from any thread) and *sent*
state (touched only on the region thread inside a debounced flush that diffs and emits minimal
packets).


## Performance

FoliaBoard is built to stay cheap even with many players and fast, animated boards:

- **Minimal packets.** Sidebars diff desired-vs-sent state and send only changed lines. Below-name/tab
  score updates skip the broadcast entirely when the value is unchanged.
- **No re-parsing.** Dynamic placeholder lines cache their parsed MiniMessage and only re-parse when
  the resolved string actually changes.
- **Cheap conversions.** The (very common) empty component, blank spacer lines, empty titles, is
  converted to its vanilla form once and reused. Score-holder names are interned.
- **Fast send path.** Packets go out through cached `MethodHandle`s (with a reflection fallback).
- **No busy loops.** Nothing polls; work is event- and scheduler-driven, and refresh loops stop the
  instant a board closes or a player leaves.

Practical guidance: pick a `refreshEvery(...)` that matches your content, `2, 4` ticks for smooth
animations, `10, 20` for mostly-static boards. Static content isn't refreshed at all.

### Observability

`board.stats()` returns a snapshot for profiling TPS impact:

```java
FoliaBoardStats s = board.stats();
// s.totalPackets(), s.providerRefreshes(), s.activeSidebars(), s.activeNametags()
getLogger().info(s.toString());
```

FoliaBoard also warns (once) when a board exceeds the 15-line client limit or a single line/title is
unusually large (likely accidental payload bloat).


## Lifecycle, cleanup & `/reload`

- Create once in `onEnable`, call `board.close()` in `onDisable`. `close()` cancels every task,
  unregisters the listener, and tears down all boards, nametags and objectives.
- **Auto-cleanup** on quit, world-change and plugin-disable, no ghost players, no leaks.
- **`/reload` is discouraged** (on Paper/Folia generally). Because FoliaBoard registers a listener and
  scheduler tasks, prefer a full restart. A clean disable→enable cycle won't leak (guarded against
  scheduling while disabled), but `/reload` remains unsupported as a reload mechanism.
