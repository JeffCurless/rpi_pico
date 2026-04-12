# pico_flash — Firmware Flashing Utility

Desktop Python 3 utility that automatically detects a Pico in bootloader mode and flashes a UF2 firmware file to it.

## Files

### pico_flash.py

Polls every 5 seconds for a device mounted as `RPI-RP2` (the Pico's USB mass-storage bootloader volume). When found, copies the specified `.uf2` file to the device root, which triggers the firmware flash and reboot.

Handles:
- `PermissionError` — device not yet fully mounted; retries next poll
- `FileNotFoundError` — mount point disappeared mid-copy; retries next poll

## Usage

```bash
python3 pico_flash.py -d <path_to_firmware.uf2>
```

1. Run the script
2. Hold BOOTSEL on the Pico and plug in USB (or press BOOTSEL while plugged in)
3. The script detects `RPI-RP2`, copies the UF2, and the Pico reboots automatically
4. Press Ctrl-C to exit; do not interrupt the process while a transfer is in progress

## Notes

- Works on Linux, macOS, and Windows (mount point detection may differ on non-Linux systems)
- The script loops indefinitely so you can flash multiple Picos one after another without restarting

## Parent

See the [project root](../../README.md) for an overview of all projects.
