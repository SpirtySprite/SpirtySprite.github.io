---
title: "FoliaGUI"
description: "Thread-safe inventory menus for Folia and Paper."
sidebar:
  order: 0
  label: "Introduction"
---

A thread-safe inventory GUI library for [Folia](https://papermc.io/software/folia) and regular Paper. It is a pure library: no commands, no `plugin.yml`, no config file. You add it as a dependency, call `FoliaGUI.init(this)` once, and build menus with a fluent API from there.

Every operation that touches an inventory (open, close, update, title change, animation) is dispatched through a Folia-safe scheduler. Your GUIs work correctly under Folia's regionised threading and on classic single-thread Paper, using the exact same code.

## Core concepts

A few rules apply across the whole library:

- **One GUI instance per viewer.** A `BaseGui` is designed to be looked at by one player at a time. If you want the same menu shown to several players, build one instance per player (a small factory method is the usual pattern).
- **Item mutators are map-only.** Calling `setItem`, `addItem`, `removeItem`, or anything under `filler()` just updates an internal map. The change becomes visible the next time you call `update()` or `open()`. This is deliberate: it lets you build a whole screen's worth of items without triggering a redraw after every single call.
- **Everything else is Folia-safe.** `open`, `close`, `update`, `updateTitle`, and `updateItem` route through the scheduler automatically, so you never need to check what thread you're on before calling them.
- **Colour strings accept both formats.** Anywhere a `String` title, name, or lore line is accepted, you can use legacy `&`-codes (`&aHello`) or call the `*Mini` variant for MiniMessage tags (`<gradient:#ff0000:#0000ff>Hello</gradient>`).
