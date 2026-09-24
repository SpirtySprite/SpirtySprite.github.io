---
title: "Dialogs and text input"
sidebar:
  order: 4
---

## Confirmation and alert dialogs

A ready-made yes/no menu:

```java
Confirmation.builder()
        .title("&8Reset your stats?")
        .onConfirm(player -> {
            resetStats(player);
            player.sendMessage("&aDone.");
        })
        .onCancel(player -> player.sendMessage("&7Cancelled."))
        .expireAfter(20 * 10, player -> player.sendMessage("&cTimed out.")) // optional, in ticks
        .open(player);
```

A confirmation runs `onConfirm` or `onCancel` exactly once, even if the player double clicks before the
menu closes, so it is safe in front of purchases.

`Alert` is the single-button counterpart, for a message that just needs acknowledging rather than a choice:

```java
Alert.builder()
        .title("&8Maintenance notice")
        .onAcknowledge(player -> player.sendMessage("&7Thanks for reading."))
        .open(player);
```

## Force-open dialogs

For a dialog the player must explicitly resolve rather than dismiss with Escape:

```java
Gui dialog = Confirmation.builder()
        .title("&8You must choose one")
        .onConfirm(player -> player.sendMessage("Confirmed."))
        .onCancel(player -> player.sendMessage("Cancelled."))
        .build();
dialog.setForceOpen(true);
dialog.open(player);
```

Closing the dialog through your own code (`gui.close(player)`, which is exactly what the confirm and cancel buttons do internally) still works normally. Only a player closing it themselves (Escape, an inventory swap) triggers the reopen.

## Loading content asynchronously

`AsyncContent` opens a GUI immediately (so the player isn't left waiting on a frozen screen), fetches data off the main thread, then swaps it in once ready, hopping back to the player's region thread automatically:

```java
Gui gui = Gui.builder().rows(3).title("&8Leaderboard").create();

AsyncContent.load(gui, player,
        () -> fetchTopPlayersFromDatabase(), // runs off-thread
        results -> {                          // runs back on the player's region thread
            for (int i = 0; i < results.size(); i++) {
                gui.setItem(i, ItemBuilder.skull().owner(results.get(i)).asGuiItem());
            }
            gui.update();
        });
```

While loading, the centre slot shows the theme's loading item. If the fetch throws, the failure is logged,
the centre slot shows the theme's error item and the optional error callback runs:

```java
AsyncContent.load(gui, player, this::fetch, this::render, failure -> player.sendMessage("Try again later."));
AsyncContent.loadPages(paginatedGui, player, () -> database.listings(), Listing::icon);
```

## Quantity picker

A ready made amount selector with -64, -10, -1, +1, +10, +64, a live preview and confirm or cancel:

```java
QuantityGui.builder()
        .title("&8How many?")
        .display(new ItemStack(Material.DIAMOND))
        .range(1, 256)
        .initial(1)
        .description(amount -> List.of("&7Price: &6" + amount * 50))
        .onConfirm(amount -> buy(player, amount))
        .open(player);
```

## Anvil text input

A virtual anvil used purely as a text prompt, with no NMS or packet libraries involved:

```java
AnvilGui.builder()
        .title("&8Name your pet")
        .text("Fluffy")
        .onComplete((player, input) -> {
            if (input.isBlank()) {
                return AnvilGui.Response.text("&cType something!");
            }
            player.sendMessage("Named: " + input);
            return AnvilGui.Response.close();
        })
        .onClose(player -> player.sendMessage("Naming cancelled"))
        .open(player);
```

`Response.text(...)` keeps the dialog open and replaces the input field, which is how you show a validation hint. `Response.keepOpen()` leaves it untouched, and `Response.close()` ends the dialog.

Add `.forceOpen(true)` to the builder if the player must submit or explicitly cancel rather than dismiss the anvil with Escape; closing it any other way reopens it automatically, the same way [force-open dialogs](/wiki/foliagui/dialogs-and-input/#force-open-dialogs) work for regular menus.

## Sign text input

`SignGui` is the same idea as `AnvilGui`, a 4-line text prompt, but built on Paper's virtual sign packets (`Player#openVirtualSign`) instead of a fake anvil inventory. Set all 4 lines at once with `.lines(...)`, or just one with `.line(lineNumber, text)` (1-4) without touching the others:

```java
SignGui.builder()
        .line(1, "&8Type your pet's name below")
        .onComplete((player, lines) -> {
            String name = lines.get(1);
            if (name.isBlank()) {
                player.sendMessage("&cYou didn't type anything.");
                return;
            }
            player.sendMessage("Named: " + name);
        })
        .open(player);
```

A few things behave differently here than with `AnvilGui`, because a sign isn't an inventory:

- **A sign block is genuinely rendered**, faked client-side only for that one player via `sendBlockChange`, at a `Location` you can override with `.position(...)`. By default it's placed 3 blocks beneath the player's feet so solid ground blocks it from view; standing over an open cave, glass floor, or in the air will expose it. Nothing is placed in the real world, no other player ever sees it, and the original block is restored once the dialog ends.
- **Lines that come back unchanged are blanked out.** Whatever you passed to `.lines(...)` is compared against what the player submitted; a line the player left untouched comes back as `""` in the callback instead of your placeholder text, so `onComplete` only reflects what was actually typed or changed.
- **There's no reliable "player pressed Escape" signal** the way `AnvilGui` gets one from `InventoryCloseEvent`, so there's no `onClose` or `forceOpen` here. Instead, `.timeout(ticks)` (default 60 seconds, `0` disables it) auto-reverts the fake sign and drops the session if the player never submits, so it doesn't linger client-side forever.
- **Built on `@ApiStatus.Experimental` Paper API** (`UncheckedSignChangeEvent`), which may change between Paper releases.

## Chat text input

For text longer than an anvil's rename field comfortably shows, `ChatPrompt` closes whatever GUI the player has open, listens for their next chat line, and hands it to a callback:

```java
ChatPrompt.ask(player, "&eType a description, or 'cancel':", 20 * 30, input -> {
    if (input == null) {
        player.sendMessage("Timed out.");
        return;
    }
    player.sendMessage("You wrote: " + input);
});
```

The chat message is cancelled so it never reaches the server's chat log, and the callback runs back on the player's own region thread even though chat events fire off it. Pass `0` as the timeout to wait indefinitely.

## Merchant trade window

A real villager trade window, backed by `Bukkit.createMerchant`, with your own recipes instead of a real villager:

```java
MerchantGui.builder()
        .title("&2Blacksmith")
        .addRecipe(new ItemStack(Material.DIAMOND_SWORD), List.of(new ItemStack(Material.EMERALD, 5)))
        .onTrade((player, recipe) -> player.sendMessage("Thanks for your business!"))
        .onClose(player -> player.sendMessage("Come back soon."))
        .open(player);
```

Vanilla trading mechanics (taking ingredients, giving the result) run exactly as they would with a real villager. `onTrade` fires once vanilla has already applied the trade.
