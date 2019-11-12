# Zemismart Roller Shade Integration
This is a pythons script to connect an Raspberry PI to an Zemismart Roller Shade, it's listen to an MQTT topic and execute a close or open command based on that topic.

# Dependencies

- paho-mqtt (pip install paho-mqtt)
- bluepy (sudo pip install bluepy)
- libglib2.0-dev (sudo apt-get install libglib2.0-dev)

# Home Assistant Config

Just add a MQTT switch:

```yaml
- platform: mqtt
  name: "Curtain Bedroom"
  state_topic: "curtains/00:00:00:00:00:00/status"
  command_topic: "curtains/00:00:00:00:00:00"
  qos: 0
  state_on: "on"
  state_off: "off"
  payload_on: "open"
  payload_off: "close"
  retain: false
  optimistic: false
```

# What Next?

- Get information from the Shade (battery, state, etc..), currently it's just sending command, for open and close.
- ESP32 version - Would prefer to run this in a ESP32 instead of a Raspberry PI
