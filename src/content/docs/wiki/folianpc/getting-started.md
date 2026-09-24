---
title: "Getting started"
sidebar:
  order: 1
---

## Requirements

- Java 21
- Paper or Folia **1.20.6 or newer**, Mojang-mapped (this is the default for all modern Paper/Folia
  builds; you don't need to do anything special to get it). This includes the calendar-numbered
  releases (26.x): tested on Purpur 26.3, where the position packet now carries a `VecDelta` and team
  colours are set through `TeamColor`; both forms are detected at startup.
- No other plugins, dependencies, or protocol libraries required at runtime

`FoliaNpc.create(plugin)` checks the version at startup and throws `IllegalStateException` immediately
if the server is older than 1.20.6. There's no partial/degraded support for older versions, either the
whole packet layer binds, or NPC creation refuses to start at all. See
FoliaNpc.create() throws IllegalStateException if this
happens on a server you believe meets the requirement.

On 26.x the server no longer exposes its entity-id counter, so FoliaNPC logs one warning at startup and
uses its own counter, placed far above the ids the game hands out. NPC ids never collide with real
entities.

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
	    <artifactId>FoliaNPC-API</artifactId>
	    <version>1.2.1</version>
	</dependency>
```

**2. Mark your plugin Folia-ready**, required or it won't load on Folia:

```yaml
name: YourPlugin
main: com.yourplugin.YourPlugin
version: 1.0.0
api-version: '1.20'
folia-supported: true
```

Use the `maven-shade-plugin` (or the Gradle Shadow plugin) to bundle it into your own jar, FoliaNPC has
no `plugin.yml`, so it cannot be installed as a standalone plugin, and shading it cannot collide with
your own plugin descriptor. If two of your own plugins both shade FoliaNPC, each gets its own
independent copy: they do not share NPCs, view distance, or any other state, because each shaded copy
is a completely separate set of classes to the JVM.

The public API lives entirely in `net.folianpc.api`. The `internal` packages (`net.folianpc.internal.*`)
are marked `@ApiStatus.Internal` and may change shape or behavior between releases without notice, don't call into them directly, and don't rely on anything not exposed through `net.folianpc.api`.

## Quick start

```java
public final class MyPlugin extends JavaPlugin {

    private FoliaNpc npcs;

    @Override
    public void onEnable() {
        npcs = FoliaNpc.create(this);

        npcs.builder()
            .name("Shopkeeper")
            .location(someLocation)
            .lookAtPlayers(true)
            .nametag("<gradient:gold:yellow><bold>Shop</bold></gradient>", "<gray>Right-click me")
            .action(ClickType.RIGHT, Actions.message("<green>Welcome, %player%!"))
            .spawn();
    }

    @Override
    public void onDisable() {
        npcs.close();
    }
}
```

Create exactly **one** `FoliaNpc` instance per plugin, in `onEnable`, and keep it for the plugin's
lifetime. Call `close()` in `onDisable`, this despawns every NPC for every online player, cancels the
internal tick timer, unregisters the join/quit/move listener, and shuts down the skin-fetch HTTP client
and its background thread. Skipping `close()` on a `/reload` leaves stale packet listeners injected into
player connections and a thread pool that never terminates.
