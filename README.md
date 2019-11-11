# Zemismart Roller Shade Integration
This is a pythons script to connect an Raspberry PI to an Zemismart Roller Shade, it's listen to an MQTT topic and execute a close or open command based on that topic.

# Dependencies

- paho-mqtt (pip install paho-mqtt)
- bluepy (sudo pip install bluepy)
- libglib2.0-dev (sudo apt-get install libglib2.0-dev)

# Home Assistant Config:

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
