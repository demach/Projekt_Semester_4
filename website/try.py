import sqlite3 as sql
import json
from time import sleep
from random import randint, uniform
import datetime
import pandas as pd

with open('settings.json', 'r') as rd:
    settings = json.loads(rd.read())

with open(settings["GENERAL"]["location_path"], "r") as file:
    ort = file.read()

print(ort)

conn = sql.connect(settings["GENERAL"]["db_path"])
cursor = conn.cursor()


df_orte = pd.read_sql('SELECT * from Orte', conn)


orte_dict = df_orte.to_dict()

orte = [i for i in orte_dict["Ortsbezeichnung"].values()]
orte_id = [i for i in orte_dict["Ort_ID"].values()]


orte_dict = dict(zip(orte_id,orte))

print(orte_dict)

for id, orte in orte_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
    if orte == ort:
        current_location = id



while True:
    with open(settings["GENERAL"]["location_path"], "r") as file:
        ort = file.read()

    print(ort)

    conn = sql.connect(settings["GENERAL"]["db_path"])
    cursor = conn.cursor()


    df_orte = pd.read_sql('SELECT * from Orte', conn)


    orte_dict = df_orte.to_dict()

    orte = [i for i in orte_dict["Ortsbezeichnung"].values()]
    orte_id = [i for i in orte_dict["Ort_ID"].values()]


    orte_dict = dict(zip(orte_id,orte))

    # print(orte_dict)

    for id, orte in orte_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if orte == ort:
            current_location = id
    cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [f"{datetime.datetime.now()}",1, int(current_location), uniform(10.0, 30.0)])
    cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [f"{datetime.datetime.now()}",2, int(current_location), uniform(400.0, 2000.0)])
    cursor.execute("insert into Messwerttabelle values (null, ?,?,?,?)", [f"{datetime.datetime.now()}",3, int(current_location), uniform(1.0, 100.0)])
    conn.commit()
    print("commit")
    sleep(60)
 