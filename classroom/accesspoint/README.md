# Access Point

Creates a WiFi soft access point with a built-in DHCP server and HTTP server. No internet connection is required — useful for classroom environments where internet access is restricted or unavailable.

## Files

### accesspoint.py

Async server using `uasyncio`. Configures the Pico W as a WiFi access point and handles HTTP requests.

**Endpoints:**

| Endpoint | Description |
|---|---|
| `/light/on` | Turns on the onboard LED |
| `/light/off` | Turns off the onboard LED |
| `/badge?username="name"` | Displays a name badge on the connected display |

WiFi credentials and channel are read from `secret.py`.

### secret.py

WiFi configuration. Copy and edit before deploying:

```python
SSID = "MyAccessPoint"
PASSWORD = "mypassword"
CHANNEL = 6
```

This file is gitignored — do not commit real credentials.

### get.py

Test client that connects to the access point and exercises all three HTTP endpoints. Run on a separate device or desktop Python to verify the server is working.

## Usage

1. Edit `secret.py` with your desired AP name and password
2. Copy `accesspoint.py` and `secret.py` to the Pico W
3. Power on — the Pico W will broadcast the WiFi network
4. Connect a device to the AP, then run `get.py` to test

## Parent

See [classroom/](../README.md) for other classroom projects.
