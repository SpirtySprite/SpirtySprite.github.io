---
title: "Packages and building"
sidebar:
  order: 9
---

## Package overview

| Package | Contents |
|---|---|
| `com.foliagui` | `FoliaGUI` entry point, `FoliaGUIService`, `FoliaGUINotInitialisedException` |
| `com.foliagui.gui` | `BaseGui`, `Gui`, `PaginatedGui`, `SearchablePaginatedGui`, `ScrollingGui`, `StorageGui`, `AnvilGui`, `SignGui`, `MerchantGui`, `ChatPrompt`, `Confirmation`, `Alert`, `AsyncContent`, `GuiManager`, `GuiNavigator`, `GuiTheme`, `CycleItem`, `GuiType`, `ScrollType`, `InteractionModifier`, `GuiFiller` |
| `com.foliagui.item` | `GuiItem`, `GuiAction` |
| `com.foliagui.event` | `GuiOpenEvent`, `GuiClickEvent`, `GuiCloseEvent` |
| `com.foliagui.builder.item` | `ItemBuilder`, `SkullBuilder`, `PotionBuilder`, `BannerBuilder`, `FireworkBuilder`, `BookBuilder`, `BaseItemBuilder` |
| `com.foliagui.builder.gui` | `SimpleGuiBuilder`, `PaginatedGuiBuilder`, `ScrollingGuiBuilder`, `StorageGuiBuilder` |
| `com.foliagui.animation` | `GuiAnimation` |
| `com.foliagui.scheduler` | `Scheduler`, `PaperFoliaScheduler`, `TaskHandle` |
| `com.foliagui.listener` | `GuiListener` (registered automatically by `init`) |
| `com.foliagui.util` | `Text`, `Slot`, `ItemStackSerializer` |

## Testing

The test suite runs against [MockBukkit](https://github.com/MockBukkit/MockBukkit) so it can exercise real click events, real inventory holders, and the Folia-style per-entity scheduler without a live server:

```bash
mvn test
```

## Building from source

```bash
mvn clean install
```

This compiles the library, runs the test suite, and installs the jar (plus sources and javadoc jars) to your local Maven repository.

## License

Do whatever you want with it.
