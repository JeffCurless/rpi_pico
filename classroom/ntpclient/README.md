# ntpclient — NTP Time Sync

Synchronises the Pico W's real-time clock from an NTP server over an existing WiFi connection.

## Files

### WIFI.py

WiFi credentials. Fill in before deploying:

```python
SSID = "your_network"
PASSWORD = "your_password"
```

This file is gitignored — do not commit real credentials.

### ntptime.py

**`NTPTime(host)`** class

| Method | Description |
|---|---|
| `getTime()` | Fetches UTC time from the NTP host via UDP port 123; returns a time tuple |
| `setTime()` | Calls `getTime()` and also sets `machine.RTC()` with the result |

### ntptest.py

Demo script that:
1. Connects to WiFi using `WIFI.py`
2. Syncs the clock once per hour (when the hour changes)
3. Prints the formatted current time in a loop

## Prerequisites

- Pico W with WiFi credentials in `WIFI.py`
- Internet access from the connected network

## Parent

See [classroom/](../README.md) for other classroom projects.
