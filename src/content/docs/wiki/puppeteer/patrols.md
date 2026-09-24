---
title: "Patrols"
sidebar:
  order: 3
---

An NPC can walk a loop, starting from its location, through a list of points, and back:

```yaml
patrol:
  speed: 0.8
  pause-ticks: 60
  points:
    - "4.5 64 4.5"
    - "4.5 64 0.5"
```

`speed` is in blocks per second, `pause-ticks` is the wait at each point. The NPC finds its way
around blocks; when no path exists it walks straight to the point. `/npc path add <id>` adds the
point where you stand, `/npc path clear <id>` removes the patrol.
