---
title: "Nametags"
sidebar:
  order: 6
---

Two different things can appear above an NPC's head, and they are not the same mechanism.

The **vanilla name plate** is drawn by the client purely from the tab-list profile name, it's a single
line, no color/formatting beyond a single team color (see below), and every `PLAYER`-type NPC gets it
automatically the moment it spawns, using whatever `npc.name()` currently is.

A **floating nametag** is a stack of real `text_display` entities, one per line, positioned just above
the NPC's head. This is what you want for color, gradients, multiple lines, or a nametag on a
non-player NPC (mobs have no vanilla name plate of their own worth using).

```java
npc.nametag(List.of(
    "<gradient:gold:yellow><bold>Shopkeeper</bold></gradient>",
    "<gray><italic>Right-click to trade</italic>",
    "&aOpen now"));   // legacy & codes still work
```

Setting a non-empty floating nametag **automatically hides the vanilla plate**, so the two never visibly
overlap or double up. Clearing it with `nametag(List.of())` restores the vanilla plate. If you actually
want both showing at once (unusual, but supported), explicitly call `.nametagVisible(true)` afterwards.

## Why `npc.name()` and the name on the wire can differ

Hiding the vanilla name plate (whether directly via `nametagVisible(false)`, indirectly via setting a
floating nametag, or via `glowColor`/`collidable(false)`, all three of which force a scoreboard team, see [Appearance](/wiki/folianpc/appearance/#appearance)) is implemented with a scoreboard team set to never show its members' name
tags. Scoreboard teams are keyed on the *player name string*. If an NPC were teamed under its own
display name, say, an NPC named `Notch`, a real player actually named Notch would also have their
real nametag hidden as a side effect, which would be a serious, confusing bug. To avoid this entirely,
whenever a team is required the NPC is sent under a unique, id-derived name instead of its display name.
This substitution is entirely internal and never surfaces through the public API, you never see or
need to know the wire name, but it's the reason `npc.name()` (what you set) and the name Mojang's
tab-list/team system actually sees on the wire can differ. `Capabilities.namePlateHiding` reports
whether the underlying team subsystem bound at all on this server.

## Text formatting

Text accepts MiniMessage and legacy codes (`&a`, `§a`, `&#rrggbb`, `§x§r§r§g§g§b§b`) in the same string,
so `&6Gold <bold>and bold` works as expected. This applies everywhere text is accepted (nametag lines,
`Actions.message`, `Actions.title`, `Actions.actionBar`). `Text.escape(...)` neutralises tags in untrusted
input and `Text.plain(...)` flattens a component back to plain text. `Text.mini(...)`,
`Text.legacy(...)`, and `Text.toMini(component)` are available if you want to be explicit rather than
rely on the auto-detection, or need to convert an existing `Component` back into a MiniMessage string
for storage. `Capabilities.richText` reports whether the server can render true Adventure components
(gradients, hover, etc.) client-side; where it can't, formatting degrades to legacy section-sign codes.

## Per-player text and placeholders

Nametag text is resolved **per viewer**, not once globally, so you can wire in PlaceholderAPI or any
resolver of your own:

```java
npcs.placeholders((player, line) -> PlaceholderAPI.setPlaceholders(player, line));
npc.nametag(List.of("<gold>%vault_eco_balance%"));   // resolves differently for each player who sees it
npc.autoRefreshNametag(40);                          // re-resolve and re-send every 40 ticks; 0 disables
```

For the common case there is a ready made resolver: `%player%`, `%online%` and `%world%` are built in,
and PlaceholderAPI is used automatically when it is installed (detected lazily, so load order does not
matter). You can chain your own resolver in front of it:

```java
npcs.placeholderApi();
npcs.placeholderApi((player, line) -> line.replace("%rank%", ranks.of(player)));
```

The resolver function runs on the raw line string *before* MiniMessage/legacy parsing, so placeholder
tokens can themselves contain color codes if your resolver produces them. `refreshNametag()` re-sends
the resolved text to every current viewer without respawning the underlying line entities (cheap, no
flicker); `autoRefreshNametag(ticks)` does the same thing automatically on a repeating timer so a live
value (an economy balance, a countdown, a player's current world) stays current without you having to
remember to call `refreshNametag()` yourself. Passing `0` or less turns automatic refresh back off.

## Background, transparency, shadow and see-through

Every floating line is drawn with the vanilla text display background: black at 25% opacity. A
`NametagStyle` changes that for all lines of an NPC at once:

```java
npc.nametagStyle(NametagStyle.transparent());

npc.nametagStyle(NametagStyle.defaults()
        .withBackground(0x1E1033, 160)
        .withTextOpacity(200)
        .withShadow(true)
        .withSeeThrough(true));

NpcBuilder builder = npcs.builder().nametagStyle(NametagStyle.transparent());
```

| Method | Default | Effect |
|---|---|---|
| `withBackground(argb)` | `0x40000000` | full ARGB background, `0` for none |
| `withBackground(rgb, alpha)` | | same, with the alpha given separately and clamped to 0..255 |
| `withTextOpacity(opacity)` | `255` | text alpha, clamped to 0..255 |
| `withShadow(boolean)` | `false` | text shadow |
| `withSeeThrough(boolean)` | `false` | lines stay visible through walls |

Changing the style only re-sends the line metadata to current viewers: no respawn, no flicker, and
setting the style an NPC already has sends nothing. The style is kept by `copy(...)` and by `NpcData`,
and it applies to lines added later too. The client discards text whose alpha is below about 26, so any
text opacity in that range renders as fully hidden rather than faint. The style fields are optional
on the protocol side, like the rest of the nametag support: a server build missing them still shows the
text with vanilla styling.
