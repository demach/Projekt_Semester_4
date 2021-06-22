#from boot import *
# MQTT configuration
config = settings["mqtt"]
durchschnitt_liste =[0,0,0]
sleep(2)
print("measuring")
#dht_sensor.measure()
#print(dht_sensor.temperature(), dht_sensor.humidity())

#sensor_data = 0

from machine import SoftI2C, Pin, Timer
import ads1x15
from time import sleep_ms, ticks_ms, ticks_us, sleep
from array import array

addr = 72
gain = 4

i2c = SoftI2C(sda=Pin(16), scl=Pin(17), freq=400000)

# for the Pycom branch, use:
# i2c = I2C()
print(i2c.scan())
ads = ads1x15.ADS1115(i2c, addr, gain)
#print(ads.read())

#
# Interrupt service routine for data acquisition
# called by a timer interrupt
#


index_put = 0
ADC_RATE = 1000

# set the conversion rate to 860 SPS = 1.16 ms; that leaves about
# 3 ms time for processing the data with a 5 ms timer
ads.set_conv(6, 0) # start the first conversion


print(ads.read_rev())

# for i in range(1000):
#     #print(i, 0.33 * 0.0806 * float(analog_sensor.read()))
#     sensor_data += float(analog_sensor.read())
#     sleep(0.01)
# 
# print((sensor_data * 0.33 * 0.0832)/1000)
    
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
    
    if topic == b"projekt4/rgb_value":
        message = json.loads(msg)
        print(message)
        np.fill((message["red"], message["green"],message["blue"]))
        np.write()
        
    
        
    

# #Create an instance of MQTTClient 
client = MQTTClient(config['id'], config['broker'], user=(str(config['user']) + str(random.randint(0,100))), password=config['psk'], port=config['port'])
# # Attach call back handler to be called on receiving messages
client.set_callback(onMessage)
client.connect()
# client.publish("{}/startup".format(config["topic"]), "ESP_Projekt4 is connected")
client.subscribe("#")
while True:
    client.check_msg()
    
    val = 0
    for i in range(60):
        val += ads.read_rev()
        #print(val, "value")
        sleep(1)
    analog = float(ads.raw_to_v(val/60))*100
    
    try:
        Messwerte=scd30.read_measurement()
    
    except:
        machine.reset()
        
    print(analog)
    print("Grad: {} \t Co2: {} \t Luftfeuchte: {}".format(Messwerte[1],Messwerte[0], Messwerte[2]))
    
    durchschnitt_liste = [durchschnitt_liste[1], durchschnitt_liste[2], int(Messwerte[0])]
    
    durschnitt_co2 = sum(durchschnitt_liste)/float(len(durchschnitt_liste))
    
    if durschnitt_co2 < 1000:
        np.fill((100,0,20))
        np.write()
    elif durschnitt_co2 >= 1000 and durschnitt_co2 < 2000:
        np.fill((0,100,0))
        np.write()
    else:
        np.fill((100,0,0))
        np.write()
    
    dict_ausgabe = {"Sensirion SCD30_Co2": Messwerte[0], "Sensirion SCD30_Temp": Messwerte[1], "Sensirion SCD30_Hum": Messwerte[2], "LM35": analog}
    #print(dict_ausgabe)
    try:
        client.publish("{}/scd30".format(config["topic"]),"{}".format(Messwerte[1]))
    except: print("Failed Publish")
    
    try:
        client.publish("{}/messwerte".format(config["topic"]),"{}".format(json.dumps(dict_ausgabe)))
        #print(dict_ausgabe)
    except: print("Failed Publish")

    
    #sleep(60)
