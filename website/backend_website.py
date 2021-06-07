import random
import time
import json
import sqlite3 as sql
from paho.mqtt import client as mqtt_client
import pandas as pd
import datetime

with open('settings.json', 'r') as rd:
    settings = json.loads(rd.read())
# print(settings)
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

    with open(settings["GENERAL"]["location_path"], "r") as file:
        ort = file.read()

    # print(ort)

    conn = sql.connect(settings["GENERAL"]["db_path"])
    cursor = conn.cursor()


    df_orte = pd.read_sql('SELECT * from Orte', conn)
    df_sensoren = pd.read_sql('SELECT * from Sensoren', conn)

    orte_dict = df_orte.to_dict()

    orte = [i for i in orte_dict["Ortsbezeichnung"].values()]
    orte_id = [i for i in orte_dict["Ort_ID"].values()]


    orte_dict = dict(zip(orte_id,orte))

    print(orte_dict)

    for id, orte in orte_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if orte == ort:
            current_location = id

    sensoren_dict = df_sensoren.to_dict()
    # print(sensoren_dict)
    sensor = [i for i in sensoren_dict["Sensorname"].values()]
    sensor_id = [i for i in sensoren_dict["Sensoren_ID"].values()]


    sensor_dict = dict(zip(sensor_id,sensor))

    print(sensor_dict)

    

    
    topic=msg.topic
    
    m_in=json.loads(msg.payload)
    # print(type(m_in))
    print("m_in = = ", m_in)
    print(list(m_in.keys())[-1], list(m_in.values())[-1])
    cursor.execute("Insert into random values (?,?)", [f"{list(m_in.keys())[-1]}", f"{list(m_in.values())[-1]}"])
    conn.commit()
    for key in m_in.keys():
        

        for id, sensoren in sensor_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if sensoren == key:
                current_sensor = id
        print(current_sensor)
        cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),int(current_sensor), int(current_location), m_in[key]])

    # cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [f"{datetime.datetime.now()}",1, int(current_location), uniform(10.0, 30.0)])
    # cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [f"{datetime.datetime.now()}",2, int(current_location), uniform(400.0, 2000.0)])
    # cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [f"{datetime.datetime.now()}",3, int(current_location), uniform(1.0, 100.0)])
    conn.commit()
    print("commit")



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
