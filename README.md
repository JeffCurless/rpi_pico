# rpi_pico

Collection of programs for the Raspberry Pi Pico/PicoW targeting Pimoroni display accessories.

## Folder Structure

| Folder | Description |
|---|---|
| [ambassadors/](ambassadors/README.md) | CTE Ambassador badge projects |
| [classroom/](classroom/README.md) | Classroom examples and student projects |
| [clock/](clock/README.md) | Stepper motor clock |
| [tools/pico_flash/](tools/pico_flash/README.md) | Firmware flashing utility |

## Hardware

Projects target Pimoroni accessories for the Pico and Pico W:

- **Pico Display Pack** — color LCD display with buttons and RGB LED
- **Pico Inky Pack** — eInk display
- **Badger2040W** — WiFi-enabled eInk badge board

All hardware-specific imports (`machine`, `picographics`, `badger2040`) only run on-device, not on a desktop Python interpreter.

## Deployment

Copy files to the Pico using **Thonny IDE** or `rshell`/`mpremote`.

To flash UF2 firmware:

```bash
python3 tools/pico_flash/pico_flash.py -d <path_to_firmware.uf2>
```
