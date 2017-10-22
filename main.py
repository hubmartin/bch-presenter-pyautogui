
#
# This script is listening on MQTT for specific messages and is pressing buttons with pyautogui.
# This can be used to control volume by BigClown button kits, or create a simple slideshow presenter
# Author: Martin Hubacek
#
# Example mqtt messages (the payload is ignored)
#   key/volumemute
#   key/right
#


from pyautogui import press, typewrite, hotkey
import paho.mqtt.client as mqtt

mqttBrokerAddress = "localhost"
keyCommands = ["volumemute", "volumeup", "volumedown", "playpause", "nexttrack", "prevtrack", "left", "right", "up", "down", "space"]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("key/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    command = msg.topic.replace("key/", "")
    if command in keyCommands:
      press(command)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBrokerAddress, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
