---
title: "Menu types"
sidebar:
  order: 2
---

## Basic GUI

`Gui` is a plain chest-style menu, sized by row count (1 to 6):

```java
Gui gui = Gui.builder()
        .rows(3)
        .title("&8Menu")
        .onOpen(event -> player.sendMessage("Opened!"))
        .onClose(event -> player.sendMessage("Closed!"))
        .create();

gui.setItem(1, 1, ItemBuilder.of(Material.PAPER).name("&fHello").asGuiItem());
gui.addItem(ItemBuilder.of(Material.EMERALD).asGuiItem()); // fills the next empty slot
gui.removeItem(1, 1);
gui.updateItem(4, ItemBuilder.of(Material.GOLD_INGOT).build()); // pushes to viewers immediately
```

## Typed GUIs

Non-chest inventory shapes are available through `GuiType`:

```java
Gui gui = Gui.builder()
        .type(GuiType.HOPPER) // also WORKBENCH, DISPENSER, BREWING
        .title("&6A Hopper Window")
        .create();
```

## Paginated GUI

Static items placed with `setItem` stay on every page. Items added with `addPageItem` flow through whatever slots are left empty, and are paged automatically:

```java
PaginatedGui gui = PaginatedGui.builder()
        .rows(6)
        .title("&8Shop")
        .create();

gui.setItem(6, 3, ItemBuilder.of(Material.ARROW).name("&aPrevious")
        .asGuiItem(event -> gui.previous()));
gui.setItem(6, 7, ItemBuilder.of(Material.ARROW).name("&aNext")
        .asGuiItem(event -> gui.next()));

for (Material material : Material.values()) {
    if (material.isItem()) {
        gui.addPageItem(ItemBuilder.of(material).name("&f" + material.name()).asGuiItem());
    }
}

gui.open(player);          // opens on the current page
gui.open(player, 3);       // or jump straight to page 3
gui.openLastPage();        // or jump to whatever the last page turns out to be
gui.promptJumpToPage(player); // ask via chat for a page number and jump there
```

Instead of wiring arrows by hand, let the GUI place themed controls: previous in the first column of the
bottom row, a page indicator in the middle and next in the last column. Unavailable arrows show the
theme filler, and the controls are only rebuilt when the page or the page count changes:

```java
PaginatedGui gui = PaginatedGui.builder().rows(6).title("&8Shop").pageControls(true).create();
gui.pageControls(previousSlot, indicatorSlot, nextSlot); // or pick the slots yourself
gui.hideUnavailableControls(false);                        // always show both arrows
```

## Filtering and sorting pages

`view(...)` turns a list of your own objects into pages and lets you filter and sort without rebuilding
the menu. Only the items on the visible page are rendered:

```java
PageView<Listing> view = gui.view(listings, listing -> listing.icon());
view.filter(listing -> listing.price() <= budget);
view.sort(Comparator.comparingDouble(Listing::price));
view.entries(freshListings);   // swap the data, keeps the filter and sort
view.filter(null);             // clear the filter
```

## Searchable paginated GUI

`SearchablePaginatedGui` keeps a master list of items separate from what's currently displayed, so it can filter down to whatever matches a search term:

```java
SearchablePaginatedGui gui = new SearchablePaginatedGui(6, Text.of("&8Items"), 0);

for (Material material : Material.values()) {
    if (material.isItem()) {
        gui.addSearchableItem(ItemBuilder.of(material).asGuiItem(), material.name());
    }
}

gui.setItem(6, 5, ItemBuilder.of(Material.COMPASS).name("&eSearch")
        .asGuiItem(event -> gui.promptSearch((Player) event.getWhoClicked())));
```

Clicking the compass calls `promptSearch`, which uses [chat text input](/wiki/foliagui/dialogs-and-input/#chat-text-input) to ask for a term, then filters the list down to matches. Search `"clear"` to reset it. The matching logic is a case-insensitive substring match by default and can be overridden with `.matcher(BiPredicate<GuiItem, String>)`.

## Scrolling GUI

Unlike `PaginatedGui`, which jumps a whole page at a time, `ScrollingGui` slides its content one row or column at a time, filling whatever slots are left empty:

```java
ScrollingGui gui = ScrollingGui.builder()
        .rows(6)
        .title("&8Warps")
        .scrollType(ScrollType.VERTICAL) // or HORIZONTAL
        .create();

gui.filler().fillColumn(9,
        ItemBuilder.of(Material.BLACK_STAINED_GLASS_PANE).name(" ").asGuiItem());

warps.forEach(warp -> gui.addContent(
        ItemBuilder.of(Material.ENDER_PEARL).name("&a" + warp.name())
                .asGuiItem(event -> warp.teleport((Player) event.getWhoClicked()))));

gui.setItem(6, 9, ItemBuilder.of(Material.ARROW).name("&aScroll down")
        .asGuiItem(event -> gui.scrollNext()));

gui.open(player);
gui.scrollToEnd(); // or jump straight to the last window of content
```

## Storage GUI

A chest-like menu where players can freely deposit and withdraw items. All interaction modifiers are cleared by default, unlike a plain `Gui`, which locks everything down:

```java
StorageGui gui = StorageGui.builder()
        .rows(3)
        .title("&8Deposit box")
        .onClose(event -> {
            StorageGui closed = (StorageGui) event.getInventory().getHolder();
            persist(event.getPlayer().getUniqueId(), closed.getStoredItems());
        })
        .create();

gui.open(player);
```
