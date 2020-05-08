#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time
import re
import Zemismart

### Variables

mqtt_client = "192.168.1.1" #mqtt IP
mqtt_port = 1883
mqtt_user = "username"
mqtt_password = "password"
mqtt_path = "blinds"
dev_pin = 8888

####  Don't edit below here

# btle.Debugging=True


def shade_command(fble, fcmd, fpos=100):
    print ("["+ fble + "] Connecting")
    shade = Zemismart.Zemismart(fble, dev_pin)
    with shade:
      print ("["+ fble + "] Connected!")
      if fcmd == "open":
          shade.open()
      elif fcmd == "close":
          shade.close()
      elif fcmd == "stop":
          shade.stop()
      elif fcmd == "set_position":
          shade.set_position(int(fpos))
      else:
          print("Unrecognized command.")
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
    if msg.topic.find("set_position") > 0:
       mac = mac.replace("/set_position", "")
    if msg.topic.find("status") > 0:
       mac = mac.replace("/status", "")
    if msg.topic.find("/position") > 0:
       mac = mac.replace("/position", "")
    if checkMAC(mac) == 0:
       print ("["+ mac + "] Is not a valid Mac Address")
       return
    if msg.topic == (mqtt_path + "/" + mac + "/set_position"):
      t = 1
      while t <= 3:
        try:
          shade_command(mac, "set_position", msg.payload.decode())
          client.publish(msg.topic.replace("/set_position", "") + "/position", msg.payload.decode(), qos=0, retain=False)
          print ("["+ mac + "] Status Published: " + msg.topic.replace("/set_position", "") + "/position")
          print ("["+ mac + "] Finished")
          break
        except:
          time.sleep(0.5)
          if t <= 3:
            print ("["+ mac + "] Error! - Trying to Connect Again! (" + str(t) + "/3)")
          else:
            print ("["+ mac + "] Error! - Can't Connect")
          t += 1
    if msg.payload.decode() == "open":
      t = 1
      while t <= 3:
        try:
          shade_command(mac, "open")
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
          shade_command(mac, "close")
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
    if msg.payload.decode() == "stop":
      t = 1
      while t <= 3:
        try:
          shade_command(mac, "stop")
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
