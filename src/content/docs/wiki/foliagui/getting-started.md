---
title: "Getting started"
sidebar:
  order: 1
---

## Requirements

- Java 21 or newer
- Folia or Paper, version 1.21.x


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
	    <artifactId>FoliaGUI-API</artifactId>
	    <version>1.1.1</version>
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

This library ships no `plugin.yml`, so it needs to end up on your plugin's classpath somehow. Two options:

1. **Shade it into your plugin jar** with the Maven Shade plugin. If you do this, relocate the `com.foliagui` package to something unique to your plugin (for example `com.yourplugin.libs.foliagui`). FoliaGUI keeps a small amount of process-wide state (the registered listener, the open-GUI registry). If two plugins on the same server both shade in an *unrelocated* copy, they will fight over that state and one of them will end up initialised against the wrong plugin instance.
2. **Ship it as its own library plugin** that calls `FoliaGUI.init(this)` in its `onEnable`, and have your other plugins depend on it via `depend` or `softdepend` in their own `plugin.yml`.

## Quick start

Initialise once, in your plugin's `onEnable`:

```java
public final class MyPlugin extends JavaPlugin {

    @Override
    public void onEnable() {
        FoliaGUI.init(this);
    }

    @Override
    public void onDisable() {
        FoliaGUI.shutdown();
    }
}
```

Build a menu and open it. Every method below is safe to call from any thread:

```java
Gui gui = Gui.builder()
        .rows(3)
        .title("&8Main Menu")
        .create();

gui.filler().fillBorder(
        ItemBuilder.of(Material.GRAY_STAINED_GLASS_PANE).name(" ").asGuiItem());

gui.setItem(2, 5, ItemBuilder.of(Material.DIAMOND)
        .name("&bClick me")
        .lore("&7A shiny reward")
        .glow(true)
        .asGuiItem(event -> {
            Player player = (Player) event.getWhoClicked();
            player.sendMessage("You clicked the diamond!");
        }));

gui.open(player);
```
