import random
import time

from paho.mqtt import client as mqtt_client
import numpy as np

start_broker = "192.168.178.77"
start_port = 1883
start_topic = "/home/anotherone"
client_id = f"python-mqtt-{random.randint(0, 1000)}"

Tiefpass = 0
INPUTS = 2
PERIOD = 3
ADCMODE = 10 * INPUTS * PERIOD
MAX = 1000
array = np.zeros((MAX, INPUTS), np.float16)

count = 0

def connect_mqtt(broker=start_broker, port=start_port) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, message, topic=start_topic):
    msg_count = 0
    # while True:
        # time.sleep(1)
        # msg = message
        # result = client.publish(topic, msg)
        # status = result[0]
        # if status == 0:
        #     print(f"Send `{msg}` to topic `{topic}`")
        # else:
        #     print(f"Failed to send message to topic {topic}")
    time.sleep(1)
    msg = message
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")



def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)




if __name__ == '__main__':
    try:
        run()
    except KeyError:
        print("Finished the program")
