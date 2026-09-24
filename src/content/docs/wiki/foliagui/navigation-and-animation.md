---
title: "Navigation, themes and animation"
sidebar:
  order: 5
---

## Navigation and themes

`GuiNavigator` is a small per-player back-stack, so you don't have to hand-wire a "previous screen" button into every menu:

```java
GuiNavigator.open(player, nextMenu); // pushes the player's current GUI, then opens nextMenu
GuiNavigator.back(player);            // pops one level and reopens it, returns false if there's nothing to pop
GuiNavigator.backOrClose(player);     // back, or close when there is no history
GuiNavigator.maxDepth(16);            // history is bounded (32 by default) and never stores a menu twice
```

`GuiTheme` bundles the border, back button, and close button most menus repeat, so you configure the look once:

```java
static final GuiTheme THEME = new GuiTheme()
        .border(() -> ItemBuilder.of(Material.BLACK_STAINED_GLASS_PANE).name(" ").asGuiItem());

Gui gui = Gui.builder().rows(3).title("&8Menu").create();
THEME.applyBorder(gui);
gui.setItem(3, 1, THEME.backButton());       // wired to GuiNavigator.back
gui.setItem(3, 9, THEME.closeButton(gui));   // closes this exact GUI
```

Set a theme once for the whole library with `FoliaGUI.theme(THEME)`. The theme also provides the filler,
the previous and next buttons, the page indicator, the loading and error items and four sounds
(`click`, `success`, `deny`, `page`, each replaceable or `null` to mute):

```java
FoliaGUI.theme(new GuiTheme()
        .filler(() -> ItemBuilder.of(Material.PURPLE_STAINED_GLASS_PANE).name(" ").asGuiItem())
        .pageIndicator(gui -> ItemBuilder.of(Material.BOOK).nameAny("<gold>Page " + gui.getCurrentPage()).asGuiItem())
        .clickSound(new GuiTheme.ThemeSound(Sound.UI_BUTTON_CLICK, 0.4f, 1.5f)));

FoliaGUI.theme().success(player);
```

The previous and next buttons can also be built from the menu they belong to, for example to show the
current page in their lore. They are rebuilt whenever the page changes:

```java
new GuiTheme().nextButtonItem(gui -> ItemBuilder.of(Material.ARROW)
        .nameAny("<yellow>Next page").loreAny("<gray>Page " + gui.getCurrentPage() + " of " + gui.getPagesCount())
        .asGuiItem());
```

## Animation and auto-refresh

For a hand-driven animation loop tied to a GUI and its viewer:

```java
Material[] frames = { Material.WHITE_WOOL, Material.ORANGE_WOOL, Material.MAGENTA_WOOL };
int[] index = {0};

GuiAnimation.play(gui, player, 8, g ->
        g.updateItem(4, ItemBuilder.of(frames[index[0]++ % frames.length]).build()));
```

The animation stops itself automatically once the player is no longer viewing that GUI. For a simpler, ticket-based periodic refresh instead of a manual loop:

```java
gui.setUpdateInterval(20); // rebuild the inventory from the item map once a second while it's open
```

To change content on that same schedule, give the GUI a tick action. It runs on the viewer's thread before
each refresh, and a failing action is logged instead of stopping the refresh:

```java
gui.onTick(20, g -> g.updateItem(4, countdownItem()));
```

## Cycling items

A button that advances through a fixed list of values on every click, for toggles, difficulty levels, and similar settings:

```java
CycleItem<String> mode = CycleItem.of(List.of("On", "Off", "Auto"), state ->
        ItemBuilder.of(Material.LEVER).name("&bMode: " + state).build());

gui.setItem(1, 1, mode.asGuiItem(gui, Slot.of(1, 1)));
```
