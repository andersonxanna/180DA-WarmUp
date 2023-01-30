import paho.mqtt.client as mqtt
import numpy as np
import time
from rps import RockPaperScissors



p1_ready = False
p2_ready = False

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    info = client.publish("ece180/team1/rps", '8 '+rps.get_start_message(), qos=1)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180/team1/rps")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (won’t be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    # print('Received message: "' + str(message.payload) + '" on topic "' +
    # message.topic + '" with QoS ' + str(message.qos))

    global rps
    global p1_ready
    global p2_ready

    # print("BBBB", str(message.payload)[0:3])
    # Expected input 'player#-1move' eg. '1r' for player 1 moves rock
    if str(message.payload)[0:3] == "b'1":
        print("PLAYER 1:", str(message.payload))
        rps.set_move(1, str(message.payload)[3])
        p1_ready = True
    elif str(message.payload)[0:3] == "b'2":
        print("PLAYER 2", str(message.payload))
        rps.set_move(2, str(message.payload)[3])
        p2_ready = True

    if p1_ready and p2_ready:
        msg = rps.get_game_state()
        client.publish("ece180/team1/rps", '0 '+msg, qos=1)
        client.publish("ece180/team1/rps", '8 '+rps.get_start_message(), qos=1)
        p1_ready = False
        p2_ready = False
    elif p1_ready:
        info = client.publish("ece180/team1/rps", '0 Waiting for Player2', qos=1)
    elif p2_ready:
        info = client.publish("ece180/team1/rps", '0 Waiting for Player1', qos=1)


if __name__ == '__main__':
    # 1. create a client instance.
    client = mqtt.Client("Andrew's Publisher")

    # add additional client options (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.
    # client.connect_async("test.mosquitto.org")
    client.connect_async('mqtt.eclipseprojects.io')

    # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()

    # 4. use subscribe() to subscribe to a topic and receive messages.

    # 5. use publish() to publish messages to the broker.
    # payload must be a string, bytearray, int, float or None.
    print('Initializing Rock Paper Scissors')
    rps = RockPaperScissors()
    # p1_ready = False
    # p2_ready = False
    print('Publishing...')

    # for i in range(10):
    #     info = client.publish("ece180/team1/rps", "hello andrew", qos=1)
    # info = client.publish("ece180/team1/rps", '8 '+rps.get_start_message(), qos=1)


    while True:
        pass