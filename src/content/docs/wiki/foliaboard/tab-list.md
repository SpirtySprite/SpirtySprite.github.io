---
title: "Tab list and numbers"
sidebar:
  order: 5
---

## Tab-list header & footer

```java
board.tabHeaderFooter(player,
    "<gradient:#00c6ff:#fff><bold>MY SERVER</bold></gradient>",
    "<gray>Online: <green>" + Bukkit.getOnlinePlayers().size());

board.clearTabHeaderFooter(player);
```

Accepts `String` (MiniMessage) or `Component`. Sent on the player's region thread.

### Tab-list entry styling & sorting

Style how a player appears **in the tab list**, independently of their above-head nametag, and sort
the list, **with no scoreboard team**, so it doesn't conflict with other team-based plugins.

```java
board.tabName(player, "<aqua>★ <white>" + player.getName());  // tab prefix ≠ above-head prefix
board.tabOrder(player, staff ? 100 : 0);                      // higher sorts higher (Paper 1.21.2+)
board.resetTabName(player);                                    // back to the vanilla name

if (!board.tabOrderSupported()) { /* pre-1.21.2: use nametag tabSort instead */ }
```

- **Tab vs. above-head are now separate.** The above-head prefix comes from a [nametag](/wiki/foliaboard/nametags/)
  (a team); the tab prefix comes from `tabName(...)` (no team). Use either or both.
- **Flicker-free, dynamic sorting.** `tabOrder(...)` changes instantly with no team-name trick.
  (On 1.21.1 and older, fall back to nametag `tabSort`.)
- **Team-conflict friendly.** Because tab styling needs no team, a server that already runs a
  team-based nametag/prefix plugin can use FoliaBoard purely for the tab list (and sidebars) without
  fighting over teams. Above-head prefixes still require a team, that's a vanilla limitation, so
  simply don't create FoliaBoard nametags if another plugin owns the above-head text.

`tabName`/`tabOrder` are per-target (shown the same to everyone), built on stable Paper API.

### Per-viewer tab names

To show a target a *different* tab name to *different* viewers, use the packet-level API:

```java
if (board.perViewerTabSupported()) {                 // 1.20.6+ with the player-info packet
    board.tabNameFor(viewer, target, "<red>ENEMY " + target.getName());
    board.resetTabNameFor(viewer, target);           // back to default
}
```

This is a **manual** send (no automatic lifecycle): re-apply it when you need it, e.g. on the
viewer's join or after the server resends player info. It's built on `ClientboundPlayerInfoUpdatePacket`
and **fails safe**, if the server build doesn't support it, `perViewerTabSupported()` returns false
and the calls no-op rather than erroring.

### Managed tab list

`board.tab(player)` builds a tab list that refreshes itself and only resends the parts that changed
(header and footer together, the entry name, the sort order):

```java
board.tab(player)
     .placeholders(true)
     .refreshEvery(20)
     .header(List.of("&5&lNEXUS", "<gray>%online% players online"))
     .footer("<gray>Ping: <white>%ping%ms")
     .name("%luckperms_prefix% <white>%player%")
     .orderByPermission("group.admin", "group.mod", "group.vip")
     .build();
```

For everyone at once, set a global layout. It is applied to online players immediately and to every
player who joins later, and closed on quit:

```java
board.setGlobalTab(TabLayout.of(tab -> tab
        .placeholders(true)
        .header("&5&lNEXUS")
        .footer("<gray>%online% online")
        .name(p -> (p.isOp() ? "<red>" : "<white>") + p.getName())));
board.clearGlobalTab();
```

`resetOnClose(true)` (the default) clears the header, footer and name when the tab closes.


## Below-name & tab-list numbers

Shared objectives that show a number below every player's name, or beside their tab-list entry.

```java
board.belowName().title(mini("<red>❤")).score(player, 20);   // hearts below the name
board.tabList().score(player, player.getPing());             // ping in the tab list

board.belowName().remove(player.getName());                  // remove one entry
board.belowName().hide();                                    // hide for everyone…
board.belowName().show();                                    // …and bring it back
```

### Per-viewer numbers

```java
board.tabList().scoreFor(viewer, target.getName(), value);   // only `viewer` sees this value
board.tabList().removeFor(viewer, target.getName());         // revert to the shared value
```

Quit players are cleaned up automatically (no leaks, no phantom scores).


## Number formats

Control the red score number the client draws on the right of each entry (1.20.3+). Sidebars hide it
by default; override per line or on shared objectives.

```java
NumberFormat.blank();                              // hide it (sidebar default)
NumberFormat.fixed(mini("<red>✖"));                // replace it with any component
NumberFormat.styled(Style.style(NamedTextColor.GOLD));  // keep the number, restyle it
NumberFormat.defaultFormat();                      // the vanilla red number

board.sidebar(player).line(0, mini("<gray>Kills"), NumberFormat.fixed(mini("<red>12")));
```
