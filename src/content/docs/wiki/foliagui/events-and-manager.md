---
title: "Events and GuiManager"
sidebar:
  order: 7
---

## Custom events

Alongside the per-GUI callbacks (`onOpen`, `onClick`, and so on), FoliaGUI fires three normal Bukkit events so other plugins can observe or react to menu activity without needing direct access to your GUI instances:

```java
@EventHandler
public void onGuiClick(GuiClickEvent event) {
    if (event.getGui() instanceof MyShopGui) {
        // log it, run an anti-cheat check, whatever you need
    }
}
```

`GuiOpenEvent` and `GuiClickEvent` are cancellable and mirror the outcome back onto the underlying `InventoryOpenEvent` or `InventoryClickEvent`. `GuiCloseEvent` is not cancellable, matching vanilla's own `InventoryCloseEvent`.

## GuiManager

A registry, maintained automatically, of who currently has what open:

```java
BaseGui open = GuiManager.getOpenGui(player);
boolean hasOne = GuiManager.hasGuiOpen(player);
int total = GuiManager.openCount();
List<Player> viewers = GuiManager.viewersOf(someGui);
List<BaseGui> shops = GuiManager.openGuisOfType(ShopGui.class);

GuiManager.refresh(someGui);                       // rebuild it for its current viewers
GuiManager.closeAll();                             // everything, e.g. on plugin disable
GuiManager.closeAll(gui -> gui instanceof ShopGui); // just one kind of menu

// true if the player has a Gui, an AnvilGui, a SignGui, a MerchantGui, or a ChatPrompt open, any
// of which would make it a bad time to also open a menu of your own
boolean busy = GuiManager.hasAnyScreenOpen(player);
```

A couple of matching queries live directly on `BaseGui` itself, for when you already hold the instance:

```java
List<Player> viewers = someGui.getViewerPlayers(); // just the real Player viewers, filtered from getViewers()
boolean isThisOneOpen = someGui.isOpenFor(player);
```
