import random
import time
import json
import sqlite3 as sql
from paho.mqtt import client as mqtt_client
import pandas as pd

with open('settings.json', 'r') as rd:
    settings = json.loads(rd.read())
print(settings)
broker = settings["GENERAL"]["mqtt_broker"]
port = settings["GENERAL"]["ports"]["mqtt"]
topic = "projekt4"
client_id = f"backend_{random.randint(0, 1000)}"

conn = sql.connect(settings["GENERAL"]["db_path"])
cursor = conn.cursor()

count = 0

def connect_mqtt(broker=broker, port=port) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
            client.subscribe("#")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, message, topic=topic):
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


def on_message(client, userdata, msg):
    
    topic=msg.topic
    
    m_in=json.loads(msg.payload)
    # print(type(m_in))
    print("m_in = = ", m_in)
    print(list(m_in.keys())[-1], list(m_in.values())[-1])
    cursor.execute("Insert into random values (?,?)", [f"{list(m_in.keys())[-1]}", f"{list(m_in.values())[-1]}"])
    conn.commit()


def run():

    client = connect_mqtt()
    client.on_message = on_message
    # client.loop_start()
    # publish(client, "hello")
    client.loop_forever()



if __name__ == '__main__':
    try:
        run()
        
    except KeyError:
        print("Finished the program")
    finally:
        conn.close()
