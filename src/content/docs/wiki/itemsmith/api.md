---
title: "Developer API"
sidebar:
  order: 2
---

Add Itemsmith as a `depend` or `softdepend`, then get the service:

```java
ItemsmithApi.get().ifPresent(itemsmith -> itemsmith.openEditor(player));
```

`ItemsmithApi` opens the editor, undoes the last edit of a player and tells how many edits can be
undone.

`ItemEditEvent` fires before an edit replaces the item in hand, from the menu or the command. It
carries copies of the item before and after, and a short description of the change. Cancelling it
keeps the original item and leaves the undo history untouched.
