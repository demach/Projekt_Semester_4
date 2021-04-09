#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include "DHT.h"


#define DHTPIN 4
#define DHTTYPE DHT11

#define MQTT_PUB_TEMP "esp32/dht/temperature"
#define MQTT_PUB_HUM  "esp32/dht/humidity"

DHT dht(DHTPIN, DHTTYPE);

float temp =0.0;
float hum=0.0;

unsigned long previousMillis = 0;
const long interval = 10000;

const char* SSID = "hm.dslmobil.FRITZ!Box 7590 VJ";
const char* PSK = "30036950525569455340";
const char* MQTT_BROKER = "192.168.178.77";

Adafruit_ADS1115 ads;
float Voltage = 0.0;
float Temperature = 0.0;
float Reading = 0.0;
float tempmap = 0.0;
float anotherone = 0.0;


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

  ads.begin(0x48);
  ads.setGain(GAIN_TWOTHIRDS);

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
  for(int i=0; i<repetitions; i++){
    adc0 = ads.readADC_SingleEnded(0);
    Voltage = (adc0 * 0.1875) / 1000;
    //Temperature = (adc0 * 0.1875) * 0.0806;
    //Reading = (adc0 * 0.1875);
    anotherone = (Voltage * 100);
    //tempmap = map(Reading, 0, 307, 0, 150);
    /*String Str_temp = String(tempmap,4);
    String Str_voltage = String(Voltage, 4);
    String Str_value = String(Reading, 4);
    String Str_temperature = String(Temperature, 4);*/
    String Str_anotherone = String(anotherone, 4);
    /*client.publish("/home/voltage", Str_voltage.c_str());
    client.publish("/home/value", Str_value.c_str());
    client.publish("/home/temperature", Str_temperature.c_str());
    client.publish("/home/temp", Str_temp.c_str());*/
    client.publish("/home/anotherone", Str_anotherone.c_str());
    delay(25);
  }
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

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
/*
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval){
    previousMillis = currentMillis;

    /hum = dht.readHumidity();
    temp= dht.readTemperature();

    if(isnan(temp) || isnan(hum)){
      Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }

    // Publish an MQTT message on topic esp32/dht/temperature
    //uint16_t packetIdPub1 = client.publish(MQTT_PUB_TEMP, 1, true, String(temp).c_str());    
    client.publish(MQTT_PUB_TEMP, String(temp).c_str());                        
    //Serial.printf("Publishing on topic %s at QoS 1, packetId: %i", MQTT_PUB_TEMP, packetIdPub1);
    Serial.printf("Message: %.2f temp\n", temp);

    // Publish an MQTT message on topic esp32/dht/humidity
    client.publish(MQTT_PUB_HUM, String(hum).c_str()); 
    //uint16_t packetIdPub2 = client.publish(MQTT_PUB_HUM, 1, true, String(hum).c_str());                            
    //Serial.printf("Publishing on topic %s at QoS 1, packetId %i: ", MQTT_PUB_HUM, packetIdPub2);
    Serial.printf("Message: %.2f hum\n", hum);
    
  }
*/
  
  /*adc0 = ads.readADC_SingleEnded(0);
  Voltage = (adc0 * 0.0625) / 1000;
  Temperature = (adc0 * 0.0625) * 0.0806;
  String Str_voltage = String(Voltage, 4);
  String Str_temperature = String(Temperature, 4);*/
  /*snprintf (msg, 50, "Alive since %ld milliseconds", millis());
  Serial.print("Publish message: ");
  Serial.println(msg);
  client.publish("/home/finish", "Finished with this measurement");*/
  //delay(5000);
}
