import random
import time

from paho.mqtt import client as mqtt_client
import numpy as np

import sqlite3
from datetime import datetime
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
location = ""

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
        global location
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == "/home/start_measurement":
            location = msg.payload.decode()
        if msg.topic == "/home/anotherone":
            array[count] = msg.payload.decode()
            count += 1
            if count % 100 == 0:
                print(count)
            #print(count, array)
        if msg.topic == "/home/finish":
            print(count, np.average(1.0104* array))
            write_data()
            count = 0
            print("ready for next start")
            #raise KeyError
        else:
            pass

    client.subscribe(topic)
    client.on_message = on_message

def write_data():
    verbindung = sqlite3.connect("./datenbank.db")
    cursor = verbindung.cursor()

    cursor.execute("""CREATE TABLE if not exists ALLE_DATEN(
    ID INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    Zeitstempel text UNIQUE
    Ort text,
    Beleuchtung real,
    Temperatur real)""")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    avgTemperatur = round(np.average(array[:,0]), 2)
    avgBeleuchtung = round(np.average(array[:,1]), 2)

    if avgTemperatur != 0.0 and avgBeleuchtung != 0.0:
        cursor.execute(
            """INSERT INTO Alle_Daten (ID,Zeitstempel,Ort,Beleuchtung,Temperatur)VALUES(null,'{0}','{1}','{2}', '{3}');""".format(
                timestamp, location, avgBeleuchtung, avgTemperatur))

    ergebnisSQL = cursor.execute("SELECT * from ALLE_DATEN")
    ergebnisSQL

    verbindung.commit()
    cursor.close()
    verbindung.close()



def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()



if __name__ == '__main__':
    try:
        run()
    except KeyError:
        print("Finished the program")
