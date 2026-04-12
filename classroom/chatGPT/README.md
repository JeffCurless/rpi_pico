# chatGPT

A wrapper around the OpenAI completions API for Pico W. Sends prompts to ChatGPT and returns the response text over an established WiFi connection.

## Files

### chatgpt.py

**`chatGPT(api_key, max_tokens)`** class

| Method | Description |
|---|---|
| `askQuestion(prompt)` | POSTs to `https://api.openai.com/v1/completions` using the `text-davinci-003` model; returns the response text string |

### apikey.py

Paste your OpenAI API key here:

```python
KEY = 'sk-...'
```

This file is gitignored — do not commit your API key.

### chattest.py

Demo script that:
1. Connects to WiFi using `WIFI.py`
2. Creates a `chatGPT` instance with the key from `apikey.py`
3. Asks a Sherlock Holmes story question
4. Prints the response

## Prerequisites

- A Pico W with an active WiFi connection
- `WIFI.py` placed on the device (see [ntpclient/](../ntpclient/README.md) for a `WIFI.py` template)
- A valid OpenAI API key in `apikey.py`

## Parent

See [classroom/](../README.md) for other classroom projects.
