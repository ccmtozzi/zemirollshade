# Zemismart Roller Shade Integration
This is a pythons script to connect an Raspberry PI to an Zemismart Roller Shade, it's listen to an MQTT topic and execute a close or open command based on that topic.

# Requirements

- Python 3+
- pip (to automatically install python dependencies)

# Dependencies
- paho-mqtt
- bluepy
- [Zemismart](https://github.com/GylleTanken/python-zemismart-roller-shade)
- libglib2.0-dev ```sudo apt-get install libglib2.0-dev```

# Install

1. Download or clone the repository:
2. In the directory run ```pip install -r requirements.txt```
3. Configure details in ```rollshade.py``` and then run with ```python rollshade.py```

# Home Assistant Config

Just add a MQTT cover:

```yaml
cover:
  - platform: mqtt
    name: "Blinds Bedroom"
    state_topic: "blinds/02:D6:32:D3:A8:B0/status"
    command_topic: "blinds/02:D6:32:D3:A8:B0"
    qos: 0
    state_open: "on"
    state_closed: "off"
    payload_open: "open"
    payload_close: "close"
    retain: false
    optimistic: false
```

# What Next?

- Get information from the Shade (battery, state, etc..), currently it's just sending command, for open and close.
- ESP32 version - Would prefer to run this in a ESP32 instead of a Raspberry PI
