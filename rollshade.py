#!/usr/bin/env python
from bluepy import *
import paho.mqtt.client as mqtt
import time
import re

### Variables

mqtt_client = "192.168.1.1" #mqtt IP
mqtt_port = 1883
mqtt_user = "username"
mqtt_password = "password"
mqtt_path = "curtains"

####  Don't edit below here

#btle.Debugging=True

open = "\x00\xff\x00\x00\x9a\x0d\x01\x00\x96"
close = "\x00\xff\x00\x00\x9a\x0d\x01\x64\xf2"

def shade_command(fble, fcmd):
    print ("["+ fble + "] Connecting")
    dev = btle.Peripheral(fble)
    print ("["+ fble + "] Connected!")
    chs = dev.getCharacteristics()
    for ch in chs:
      if ch.uuid == "0000fe51-0000-1000-8000-00805f9b34fb":
        ch.write(fcmd)
    dev.disconnect
    print  ("["+ fble + "] Disconnected")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_path + "/#")

def checkMAC(x):
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", x.lower()):
        return 1
    else:
        return 0

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
#    print ("message comming in")
    mac = msg.topic.replace(mqtt_path + "/", "")
    if checkMAC(mac) == 0 and (msg.payload == open or msg.payload == close):
       print ("["+ mac + "] Is not a valid Mac Address")
       return
    if msg.payload.decode() == "open":
      t = 1
      while t <= 3:
        try:
          shade_command(mac, open)
          client.publish(msg.topic + "/status", "on", qos=0, retain=False)
          print ("["+ mac + "] Status Published: " + msg.topic + "/status")
          print ("["+ mac + "] Finished")
          break
        except:
          time.sleep(0.5)
          if t <= 3:
            print ("["+ mac + "] Error! - Trying to Connect Again! (" + str(t) + "/3)")
          else:
            print ("["+ mac + "] Error! - Can't Connect")
          t += 1
    if msg.payload.decode() == "close":
      t = 1
      while t <= 3:
        try:
          shade_command(mac, close)
          client.publish(msg.topic + "/status", "off", qos=0, retain=False)
          print ("["+ mac + "] Status Published: " + msg.topic + "/status")
          print ("["+ mac + "] Finished")
          break
        except:
          time.sleep(0.5)
          if t <= 3:
            print ("["+ mac + "] Error! - Trying to Connect Again! (" + str(t) + "/3)")
          else:
            print ("["+ mac + "] Error! - Can't Connect")
          t += 1

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
