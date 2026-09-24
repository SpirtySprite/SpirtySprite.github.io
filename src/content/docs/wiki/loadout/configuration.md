---
title: "Configuration, points and teams"
sidebar:
  order: 2
---

`kits.yml` holds the settings (`settings`), progression (`progression`: mastery, streaks,
collection, featured kit), the menu categories and the kits under `kits`. Everything can also be
edited from `/kit admin`.

Durations accept `30s`, `10m`, `2h`, `1d`. Resets accept `daily`, `weekly`, `monthly`, and days
accept `monday` to `sunday`.

## Conditions on any placeholder

With PlaceholderAPI, a kit can require any value from any plugin:

```yaml
requirements:
  placeholders:
    - "%player_level% >= 10"
    - check: "%luckperms_primary_group_name% == vip"
      label: "VIP rank"
```

Operators are `==`, `!=`, `>`, `>=`, `<`, `<=` and `contains`. Numbers compare as numbers, anything
else compares as text without case. The label shows in the menu next to the other conditions.

## Points currency

Kits can cost and give points from any points plugin (PlayerPoints, TokenManager, ...). Loadout reads
the balance through a placeholder and moves points with console commands:

```yaml
points:
  name: "Tokens"
  balance: "%playerpoints_points%"
  take: "points take {player} {amount}"
  give: "points give {player} {amount}"
```

Use `cost.shards` and `rewards.shards` in `kits.yml` for the amounts. If the claim fails after the
points were taken, they are given back. Without a `balance` placeholder, kits that cost points stay
locked.

## Team kits

A kit with `options.team: true` shares one cooldown and one set of uses across a team. The team is
read from a placeholder, so it works with any team, clan or town plugin:

```yaml
teams:
  placeholder: "%betterteams_name%"
```

Players whose placeholder is empty, `none` or `-` have no team and cannot claim team kits.

When the inventory is full, extra items drop at the player's feet.
