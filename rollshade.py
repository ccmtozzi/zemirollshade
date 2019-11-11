#!/usr/bin/env python
from bluepy import btle
import paho.mqtt.client as mqtt

### Variables

mqtt_client = "192.168.1.10"
mqtt_port = 1883
mqtt_user = "username"
mqtt_password = "password"
mqtt_path = "curtains"

####  Don't edit below here

close = "\x00\xff\x00\x00\x9a\x0d\x01\x00\x96"
open = "\x00\xff\x00\x00\x9a\x0d\x01\x64\xf2"

def curtain_command(fble, fcmd):

  print "Connecting to BLE: " + fble
  dev = btle.Peripheral(fble)
  chs = dev.getCharacteristics()
  for ch in chs:
    if ch.uuid == "0000fe51-0000-1000-8000-00805f9b34fb":
      ch.write(fcmd)
  dev.disconnect
  print "Disconnect BLE: " + fble

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_path + "/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.payload == "open":
        address = msg.topic.replace(mqtt_path + "/", "")
        curtain_command(address, open)
        print msg.topic + "/status"
        client.publish(msg.topic + "/status", "on", qos=0, retain=False)
    if msg.payload == "close":
        address = msg.topic.replace(mqtt_path + "/", "")
        curtain_command(address, close)
        client.publish(msg.topic + "/status", "off", qos=0, retain=False)
        print msg.topic + "/status"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(mqtt_user, password=mqtt_password)
client.connect(mqtt_client, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
