---
title: "FoliaNPC"
description: "Packet-based NPCs for Paper and Folia with no dependencies."
sidebar:
  order: 0
  label: "Introduction"
---

A packet-based NPC library for Paper and Folia with no third-party dependencies. Everything is done
through reflection against the server's own classes, so there's no ProtocolLib or packetevents to
install alongside it.

FoliaNPC is a library, not a plugin. It ships no `plugin.yml` and no commands; you shade it into your
own plugin and control it entirely from code.

## Design

The NPCs are not real entities. Nothing is added to the world, nothing is ticked by the server, and
nothing is written to region files. Each NPC exists only as a set of packets sent to the players close
enough to see it, the server never spawns an `Entity` object for it, there's no AI, no pathing goal,
no chunk ticket, no persistence in the level data.

That has three consequences worth understanding up front, because they explain almost every behavior
described later in this document:

1. **It's cheap.** An NPC nobody is looking at costs nothing beyond a map entry. Ten thousand NPCs
   spread across a large world cost roughly what the *visible* subset costs, not what all ten thousand
   would cost as real entities.
2. **It works cleanly on Folia.** Folia's whole model is built around real entities and players each
   being owned by exactly one region thread, and code touching one from the wrong thread throws or
   corrupts state. A library with no real entities has nothing Folia needs to protect it from, the
   only entities anywhere in this system are the *players themselves*, and FoliaNPC already tracks
   which thread owns each one (see [Threading](/wiki/folianpc/threading/)).
3. **It has no physics.** There's no gravity, no collision resolution, no falling, no fluid pushing it
   around. Position is 100% whatever you (or `walkTo`/`navigateTo`) last set it to. Spawn an NPC over a
   hole and it will float there indefinitely; nothing will ever pull it down on its own. If you need
   that, see [Known limitations](/wiki/folianpc/limitations/#known-limitations).

Every NPC is identified by a real, random `UUID` (so it can hold a tab-list profile and, for `PLAYER`
type, a skin) but that UUID belongs to no actual player and no actual entity anywhere on the server.
