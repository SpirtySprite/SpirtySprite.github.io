---
title: "Layout and interaction"
sidebar:
  order: 3
---

## Layout filler

`gui.filler()` gives you a handful of helpers for painting decoration without touching real content slots. Each one only fills slots that are still empty:

```java
gui.filler().fill(pane);                    // every empty slot
gui.filler().fillBorder(pane);               // just the outer ring
gui.filler().fillTop(pane);                  // top row
gui.filler().fillBottom(pane);               // bottom row
gui.filler().fillRow(3, pane);
gui.filler().fillColumn(5, pane);
gui.filler().fillBetween(10, 20, pane);      // inclusive flat-slot range
gui.filler().fillCorners(pane);              // just the four corner slots

gui.filler().pattern(
        Map.of('X', border, 'O', center),
        "XXXXXXXXX",
        "X       X",
        "XXXXOXXXX");
```

## Interaction modifiers

By default, every `Gui` blocks all item movement so its layout can't be disturbed. Relax individual rules when you need to:

```java
Gui gui = Gui.builder()
        .rows(3)
        .title("&8Half-locked")
        .enableInteraction(InteractionModifier.PREVENT_ITEM_TAKE) // allow taking items out
        .create();
```

The six modifiers are `PREVENT_ITEM_PLACE`, `PREVENT_ITEM_TAKE`, `PREVENT_ITEM_SWAP`, `PREVENT_ITEM_DROP`, `PREVENT_ITEM_DRAG`, and `PREVENT_OTHER_ACTIONS`. `StorageGui` clears all of them for you.

One important detail: a slot holding a `GuiItem` (a button, a piece of border decoration) is **always** protected from being taken, swapped, dropped, or dragged, no matter what the modifiers say. The modifiers only govern truly empty slots, which is what makes `StorageGui`'s free area work while its border decoration stays put. If you want a specific `GuiItem` to be movable anyway (a claimable reward, a pre-filled trade slot), call `.editable(true)` on it.

## Click types, cooldowns, and permissions

`GuiItem` supports more than one flat action:

```java
GuiItem item = ItemBuilder.of(Material.NOTE_BLOCK).name("&dClick me").asGuiItem();

item.onLeftClick(event -> player.sendMessage("Left click"));
item.onRightClick(event -> player.sendMessage("Right click"));
item.onShiftClick(event -> player.sendMessage("Shift click"));
item.onNumberKey(event -> player.sendMessage("Hotbar swap key pressed"));

item.cooldown(20); // a fast repeat click within 20 ticks is dropped, not just delayed
item.onCooldownBlocked(event -> player.sendMessage("&cSlow down!")); // fires instead, while on cooldown

item.requirePermission("myplugin.use", denied ->
        denied.sendMessage("You don't have permission for that."));
```

Cooldowns are tracked per player, so a shared item such as a close button reused across menus never
blocks one player because another one clicked it. `remainingCooldownMillis(uuid)` tells you how long is
left.
