---
title: "Getting started"
sidebar:
  order: 1
---

## Requirements

- **Paper or Folia 1.20.6+** (modern per-score display components).
- **Java 21**.


## Installation

**1. Depend on the core library:**

```xml
	<repositories>
		<repository>
		    <id>jitpack.io</id>
		    <url>https://jitpack.io</url>
		</repository>
	</repositories>

	<dependency>
	    <groupId>com.github.SpirtySprite</groupId>
	    <artifactId>FoliaBoard-API</artifactId>
	    <version>1.1.0</version>
	</dependency>
```

**2. Mark your plugin Folia-ready**, required or it won't load on Folia:

```yaml
name: YourPlugin
main: com.yourplugin.YourPlugin
version: 1.0.0
api-version: '1.20'
folia-supported: true
softdepend: [PlaceholderAPI]   # optional; enables the placeholder bridge
```


## Quick start

Two styles, pick one.

**A. Instance (recommended):**
```java
public final class YourPlugin extends JavaPlugin {
    private FoliaBoard board;

    @Override public void onEnable()  { board = FoliaBoard.create(this); }
    @Override public void onDisable() { if (board != null) board.close(); }
}
```

**B. Static handle** (if you'd rather not pass the instance around):
```java
@Override public void onEnable()  { ScoreboardAPI.init(this); }
@Override public void onDisable() { ScoreboardAPI.shutdown(); }

// anywhere:
ScoreboardAPI.createBoard(player).title("<aqua>Hi").line("<gray>Welcome!").build();
```

All examples below use a `board` (a `FoliaBoard`); with the static handle just write `ScoreboardAPI`
or `ScoreboardAPI.get()`.

Add `import static net.foliaboard.api.text.Text.mini;` (or use `Text.mini(...)`) when you want a
`Component` from a MiniMessage string.
