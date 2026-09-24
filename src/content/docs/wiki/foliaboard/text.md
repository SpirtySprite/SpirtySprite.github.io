---
title: "Text, animations and placeholders"
sidebar:
  order: 7
---

## MiniMessage & text

`Text` is the one-stop helper.

```java
Component c   = Text.mini("<rainbow>hello</rainbow>");
Component tag = Text.mini("<hover:show_text:'<green>Click!'><click:run_command:/spawn>Spawn</click>");
String    mm  = Text.toMini(someComponent);   // round-trip back to a string
Component any = Text.parse("&6Gold <blue>and blue");   // legacy codes and MiniMessage together
Component hot = Text.cached("&5NEXUS");       // parsed once, reused
String    raw = Legacy.strip("&aHi §lthere");  // "Hi there"
String    safe = Text.escape(userInput);       // cannot inject tags
```

Every `String` argument across the API goes through MiniMessage, so you rarely need `Text` directly.


## Animations

Self-timed, no ticking or registration. Call `current()` and return it; the frame is derived from the
clock.

```java
Animation<Component> title = Animations.cycle(Duration.ofMillis(400),
    mini("<aqua>HUB"), mini("<white>HUB"));

Animation<Component> marquee = Animations.scrollText(Duration.ofMillis(150),
    "welcome to the server!", 24, TextColor.color(0x8AB4F8));

Animation<Component> pulse = Animations.pulseColor(Duration.ofSeconds(2),
    "EVENT LIVE", TextColor.color(0xff0000), TextColor.color(0xffff00));

Animation<Component> typed = Animations.typewriter(Duration.ofMillis(80), Component.text("Loading…"));

Animation<Component> wave = Animations.gradientWave(Duration.ofSeconds(2), "NEXUS",
    TextColor.color(0xb44cff), TextColor.color(0x4cc9ff));

Animation<Component> frames = Animations.frames(Duration.ofMillis(500), "&5NEXUS", "&dNEXUS");
Animation<Component> alert = Animations.blink(Duration.ofMillis(500), mini("<red>!"));
Animation<Component> both = Animations.sequence(List.of(wave, frames), Duration.ofSeconds(5));
Animation<String> upper = frames.map(c -> Text.plain(c).toUpperCase(Locale.ROOT));

// use directly in a builder / layout:
board.createBoard(player).title(title).line(marquee).build();
```

`cycle`, `scrollText`, `pulseColor`, and `typewriter` are code-point safe (won't split emoji).
Animations are global wall-clock phase (every player sees the same frame at the same instant).


## Placeholders

A fast engine that replaces `%tokens%` using, in order: your resolvers → built-ins → PlaceholderAPI
(if installed; bridged reflectively, no hard dependency).

```java
board.placeholders().register("rank",  p -> p.isOp() ? "Admin" : "Member");
board.placeholders().register("coins", p -> economy.balance(p));

String  text = board.placeholders().apply(player, "Rank: %rank%");           // -> "Rank: Admin"
Component c  = board.placeholders().component(player, "<gray>Rank: <gold>%rank%");  // MiniMessage + %papi%
```

**Built-ins:** `%player%` / `%player_name%` / `%name%`, `%displayname%`, `%world%`, `%online%`,
`%max_players%`, `%ping%`, `%health%`, `%level%`, `%gamemode%`, `%x%` / `%y%` / `%z%`.

**Caching.** Expensive values can be cached per player for a duration. PlaceholderAPI results can be
cached the same way. Caches are dropped when the player quits.

```java
board.placeholders().register("balance", p -> economy.format(p), Duration.ofSeconds(2));
board.placeholders().cachePlaceholderApi(Duration.ofSeconds(1));
board.placeholders().invalidate("balance");
```

**Legacy colors.** Values that contain `&a`, `§a`, `&#rrggbb` or `§x§r§r§g§g§b§b` (typical of
PlaceholderAPI expansions and permission prefixes) are rendered as colors instead of raw codes. Turn it
off with `convertLegacyColors(false)`, in which case the codes are stripped.

**No double expansion.** Each `%token%` is resolved once: a value that itself contains `%other%` is
left as is, so a player can't smuggle placeholders through a nickname. PlaceholderAPI is detected
lazily, so it works even when it loads after your plugin. Tokens never contain spaces, so `50% off`
is left alone.

**Injection-safe:** in `component(...)`, placeholder *values* are escaped before parsing, so a value
like a display name containing `<red>` or a PAPI value with `<click:...>` renders literally and can't
inject formatting or click events into your board.

`%built-ins%` such as `%ping%` are cheapest read on the player's own thread, the builder/provider
already do that for you.
