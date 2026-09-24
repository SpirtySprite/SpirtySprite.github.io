---
title: "Item builders"
sidebar:
  order: 6
---

## Item builders

`ItemBuilder` covers the common cases (name, lore, enchants, flags, unbreakable, custom model data, glow, hide-tooltip, max stack size, durability, persistent data) and hands off to specialised builders for anything material-specific:

```java
ItemStack potion = ItemBuilder.potion(Material.SPLASH_POTION)
        .base(PotionType.STRONG_HEALING)
        .effect(PotionEffectType.SPEED, 20 * 30, 1)
        .color(Color.AQUA)
        .name("<gradient:#0ff:#00f>Zoom</gradient>") // parsed as MiniMessage via nameMini
        .build();

ItemStack head = ItemBuilder.skull()
        .owner(offlinePlayer)          // or .texture("base64...") or .textureUrl("https://...")
        .name("&fCustom Head")
        .build();

ItemStack banner = ItemBuilder.banner(Material.WHITE_BANNER)
        .pattern(DyeColor.RED, PatternType.STRIPE_BOTTOM)
        .build();

ItemStack rocket = ItemBuilder.firework()
        .power(2)
        .effect(FireworkEffect.builder().withColor(Color.LIME).with(FireworkEffect.Type.BURST).build())
        .build();

ItemStack book = ItemBuilder.book()
        .bookTitle("<gold>Rules")
        .author("<gray>The Server")
        .page("<green>Page one!")
        .build();

GuiItem button = ItemBuilder.of(Material.EMERALD)
        .name("&aBuy")
        .glow(true)
        .asGuiItem(event -> buy((Player) event.getWhoClicked()))
        .clickSound(Sound.ENTITY_EXPERIENCE_ORB_PICKUP);

ItemStack worn = ItemBuilder.of(Material.IRON_PICKAXE)
        .damage(150)
        .maxDamage(250)
        .build();
```

## Item metadata: NBT, enchants, attributes, and everything else

Every item builder is built on `BaseItemBuilder`, which exposes essentially everything `ItemMeta` offers, not just the common cosmetic options. All of it is guarded so calling the wrong method on the wrong material is a no-op, never an exception.

Enchantments, in bulk or one at a time:

```java
ItemStack sword = ItemBuilder.of(Material.DIAMOND_SWORD)
        .enchants(Map.of(Enchantment.SHARPNESS, 5, Enchantment.UNBREAKING, 3))
        .enchant(Enchantment.MENDING, 1, false) // false = respect the enchantment's normal max level
        .build();

boolean sharp = ItemBuilder.of(sword).hasEnchant(Enchantment.SHARPNESS);
Map<Enchantment, Integer> current = ItemBuilder.of(sword).getEnchants();
```

Persistent data (an item's custom NBT), beyond the single-value `setData` you'd use for a simple tag:

```java
NamespacedKey key = new NamespacedKey(plugin, "shop-price");

ItemStack priced = ItemBuilder.of(Material.DIAMOND)
        .setData(key, PersistentDataType.INTEGER, 500)
        .build();

Integer price = ItemBuilder.of(priced).getData(key, PersistentDataType.INTEGER);

ItemBuilder.of(priced).persistentData(container -> {
    // full access to the container for anything not wrapped above, e.g. nested containers
});
```

Resource-pack identity, rarity, and enchanting behaviour:

```java
ItemStack custom = ItemBuilder.of(Material.STONE)
        .itemModel(new NamespacedKey("myplugin", "custom_stone")) // Paper's modern per-item model key
        .customModelData(data -> data.setFloats(List.of(1.0f)))    // the newer component form
        .rarity(ItemRarity.EPIC)
        .enchantable(15)
        .build();
```

Attribute modifiers (bonus attack damage, extra speed, and so on):

```java
AttributeModifier bonus = new AttributeModifier(
        new NamespacedKey(plugin, "sword-bonus"), 4.0, AttributeModifier.Operation.ADD_NUMBER);

ItemStack sword = ItemBuilder.of(Material.DIAMOND_SWORD)
        .attribute(Attribute.ATTACK_DAMAGE, bonus)
        .build();
```

The newer 1.20.5+ data components (food, tool, equippable, jukebox-playable, use-cooldown) all follow the same pattern: you get a `Consumer` that receives the current component already populated with its existing values, so you only need to touch what you're changing:

```java
ItemStack apple = ItemBuilder.of(Material.GOLDEN_APPLE)
        .food(food -> {
            food.setNutrition(20);
            food.setSaturation(10f);
            food.setCanAlwaysEat(true);
        })
        .build();

ItemStack sword = ItemBuilder.of(Material.NETHERITE_SWORD)
        .equippable(equippable -> equippable.setSlot(EquipmentSlot.HAND))
        .build();
```

A few more scattered options: `glider(boolean)`, `fireResistant(boolean)`, `damageResistant(Tag<DamageType>)`, `useRemainder(ItemStack)`, `canDestroy(Material...)` / `canPlaceOn(Material...)` for adventure-mode inventories, `repairCost(int)` on anything with an anvil repair cost, `itemName(String)` for the separate non-renameable display name, and `ItemBuilder.trim(TrimMaterial, TrimPattern)` for armor. And if something genuinely isn't wrapped, `editMeta(Consumer<ItemMeta>)` drops you straight into the raw `ItemMeta`.

## Saving and loading item stacks

`StorageGui` deliberately doesn't persist its contents for you. `ItemStackSerializer` is the other half of that:

```java
String saved = ItemStackSerializer.toBase64(storageGui.getStorageContents());
// store `saved` in a config file, a database column, wherever you like

// later, perhaps after a restart:
storageGui.setStorageContents(ItemStackSerializer.fromBase64(saved));
```

`toBase64Compact`/`fromBase64Compact` do the same job using Paper's native NBT-based `ItemStack` serialization instead of Java object serialization. The result is smaller and faster to (de)serialize; reach for it unless you need the encoded string to stay readable by older saves that already used `toBase64`:

```java
String compact = ItemStackSerializer.toBase64Compact(storageGui.getStorageContents());
storageGui.setStorageContents(ItemStackSerializer.fromBase64Compact(compact));
```

## Text utility

`Text` bridges legacy colour codes, MiniMessage, and Adventure components:

```java
Component fromLegacy = Text.of("&aHello");
Component fromMini = Text.mini("<gradient:#f00:#00f>Hello</gradient>");
Component label = Text.label("&aHello"); // also disables the default item-name italic

String backToLegacy = Text.toLegacy(fromMini);

Component templated = Text.of("&aHello, {player}!", Map.of("player", player.getName()));
```

`Text.parse` accepts legacy codes (`&a`, `§a`, `&#rrggbb`, `§x§r§r§g§g§b§b`) and MiniMessage in the same
string, and the item builder has matching `nameAny` and `loreAny`:

```java
Component mixed = Text.parse("&6Gold <gradient:#f00:#00f>and gradient</gradient>");
ItemBuilder.of(Material.NETHER_STAR).nameAny("&d&lNexus <gray>Star").loreAny("&7Line one", "<aqua>Line two");
String safe = Text.escape(playerInput); // cannot inject tags
```
