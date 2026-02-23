# Badge

Two badge variants for Pimoroni eInk displays that cycle through user portraits and info panels. Used by CTE Ambassador students — each badge rotates between a student portrait and school info slides.

## Hardware Variants

### badge.py — Pico Inky Pack

Simple polling loop with no persistent state.

- Button A: cycle to next user portrait (`/user/userN.jpg`)
- Button B: restart automatic cycling
- Button C: manually advance to next panel
- Auto-advances every ~10 seconds

### CTE_Badge.py — Badger2040W

Extended version with persistent state and deep sleep support.

- State saved to `/state/CTEBadge.json` so the badge resumes where it left off after sleep
- Deep sleep via `badger2040.sleep_for(1)` to conserve battery
- Pressing UP on wake resets state back to the first image

## Image Conventions

Images must be copied to the Pico's filesystem before use:

| Directory | Files | Description |
|---|---|---|
| `/user/` | `user.jpg`, `user0.jpg`, `user1.jpg`, … | Student/user portraits |
| `/panels/` | `panel1.jpg`, `panel2.jpg`, … | Info slides (1-indexed, sequential) |

Student images are gitignored. Panel images live in `ambassadors/badge/panels/`.

## Parent

See [ambassadors/](../README.md) for the full ambassadors project overview.
