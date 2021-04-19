#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include "DHT.h"


#define DHTPIN 4
#define DHTTYPE DHT11
//#define DHTTYPE DHT22

#define MQTT_PUB_TEMP "esp32/dht/temperature"
#define MQTT_PUB_HUM  "esp32/dht/humidity"

#define ADSValue 0.03125

DHT dht(DHTPIN, DHTTYPE);

float temperatur_accumulated = 0.0;

float temperature_dht=0.0;
float humidity_dht=0.0;

unsigned long previousMillis = 0;
const long interval = 10000;

const char* SSID = "your ssid";
const char* PSK = "your psk";
const char* MQTT_BROKER = "your broker";

Adafruit_ADS1115 ads;
float Voltage = 0.0;
float Temperature = 0.0;


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


void onMqttPublish(uint16_t packetId) {
  Serial.print("Publish acknowledged.");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}



void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(MQTT_BROKER, 1883);
  client.setKeepAlive(60);

  ads.begin(0x48);
  // ads.setGain(GAIN_TWOTHIRDS);     // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)     last value has to be set in ADSValue 
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  dht.begin();
  

//  client.onPublish(onMqttPublish);
  client.setCallback(callback);
  
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(SSID);

  WiFi.begin(SSID, PSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(char* topic, byte* message, unsigned int length){
  /*Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");*/
  String messageTemp;

  for(int i = 0; i<length; i++){
    //Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  //Serial.println();


  if(String(topic) == "/home/start_measurement"){
    Serial.print("message is: ");
    Serial.print(messageTemp);
    Serial.println();
    if(messageTemp == "1"){
      measurement(1);
    }
    if(messageTemp == "10"){
      measurement(10);
    }
    if(messageTemp == "100"){
      measurement(100);
    }
    if(messageTemp == "1000"){
      measurement(1000);
    }
  }
  
}


void measurement(int repetitions){
  int16_t adc0;
  temperatur_accumulated = 0.0;
  for(int i=0; i<repetitions; i++){

    //read analog signal and multiply received value with adc resolution

    adc0 = ads.readADC_SingleEnded(0);
    Voltage = (adc0 * ADSValue) / 1000;
    
    // add values up for later averaging temperature
    temperatur_accumulated += Voltage * 100;
    

    delay(10);
  }
  
  humidity_dht = dht.readHumidity();
  temperature_dht = dht.readTemperature();


  Temperature = temperatur_accumulated/repetitions;

  if (!client.connected()) {
    reconnect();
  }
  //publish data from sensors to different mqtt topics 
  client.publish("/home/temperature", String(Temperature).c_str());
  client.publish("/home/dht/humidity", String(humidity_dht).c_str());
  client.publish("/home/dht/temperature", String(temperature_dht).c_str());
  client.publish("/home/finish", "Finished with this measurement");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("/home/start_measurement");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  
  //detect if mqtt client is still connected
  if (!client.connected()) {
    reconnect();
  }
  //let client run forever
  client.loop();
}
