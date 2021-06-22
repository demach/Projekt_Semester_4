from umqtt.simple import MQTTClient
from machine import Pin, PWM, SoftI2C
import machine
import ubinascii
import select
from time import sleep, sleep_ms, ticks_ms, ticks_us
import neopixel
from scd30 import SCD30
import ujson as json
from machine import SoftI2C, Pin, Timer
import ads1x15
import urandom as random


with open("settings.json", "r") as rd:
    settings = json.loads(rd.read())
     
    
def connect_network(ssid, psk):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, psk)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
   
connect_network(settings["network"]["ssid"], settings["network"]["psk"])

led_pin = settings["led_strip"]["pin"]
pixel = settings["led_strip"]["pixel"]

np = neopixel.NeoPixel(machine.Pin(led_pin), pixel)
 
for i in range(0, pixel):
    np.fill((0,0,0))
    np.write()
     


i2cbus = SoftI2C(sda=Pin(settings["sensor"]["SCD30"]["SDA"]), scl=Pin(settings["sensor"]["SCD30"]["SCL"]), freq=400000)
scd30 = SCD30(i2cbus, 0x61)
