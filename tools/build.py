import hashlib
import html
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1])
FONTS = ("https://fonts.googleapis.com/css2?family=Anybody:wdth,wght@50..150,300..900"
         "&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&family=Silkscreen&display=swap")
HLJS = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"
GH = "https://github.com/SpirtySprite/"


def stamp(name):
    return hashlib.sha1((OUT / "assets" / name).read_bytes()).hexdigest()[:10]


CSS = "/assets/site.css?v=" + stamp("site.css")
JS = "/assets/site.js?v=" + stamp("site.js")

ORES = {
    "lapis": "#3d6be0", "emerald": "#22a565", "copper": "#cc7440", "amethyst": "#9563d6",
    "redstone": "#d5412f", "gold": "#d9a22b", "prismarine": "#2fa597",
}

ICONS = {
    "foliagui": ["dd.dd.dd", "dd.dd.dd", "........", "dd.ww.dd", "dd.ww.dd", "........", "dd.dd.dd", "dd.dd.dd"],
    "foliaboard": ["aaaaaaaa", "awwwwwwa", "adddddda", "alllddwa", "alllldwa", "alldddwa", "adddddda", "aaaaaaaa"],
    "folianpc": ["dddddddd", "dddddddd", "llllllll", "lwkllkwl", "llllllll", "lllddlll", "llaaaall", "llllllll"],
    "itemsmith": ["........", "llllllll", "aaaaaaaa", "..aaaa..", "...aa...", "..dddd..", ".dddddd.", "........"],
    "puppeteer": ["dddddddd", ".w.ww.w.", ".w.ll.w.", ".aaaaaa.", "...aa...", "...aa...", "..a..a..", "..a..a.."],
    "lootrift": ["........", "dddddddd", "dlllllld", "dddwwddd", "daaaaaad", "daaaaaad", "dddddddd", "........"],
    "loadout": ["aa....aa", "aaa..aaa", "aaallaaa", ".aaaaaa.", ".aaaaaa.", ".adaada.", ".aaaaaa.", ".dddddd."],
}


def mix(color, other, amount):
    a = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * amount):02x}" for x, y in zip(a, b))


def pixel(slug, ore, size="", label=""):
    base = ORES[ore]
    fills = {"a": base, "d": mix(base, "#000000", 0.38), "l": mix(base, "#ffffff", 0.38),
             "w": "#f4f1ea", "k": "#1a1b1f"}
    rects = []
    for y, row in enumerate(ICONS[slug]):
        for x, cell in enumerate(row):
            if cell in fills:
                rects.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{fills[cell]}"/>')
    role = f'role="img" aria-label="{html.escape(label)}"' if label else 'aria-hidden="true"'
    return (f'<svg class="pixel {size}" viewBox="0 0 8 8" shape-rendering="crispEdges" {role}>'
            + "".join(rects) + "</svg>")


def esc(text):
    return html.escape(text, quote=False)


def p(text):
    return f"<p>{text}</p>"


def ul(items):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def grid(items):
    return '<div class="grid-list">' + "".join(
        f"<div><b>{title}</b><span>{body}</span></div>" for title, body in items) + "</div>"


def code(lang, label, body):
    return (f'<div class="code"><div class="code-bar"><span>{esc(label)}</span>'
            f'<button class="copy" type="button">Copy</button></div>'
            f'<pre><code class="language-{lang}">{esc(body.strip())}</code></pre></div>')


def table(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table class="table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def note(text):
    return f'<p class="note">{text}</p>'


def maven(artifact, version):
    return code("xml", "pom.xml", f"""
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>

<dependency>
    <groupId>com.github.SpirtySprite</groupId>
    <artifactId>{artifact}</artifactId>
    <version>{version}</version>
</dependency>""")


def gradle(artifact, version):
    return code("kotlin", "build.gradle.kts", f"""
repositories {{
    maven("https://jitpack.io")
}}

dependencies {{
    implementation("com.github.SpirtySprite:{artifact}:{version}")
}}""")


FOLIA_YML = code("yaml", "plugin.yml", """
name: YourPlugin
main: com.yourplugin.YourPlugin
version: 1.0.0
api-version: '1.21'
folia-supported: true""")


def relocate(package, target):
    return code("xml", "maven-shade-plugin", f"""
<relocation>
    <pattern>{package}</pattern>
    <shadedPattern>com.yourplugin.libs.{target}</shadedPattern>
</relocation>""")


PROJECTS = [
    {
        "slug": "foliagui", "name": "FoliaGUI", "ore": "lapis", "kind": "Library",
        "repo": "FoliaGUI-API", "version": "1.1.1",
        "tagline": "Inventory menus you can open, update and animate from any thread, on Folia and Paper.",
        "card": "Menus, pages, dialogs and text input with one fluent API. Every inventory call is routed to the right region thread for you.",
        "facts": [("Version", "1.1.1"), ("Java", "21"), ("Runs on", "Paper and Folia 1.21"), ("Dependencies", "none")],
        "sections": [
            ("overview", "Overview", [
                p("FoliaGUI is a pure library: no commands, no <code>plugin.yml</code>, no config file. You add it as a "
                  "dependency, call <code>FoliaGUI.init(this)</code> once and build menus with a fluent API."),
                p("Every operation that touches an inventory (open, close, update, title change, animation) goes "
                  "through a Folia-safe scheduler. The same code runs under Folia's regionised threading and on "
                  "classic single-threaded Paper."),
            ]),
            ("features", "What's inside", [grid([
                ("Paginated, scrolling, storage", "Pages with filters and sorting, searchable lists, scrolling rows, free storage slots."),
                ("Dialogs", "Confirmation and alert dialogs, quantity picker, force-open prompts."),
                ("Text input", "Anvil, sign and chat input, each with a callback on the right thread."),
                ("Merchant windows", "Villager trade screens built from your own offers."),
                ("Async loading", "Show a placeholder, fill the menu when your data arrives."),
                ("Animation", "Auto-refresh, cycling items and animated titles."),
                ("Navigation and themes", "Back buttons, breadcrumbs and one theme for every menu of your plugin."),
                ("Item builders", "Names, lore, NBT, enchantments, attributes, heads, and item stack save and load."),
            ])]),
            ("install", "Install", [
                p("FoliaGUI is published through JitPack."),
                maven("FoliaGUI-API", "1.1.1"), gradle("FoliaGUI-API", "1.1.1"),
                p("Mark your plugin Folia-ready, or it won't load on Folia:"), FOLIA_YML,
                p("Shade it into your jar and relocate it. FoliaGUI keeps a little process-wide state (its listener "
                  "and the open-menu registry), so two plugins shading an unrelocated copy would fight over it."),
                relocate("com.foliagui", "foliagui"),
            ]),
            ("quick-start", "Quick start", [
                code("java", "MyPlugin.java", """
public final class MyPlugin extends JavaPlugin {

    @Override
    public void onEnable() {
        FoliaGUI.init(this);
    }

    @Override
    public void onDisable() {
        FoliaGUI.shutdown();
    }
}"""),
                p("Build a menu and open it. Every call below is safe from any thread:"),
                code("java", "Menu.java", """
Gui gui = Gui.builder()
        .rows(3)
        .title("<dark_gray>Main Menu")
        .create();

gui.filler().fillBorder(
        ItemBuilder.of(Material.GRAY_STAINED_GLASS_PANE).name(" ").asGuiItem());

gui.setItem(2, 5, ItemBuilder.of(Material.DIAMOND)
        .name("<aqua>Click me")
        .lore("<gray>A shiny reward")
        .glow(true)
        .asGuiItem(event -> event.getWhoClicked().sendMessage("You clicked the diamond!")));

gui.open(player);"""),
            ]),
            ("threading", "Threading model", [ul([
                "<code>open</code>, <code>close</code>, <code>update</code>, <code>updateTitle</code> and "
                "<code>updateItem</code> are safe from any thread, with a fast path when you are already on the right one.",
                "Item mutators like <code>setItem</code> and <code>filler()</code> only touch an internal map. They show up on "
                "the next <code>update()</code> or <code>open()</code>, so a full screen redraws once.",
                "Click, drag, open and close callbacks fire on the region thread that owns the player, so they can "
                "touch that player and the menu directly.",
                "One menu instance per viewer. For a menu shown to many players, build one per player.",
            ])]),
        ],
    },
    {
        "slug": "foliaboard", "name": "FoliaBoard", "ore": "emerald", "kind": "Library",
        "repo": "FoliaBoard-API", "version": "1.1.0",
        "tagline": "Packet-level sidebars, nametags, tab lists and boss bars. Every call is safe from any thread.",
        "card": "Per-player scoreboards and tab lists without ProtocolLib. It confines each board to its player's thread, so nothing races.",
        "facts": [("Version", "1.1.0"), ("Java", "21"), ("Runs on", "Paper and Folia 1.20.6+"), ("Dependencies", "none")],
        "sections": [
            ("overview", "Overview", [
                p("Packet scoreboard libraries warn that their objects are not thread-safe. On Folia that is the whole "
                  "problem: there is no main thread, players tick on region threads, they migrate between regions, and "
                  "join and quit fire on region threads too."),
                p("FoliaBoard confines every change to a player's board to that player's <code>EntityScheduler</code>, "
                  "which follows the player across regions and runs tasks strictly in order. That gives thread-safety "
                  "with zero locks. You describe what to show; FoliaBoard decides where and when the packets go out."),
            ]),
            ("features", "What's inside", [grid([
                ("Sidebars", "Fluent builder, manual control, one global provider, or one global layout with per-player content."),
                ("Layout profiles", "Swap a player's whole sidebar in one call and remember it across sessions."),
                ("Nametags", "Prefix, suffix and colour per team, or per viewer when each player should see something else."),
                ("Tab list", "Header, footer, entry names, sorting and a fully managed tab list."),
                ("Numbers", "Below-name and tab-list numbers, with number formats."),
                ("Boss bars", "Per-player boss bars with the same MiniMessage text."),
                ("Animations and placeholders", "Animated lines, a PlaceholderAPI bridge and built-in placeholders."),
                ("Observability", "Events, hooks and counters to see what is sent and when."),
            ])]),
            ("install", "Install", [
                maven("FoliaBoard-API", "1.1.0"), gradle("FoliaBoard-API", "1.1.0"),
                p("Mark your plugin Folia-ready. Add <code>softdepend: [PlaceholderAPI]</code> to enable the placeholder bridge."),
                FOLIA_YML,
                relocate("net.foliaboard", "foliaboard"),
            ]),
            ("quick-start", "Quick start", [
                code("java", "Sidebar.java", """
FoliaBoard board = FoliaBoard.create(this);

board.createBoard(player)
     .placeholders(true)
     .title("<gradient:#00c6ff:#0072ff><bold>MY SERVER</bold></gradient>")
     .blankLine()
     .lines("<gray>Player: <white>%player%",
            "<gray>Online: <green>%online%",
            "<gray>Ping: <aqua>%ping%ms")
     .blankLine()
     .line("<yellow>play.myserver.net")
     .build();"""),
                p("Close it in <code>onDisable</code> with <code>board.close()</code>. Prefer a static handle? "
                  "<code>ScoreboardAPI.init(this)</code> and <code>ScoreboardAPI.shutdown()</code> do the same."),
            ]),
            ("threading", "Why it holds up", [ul([
                "No third-party dependencies: packets are built and sent directly.",
                "MiniMessage everywhere: any string argument accepts gradients, hover and click.",
                "The same jar runs on plain Paper, where everything simply lands on the main thread.",
                "Validated live on Folia 1.21.11.",
            ])]),
        ],
    },
    {
        "slug": "folianpc", "name": "FoliaNPC", "ore": "copper", "kind": "Library",
        "repo": "FoliaNPC-API", "version": "1.2.1",
        "tagline": "NPCs made only of packets: skins, nametags, pathfinding and click actions, with nothing spawned in the world.",
        "card": "Packet NPCs with skins, per-player nametags and pathfinding. Ten thousand idle NPCs cost what the visible ones cost.",
        "facts": [("Version", "1.2.1"), ("Java", "21"), ("Runs on", "Paper and Folia 1.20.6 to 26.x"), ("Dependencies", "none")],
        "sections": [
            ("overview", "Overview", [
                p("FoliaNPC's NPCs are not real entities. Nothing is added to the world, ticked by the server or "
                  "written to region files. Each NPC is a set of packets sent to the players close enough to see it."),
                grid([
                    ("It's cheap", "An NPC nobody is looking at costs a map entry. The cost follows what is visible."),
                    ("It's clean on Folia", "The only real entities involved are the players, and FoliaNPC tracks which thread owns each one."),
                    ("It has no physics", "No gravity, no collisions. An NPC stays exactly where you, walkTo or navigateTo put it."),
                    ("It needs nothing else", "Reflection against the server's own classes. No ProtocolLib, no packetevents."),
                ]),
            ]),
            ("features", "What's inside", [ul([
                "Any living entity type, player skins by name, URL or signed texture, and skin mirroring.",
                "Floating nametags with per-player text, PlaceholderAPI, background, opacity, shadow and see-through.",
                "Mob variants (cat, wolf, frog, rabbit, parrot, axolotl, horse and more), villager profession, type and level, baby state.",
                "Equipment, poses, glow colour, scale and collision.",
                "<code>walkTo</code> and <code>navigateTo</code> with real pathfinding around blocks.",
                "Visibility rules per player, view distance per NPC, cloning.",
                "Left and right click actions with reach validation, events, persistence and diagnostics.",
                "Clean <code>/reload</code>: closing the library removes every NPC from every client, even mid-disable.",
            ])]),
            ("install", "Install", [
                maven("FoliaNPC-API", "1.2.1"), gradle("FoliaNPC-API", "1.2.1"),
                FOLIA_YML,
                p("FoliaNPC ships no <code>plugin.yml</code>: shade it into your jar. The public API lives in "
                  "<code>net.folianpc.api</code>; anything under <code>internal</code> may change between releases."),
                relocate("net.folianpc", "folianpc"),
            ]),
            ("quick-start", "Quick start", [
                code("java", "MyPlugin.java", """
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
}"""),
                p("Create one <code>FoliaNpc</code> per plugin and keep it for the plugin's lifetime."),
            ]),
            ("versions", "Version support", [
                p("<code>FoliaNpc.create</code> checks the server at startup and refuses to start below 1.20.6. The "
                  "calendar-numbered 26.x releases are supported and tested on Purpur 26.3, where the movement packet and "
                  "team colours changed shape; both forms are detected at startup."),
            ]),
        ],
    },
    {
        "slug": "itemsmith", "name": "Itemsmith", "ore": "amethyst", "kind": "Plugin",
        "repo": "Itemsmith", "version": "1.0.0",
        "tagline": "Hold an item, type /item, and edit every part of it from a menu. Every change can be undone.",
        "card": "An in-game item editor for names, lore, enchantments, attributes, models, trims and more, with a full undo history.",
        "facts": [("Version", "1.0.0"), ("Java", "21"), ("Runs on", "Paper and Folia 1.21 and 26.x"), ("Languages", "English, French")],
        "sections": [
            ("overview", "Overview", [
                p("Itemsmith turns item editing into a menu. Hold anything, run <code>/item</code>, and change its name, "
                  "description, enchantments, attributes, hide flags, model, tooltip style, rarity, colour, head, durability "
                  "and more. Text is typed on a sign, and every change goes into an undo history."),
            ]),
            ("features", "What you can edit", [grid([
                ("Text", "Name and lore with MiniMessage, line by line, with move, insert and delete."),
                ("Enchantments", "Any enchantment at any level, even when the item can't normally hold it."),
                ("Attributes", "Add, multiply or percentage modifiers, per slot."),
                ("Looks", "Item model, custom model data, tooltip style, glint, rarity, colour, trims."),
                ("Behaviour", "Max stack, durability, unbreakable, glider, fire resistance, repair cost."),
                ("Special items", "Player heads and textures, potions, written books."),
            ])]),
            ("commands", "Commands", [
                table(["Command", "Effect"], [
                    ["<code>/item</code>", "opens the editor for the item in your hand"],
                    ["<code>/item edit &lt;field&gt; ...</code>", "edits one field directly, see <code>/item help</code>"],
                    ["<code>/item undo</code>", "undoes the last change"],
                    ["<code>/item info</code>", "summarises the item in your hand"],
                    ["<code>/item reload</code>", "rereads the config and language files"],
                ]),
                p("Aliases: <code>/itemedit</code>, <code>/ie</code>, <code>/itemeditor</code>, <code>/edititem</code>. "
                  "Everything needs <code>itemsmith.admin.item</code>, given to operators by default."),
            ]),
            ("api", "Developer API", [
                code("java", "Example.java", "ItemsmithApi.get().ifPresent(itemsmith -> itemsmith.openEditor(player));"),
                p("<code>ItemEditEvent</code> fires before an edit replaces the item in hand. It carries copies of the item "
                  "before and after; cancelling it keeps the original and leaves the undo history untouched."),
            ]),
        ],
    },
    {
        "slug": "puppeteer", "name": "Puppeteer", "ore": "redstone", "kind": "Plugin",
        "repo": "Puppeteer", "version": "1.0.0",
        "tagline": "Packet NPCs described in one YAML file, with click actions, per-player text and a reload that only touches what changed.",
        "card": "NPCs for servers, built on FoliaNPC: skins, nametags, equipment and click actions, plus importers from Citizens, FancyNpcs and ZNPCsPlus.",
        "facts": [("Version", "1.0.0"), ("Java", "21"), ("Runs on", "Paper and Folia 1.21 and 26.x"), ("Languages", "English, French")],
        "sections": [
            ("overview", "Overview", [
                p("Every NPC lives in <code>npcs.yml</code> and exists only as packets: no real entity, no server tick. "
                  "Players with skins, villagers, cats, zombies or any living entity, with nametag lines, equipment, "
                  "poses, animations and click actions."),
                p("<code>/npc reload</code> compares each NPC with the live one and only recreates those that changed. An NPC "
                  "whose world isn't loaded yet waits and appears when the world loads. NPCs locked behind a permission "
                  "are only visible to players who have it."),
            ]),
            ("example", "What an NPC looks like", [code("yaml", "npcs.yml", """
npcs:
  guide:
    name: Guide
    type: PLAYER
    location: { world: world, x: 0.5, y: 64.0, z: 0.5, yaw: 180.0, pitch: 0.0 }
    skin: Notch
    nametag:
      - "<gradient:#8a5cff:#35d0ff><b>SERVER GUIDE</b></gradient>"
      - "<gray>Welcome <white>%player%"
    look-at-players: true
    equipment:
      hand: COMPASS
    actions:
      - click: RIGHT
        type: TITLE
        value: "<gold><b>WELCOME</b>"
        subtitle: "<gray>Have a great adventure"
      - click: RIGHT
        type: SOUND
        value: entity.player.levelup
      - click: BOTH
        sneak: true
        type: PLAYER_COMMAND
        value: /spawn""")]),
            ("actions", "Click actions", [
                table(["Type", "Effect"], [
                    ["<code>MESSAGE</code>, <code>BROADCAST</code>, <code>ACTIONBAR</code>, <code>TITLE</code>", "text to the player or the server"],
                    ["<code>PLAYER_COMMAND</code>, <code>CONSOLE_COMMAND</code>", "run a command"],
                    ["<code>SOUND</code>, <code>PARTICLE</code>, <code>EFFECT</code>", "feedback for the player"],
                    ["<code>TELEPORT</code>, <code>SERVER</code>", "move the player, or send them to another proxy server"],
                    ["<code>GIVE_MONEY</code>, <code>TAKE_MONEY</code>", "Vault payments; a failed payment stops the chain"],
                    ["<code>REQUIRE_PERMISSION</code>", "stops the chain without the permission"],
                    ["<code>SWING</code>", "the NPC swings its arm"],
                ]),
                p("Actions run in order per click, with delays in ticks, sneak filters and per-action permissions."),
            ]),
            ("import", "Moving from another plugin", [
                p("Keep the other plugin's folder in <code>plugins/</code> and run <code>/npc import &lt;source&gt;</code>."),
                table(["Source", "Reads"], [
                    ["<code>citizens</code>", "<code>saves.yml</code>: name, type, location, skin, look close, command trait"],
                    ["<code>fancynpcs</code>", "<code>npcs.yml</code>: display name, location, skin, glow, scale, equipment, actions"],
                    ["<code>znpcsplus</code>", "<code>data/*.yml</code>: hologram lines, location, skin, look, actions"],
                ]),
                p("Existing ids are skipped, so running the import twice duplicates nothing."),
            ]),
            ("commands", "Commands", [
                p("<code>/npc</code> (aliases <code>/npcs</code>, <code>/pnj</code>, permission <code>puppeteer.admin.npc</code>): "
                  "<code>reload</code>, <code>list</code>, <code>info</code>, <code>create</code>, <code>delete</code>, "
                  "<code>movehere</code>, <code>tp</code>, <code>rename</code>, <code>skin</code>, <code>copy</code>, "
                  "<code>enable</code>, <code>disable</code>, <code>stats</code>, <code>import</code>."),
            ]),
            ("api", "Developer API", [
                code("java", "Example.java", """
PuppeteerApi.get().ifPresent(puppeteer -> {
    puppeteer.location("guide").ifPresent(player::teleport);
    puppeteer.setEnabled("banker", false);
});"""),
                p("<code>NpcClickEvent</code> fires before an NPC's actions run, with its id, the side and sneaking. "
                  "Cancelling it skips every action of that click."),
            ]),
        ],
    },
    {
        "slug": "lootrift", "name": "Lootrift", "ore": "gold", "kind": "Plugin",
        "repo": "Lootrift", "version": "1.0.0",
        "tagline": "Animated crates with virtual and physical keys, pity, milestones and a full in-game editor.",
        "card": "Crates with twelve opening animations, bulk opening, pity and milestones, plus importers from CrazyCrates and ExcellentCrates.",
        "facts": [("Version", "1.0.0"), ("Java", "21"), ("Runs on", "Paper and Folia 1.21 and 26.x"), ("Languages", "English, French")],
        "sections": [
            ("overview", "Overview", [
                p("Place a crate, right click it with a key to open it, left click to preview the rewards. Sneak to open "
                  "with every key at once in a dedicated animation. Rewards that don't fit drop at the player's feet."),
            ]),
            ("features", "What's inside", [grid([
                ("12 opening animations", "csgo, roulette, cascade, wheel, pulse, raffle, lightning, clock, wave, zoom, mosaic, instant."),
                ("12 bulk animations", "domino, avalanche, spiral, explosion, implosion, mirror, curtain, scanner and more."),
                ("Keys", "Virtual and physical keys, a free daily key and key purchases through Vault."),
                ("Fairness", "Pity guarantees a rarity after unlucky streaks; stats compare stated and observed chances."),
                ("Progress", "Opening milestones with money, commands and messages, repeatable or not."),
                ("Looks", "Particle effects around blocks, per-player holograms and ModelEngine models."),
                ("Rewards", "Items, money, commands, unique once-per-player rewards and server announcements."),
                ("Editor", "Every crate, reward, animation and effect is editable from <code>/crate admin</code>."),
            ])]),
            ("commands", "Commands", [
                table(["Command", "Effect"], [
                    ["<code>/crate admin</code>", "create, edit, place and remove crates"],
                    ["<code>/crate preview &lt;crate&gt;</code>", "reward preview"],
                    ["<code>/crate open &lt;crate&gt;</code>", "opens a crate without a block"],
                    ["<code>/crate history</code>", "win history"],
                    ["<code>/crate import &lt;source&gt;</code>", "imports crates and keys from another plugin"],
                    ["<code>/cle give &lt;player&gt; &lt;crate&gt; [amount]</code>", "gives virtual keys (<code>/key</code> works too)"],
                    ["<code>/cle all &lt;crate&gt; [amount]</code>", "gives keys to every online player"],
                ]),
            ]),
            ("import", "Moving from another plugin", [
                table(["Source", "Reads"], [
                    ["<code>crazycrates</code>", "<code>crates/*.yml</code> in both prize formats, and virtual keys from <code>data.yml</code>"],
                    ["<code>excellentcrates</code>", "<code>crates/*.yml</code> with vanilla items, and virtual keys from its SQLite database"],
                ]),
                p("Weights keep their proportions, commands keep working with <code>&lt;player&gt;</code>, and key balances are "
                  "added to each player. Anything that can't be carried over is listed in the console."),
            ]),
            ("placeholders", "Placeholders", [
                table(["Placeholder", "Value"], [
                    ["<code>%lootrift_keys_&lt;crate&gt;%</code>", "virtual keys of the player for a crate"],
                    ["<code>%lootrift_keys_total%</code>", "virtual keys of the player, all crates"],
                    ["<code>%lootrift_opened_&lt;crate&gt;%</code>", "openings of a crate by the player"],
                    ["<code>%lootrift_cooldown_&lt;crate&gt;%</code>", "seconds before the next opening"],
                ]),
            ]),
            ("api", "Developer API", [
                code("java", "Example.java", """
LootriftApi.get().ifPresent(lootrift -> {
    lootrift.giveKeys(player.getUniqueId(), "rare", 3);
    lootrift.open(player, "rare");
});"""),
                p("<code>CrateOpenEvent</code> fires before a key is used and can be cancelled. <code>CrateRewardEvent</code> "
                  "fires after each reward is delivered, with the reward id, rarity, amount and money."),
            ]),
        ],
    },
    {
        "slug": "loadout", "name": "Loadout", "ore": "prismarine", "kind": "Plugin",
        "repo": "Loadout", "version": "1.0.0",
        "tagline": "Kits with cooldowns, conditions, mastery tiers, streaks, vouchers and opening ceremonies.",
        "card": "Kits that reward coming back: mastery tiers, streaks, a featured kit, vouchers and gifting, plus importers from EssentialsX and UltimateKits.",
        "facts": [("Version", "1.0.0"), ("Java", "21"), ("Runs on", "Paper and Folia 1.21 and 26.x"), ("Languages", "English, French")],
        "sections": [
            ("overview", "Overview", [
                p("Loadout ships fourteen example kits and an in-game editor for all of them. Players browse kits by "
                  "category, try the gear on before claiming it, and watch an animated ceremony when they claim."),
            ]),
            ("features", "What's inside", [grid([
                ("Timing", "Cooldowns, daily, weekly or monthly resets, time windows, days of the week, limited periods."),
                ("Conditions", "Permission, playtime, level, balance, worlds, statistics and required kits."),
                ("Mastery", "Kits level up as they are claimed: shorter cooldowns, bonus rewards, extra draws."),
                ("Streaks and collection", "Claiming every reset builds a streak; collecting kits unlocks milestones."),
                ("Featured kit", "One paid kit rotates daily with a discount."),
                ("Vouchers and gifts", "Physical vouchers and paying a kit for another player."),
                ("Random draws", "Pools with weights, unique draws and an animated roulette."),
                ("Special kits", "First join, respawn, team kits, temporary items and unsellable items."),
            ])]),
            ("commands", "Commands", [
                table(["Command", "Effect"], [
                    ["<code>/kit</code>", "kit menu"],
                    ["<code>/kit &lt;kit&gt;</code>", "claims a kit"],
                    ["<code>/kit preview &lt;kit&gt;</code>, <code>/kit tryon &lt;kit&gt;</code>", "preview, or wear the gear before claiming"],
                    ["<code>/kit gift &lt;player&gt; &lt;kit&gt;</code>", "pays a kit for someone else"],
                    ["<code>/kit all</code>", "claims every free kit that is ready"],
                    ["<code>/kit admin</code>", "admin menu and editor"],
                    ["<code>/kit import &lt;source&gt;</code>", "imports kits and cooldowns from another plugin"],
                ]),
            ]),
            ("import", "Moving from another plugin", [
                table(["Source", "Reads"], [
                    ["<code>essentials</code>", "<code>kits.yml</code>, item aliases from <code>items.json</code>, and each player's last claim"],
                    ["<code>ultimatekits</code>", "<code>kit.yml</code> with its NBT items, and each player's last claim"],
                ]),
                p("Armour lands in armour slots, money and commands become rewards, and running cooldowns keep going."),
            ]),
            ("api", "Developer API", [
                code("java", "Example.java", """
LoadoutApi.get().ifPresent(loadout -> {
    if (loadout.available(player, "daily")) {
        loadout.claim(player, "daily");
    }
});"""),
                p("<code>KitClaimEvent</code> fires before anything is paid or given and can be cancelled. "
                  "<code>KitClaimedEvent</code> fires after delivery with the items and the new mastery level."),
            ]),
        ],
    },
]

PLUGIN_SECTIONS = [
    ("install", "Install", [
        p("Build the jar with <code>mvn package</code> from the repository, or grab it from the releases page, then drop "
          "it into <code>plugins/</code> and start the server. The config, the language files and the examples are "
          "written on first start."),
        p("Set <code>language: en</code> or <code>language: fr</code> in <code>config.yml</code>. "
          "PlaceholderAPI and Vault are optional."),
    ]),
]


def head(title, description, accent=None):
    style = f' style="--accent: var(--{accent})"' if accent else ""
    return f"""<!doctype html>
<html lang="en"{style}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#17181c">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{CSS}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def topbar(current=None):
    links = [("/#libraries", "Libraries", "libraries"), ("/#plugins", "Plugins", "plugins"),
             ("/#fit", "How they fit", "fit"), (GH, "GitHub", None)]
    items = []
    for href, label, key in links:
        attrs = ' aria-current="page"' if current == key else ""
        extra = ' class="optional"' if key == "fit" else ' class="secondary"' if key is None else ""
        items.append(f'<a href="{href}"{attrs}{extra}>{label}</a>')
    return f"""<header class="topbar deep">
<div class="wrap">
<a class="brand" href="/"><span class="brand-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>KiruProject</a>
<nav class="nav" aria-label="Main">{"".join(items)}</nav>
</div>
</header>
"""


FOOTER = f"""<footer class="footer">
<div class="wrap">
<span>Made by KiruGoldzZz for Paper and Folia servers.</span>
<span><a href="{GH}">github.com/SpirtySprite</a></span>
</div>
</footer>
"""


def card(project):
    tags = [f'<span class="chip accent">v{project["version"]}</span>']
    tags.append('<span class="chip">JitPack</span>' if project["kind"] == "Library" else '<span class="chip">Plugin</span>')
    return f"""<a class="card" href="/{project["slug"]}/" style="--accent: var(--{project["ore"]})">
<div class="card-top">{pixel(project["slug"], project["ore"])}<span class="chip">{project["kind"]}</span></div>
<h3>{project["name"]}</h3>
<p>{project["card"]}</p>
<div class="card-foot">{"".join(tags)}<span class="go">Read more</span></div>
</a>"""


def home():
    libraries = [project for project in PROJECTS if project["kind"] == "Library"]
    plugins = [project for project in PROJECTS if project["kind"] == "Plugin"]
    uses = {"itemsmith": ["1.1.1", "1.1.0", None], "puppeteer": ["1.1.1", "1.1.0", "1.2.1"],
            "lootrift": ["1.1.1", "1.1.0", None], "loadout": ["1.1.1", "1.1.0", None]}
    rows = []
    for plugin in plugins:
        cells = []
        for library, version in zip(libraries, uses[plugin["slug"]]):
            if version:
                cells.append(f'<td class="used" style="--accent: var(--{library["ore"]})"><span class="dot"></span>{version}</td>')
            else:
                cells.append('<td class="unused">not used</td>')
        rows.append(f'<tr><th scope="row" style="--accent: var(--{plugin["ore"]})"><a href="/{plugin["slug"]}/">'
                    f'<span class="dot"></span>{plugin["name"]}</a></th>{"".join(cells)}</tr>')
    library_heads = "".join(f'<th scope="col">{library["name"]}</th>' for library in libraries)
    legend = "".join(f'<span style="color: var(--{project["ore"]})">■</span>' for project in PROJECTS)
    return head("KiruProject", "Folia-native libraries and plugins for Minecraft servers: FoliaGUI, FoliaBoard, FoliaNPC, "
                "Itemsmith, Puppeteer, Lootrift and Loadout.") + topbar() + f"""<main id="main">
<section class="hero deep">
<div class="wrap">
<div>
<p class="eyebrow">Paper · Folia · 1.20.6 to 26.x</p>
<h1>Tools that know which thread they're on.<em>Three libraries and four plugins for Minecraft servers.</em></h1>
<p class="lede">Folia splits a world into regions, and each region ticks on its own thread. Menus, scoreboards and NPCs
that assume one main thread break there. These don't: packet-level, dependency-free, and safe to call from anywhere.</p>
<div class="hero-actions">
<a class="button solid" href="#libraries">Browse the libraries</a>
<a class="button" href="#plugins">See the plugins</a>
</div>
</div>
<figure class="map">
<canvas id="regions" role="img" aria-label="A world split into seven coloured regions, with players moving between them"></canvas>
<figcaption>
<span>{legend} one colour per region thread</span>
<span class="map-stats"><span><b data-stat="threads">7</b> threads</span><span><b data-stat="tick">0</b> ticks</span><span><b data-stat="handoffs">0</b> handoffs</span></span>
</figcaption>
</figure>
</div>
</section>

<section class="band" id="libraries">
<div class="wrap">
<div class="band-head">
<div><p class="eyebrow">Shade them in</p><h2>Libraries</h2></div>
<p>Published on JitPack, relocated into your own jar, no <code>plugin.yml</code>. Each one hides Folia's threading behind
a plain fluent API, and runs unchanged on regular Paper.</p>
</div>
<div class="cards three">{"".join(card(project) for project in libraries)}</div>
</div>
</section>

<section class="band" id="plugins">
<div class="wrap">
<div class="band-head">
<div><p class="eyebrow">Drop them in</p><h2>Plugins</h2></div>
<p>Built on those libraries. English and French out of the box, a developer API with events, PlaceholderAPI support, and
importers so you can move over from the plugin you use today.</p>
</div>
<div class="cards four">{"".join(card(project) for project in plugins)}</div>
</div>
</section>

<section class="band" id="fit">
<div class="wrap">
<div class="band-head">
<div><p class="eyebrow">Under the hood</p><h2>How they fit</h2></div>
<p>Every plugin shades its own relocated copy of the libraries it uses, so two plugins never fight over the same classes
or the same state.</p>
</div>
<div class="matrix-wrap">
<table class="matrix">
<thead><tr><th scope="col">Plugin</th>{library_heads}</tr></thead>
<tbody>{"".join(rows)}</tbody>
</table>
</div>
</div>
</section>
</main>
""" + FOOTER + f'<script src="{JS}" defer></script>\n</body>\n</html>\n'


def project_page(index, project):
    sections = list(project["sections"])
    if project["kind"] == "Plugin":
        sections.insert(1, PLUGIN_SECTIONS[0])
    toc = "".join(f'<li><a href="#{key}">{title}</a></li>' for key, title, _ in sections)
    body = "".join(f'<section id="{key}"><h2>{title}</h2>{"".join(parts)}</section>' for key, title, parts in sections)
    facts = "".join(f"<div><dt>{label}</dt><dd>{value}</dd></div>" for label, value in project["facts"])
    previous = PROJECTS[index - 1]
    following = PROJECTS[(index + 1) % len(PROJECTS)]
    second = (f'<a class="button" href="https://jitpack.io/#SpirtySprite/{project["repo"]}/{project["version"]}">JitPack</a>'
              if project["kind"] == "Library" else f'<a class="button" href="{GH}{project["repo"]}/releases">Releases</a>')
    current = "libraries" if project["kind"] == "Library" else "plugins"
    return head(f'{project["name"]}, {project["kind"].lower()} for Paper and Folia', project["tagline"], project["ore"]) + topbar(current) + f"""<main id="main">
<section class="project-head deep" style="--accent: var(--{project["ore"]})">
<div class="wrap">
{pixel(project["slug"], project["ore"], "big", project["name"] + " icon")}
<div>
<p class="eyebrow">{project["kind"]} · {project["repo"]}</p>
<h1>{project["name"]}</h1>
<p class="tagline">{esc(project["tagline"])}</p>
<dl class="facts">{facts}</dl>
<div class="hero-actions"><a class="button solid" href="{GH}{project["repo"]}">View on GitHub</a>{second}</div>
</div>
</div>
</section>
<div class="project-body">
<div class="wrap">
<nav class="toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc}</ol></nav>
<article class="doc">{body}
<nav class="pager" aria-label="More projects">
<a href="/{previous["slug"]}/" style="--accent: var(--{previous["ore"]})"><small>Previous</small><b>{previous["name"]}</b></a>
<a class="next" href="/{following["slug"]}/" style="--accent: var(--{following["ore"]})"><small>Next</small><b>{following["name"]}</b></a>
</nav>
</article>
</div>
</div>
</main>
""" + FOOTER + f'<script src="{HLJS}" defer></script>\n<script src="{JS}" defer></script>\n</body>\n</html>\n'


def not_found():
    return head("Page not found, KiruProject", "This page does not exist.") + topbar() + f"""<main id="main">
<section class="deep">
<div class="wrap missing">
<p class="eyebrow">Error 404 · chunk not generated</p>
<h1>Nothing loaded here.</h1>
<p class="lede">This page doesn't exist, or it moved. The projects are one click away.</p>
<div class="hero-actions"><a class="button solid" href="/">Back to the projects</a></div>
</div>
</section>
</main>
""" + FOOTER + "</body>\n</html>\n"


def main():
    (OUT / "index.html").write_text(home(), encoding="utf-8", newline="\n")
    (OUT / "404.html").write_text(not_found(), encoding="utf-8", newline="\n")
    for index, project in enumerate(PROJECTS):
        folder = OUT / project["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(project_page(index, project), encoding="utf-8", newline="\n")
    print("pages written", 2 + len(PROJECTS))


main()
