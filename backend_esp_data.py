import random
import time

from paho.mqtt import client as mqtt_client
import numpy as np

broker = "192.168.178.77"
port = 1883
topic = "/home/#"
client_id = f"python-mqtt-{random.randint(0, 1000)}"

Tiefpass = 0
INPUTS = 2
PERIOD = 3
ADCMODE = 10 * INPUTS * PERIOD
MAX = 1000
array = np.zeros((MAX, INPUTS), np.float16)

count = 0

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def subscribe(client: mqtt_client):

    count = 0

    def on_message(client, userdata, msg):
        global count
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == "/home/anotherone":
            array[count] = msg.payload.decode()
            count += 1
            if count % 100 == 0:
                print(count)
            #print(count, array)
        if msg.topic == "/home/finish":
            print(count, np.average(1.0104* array))
            count = 0
            print("ready for next start")
            #raise KeyError
        else:
            pass

    client.subscribe(topic)
    client.on_message = on_message




def run():
    client = connect_mqtt()
    #client.loop_start()
    #publish(client)

    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()
    except KeyError:
        print("Finished the program")
