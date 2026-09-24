---
title: "Lifecycle and threading"
sidebar:
  order: 8
---

## Lifecycle

```java
FoliaGUI.init(this);          // once, in onEnable
FoliaGUI.isInitialised();     // true after a successful init
FoliaGUI.shutdown();          // closes every open GUI, clears all registries, unregisters the listener
String version = FoliaGUI.VERSION; // the library's own version, read from its packaged POM
```

`shutdown()` exists so a plugin reload framework (or a test suite) can tear the library down cleanly and call `init()` again afterwards, rather than being stuck with a permanently-initialised singleton.

Calling almost anything in this library before `init` (or after `shutdown`) throws `FoliaGUINotInitialisedException`, a descriptive subclass of `IllegalStateException`, instead of a bare, unexplained one.

If you would rather look the running instance up as a service than depend on the static class directly:

```java
FoliaGUIService service = Bukkit.getServicesManager().load(FoliaGUIService.class);
```

## Threading model

- `open`, `close`, `update`, `updateTitle`, and `updateItem` are safe to call from any thread. They route to the correct region thread internally, and take a fast path that runs immediately when you're already on the right one.
- Direct item mutators (`setItem`, `addItem`, `removeItem`, everything under `filler()`) only touch internal maps. They take effect the next time you call `update()` or `open()`.
- Click, drag, open, and close callbacks fire on the region thread that owns the acting player, so they can safely touch that player and the GUI directly.
- A single GUI instance is meant for one viewer at a time. For a menu shown to many players, build one instance per player.
