# altmain — App Launcher

A menu-driven app launcher for Pico Display. Scans the Pico's `/apps/` directory for Python scripts and presents a navigable list, then imports and runs the selected app.

## Files

### altmain.py

**`DialogBox` class** — draws a scrollable menu on the Pico Display showing all `.py` files found in `/apps/`.

**Button mapping:**

| Button | Action |
|---|---|
| A | Move selection up |
| B | Move selection down |
| Y | Launch selected app |
| A + B simultaneously | `machine.reset()` — return to launcher |
| A + X simultaneously | `machine.reset()` — return to launcher |

The simultaneous reset combo is handled via hardware interrupts (IRQ) so it works even while an app is running.

## Deployment

1. Copy `altmain.py` to the Pico as `main.py` so it runs automatically at boot
2. Create an `/apps/` directory on the Pico's filesystem
3. Copy any app scripts into `/apps/` — they will appear in the menu

## Parent

See [classroom/](../README.md) for other classroom projects.
