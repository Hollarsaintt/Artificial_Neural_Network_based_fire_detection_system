//for reading from sensors and processing sensor readings
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
#include <BH1750.h>
#include <Wire.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <string>

//for publishing on MQTT broker
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Hollar";
const char* password = "123456789";
const char* mqttServer = "192.168.43.174";
const int mqttPort = 1883;
const char* mqttUser = "firedetection";
const char* mqttPassword = "firedetection";
const char* clientid = "esp2"; //client id changes with data points index
const char* topicName = "/data/2"; //topicName changes with data points index

WiFiClient espClient;
PubSubClient client(espClient);


BH1750 lightMeter;
Adafruit_BME680 bme; // I2C
int MQ2_input = 4; 
int MQ7_input = 36;
int Flame_input = 39;
int ledBlink = 14; //for blinking led when message is sent to central system

void setup() {
  Serial.begin(9600);
  pinMode(ledBlink, OUTPUT);
  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  Wire.begin();
  bme.begin();
  lightMeter.begin();

  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);

  //set-up connection with wifi and MQTT broker
  WiFi.begin((char *)ssid, (char *)password);
  //wifi connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  //MQTT connection
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect(clientid, mqttUser, mqttPassword)) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.print("Failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

String space = "  "; //used to separate sensors values in a single string message to be sent by data points
// message[] = ""; //holds the final message to be sent as a string having all sensor values in order 
                   //Temperature - Humidity - Smoke(MQ2) - Gas(MQ7) - Flame - Light
                   //All values are separated with double space characters

void loop() {
  delay(950); //wait 1seconds to conform with publishing every 2 seconds. the remaining 50ms delay is in the code
  // Tell BME680 to begin measurement

  String message = "";
  bme.beginReading();
  delay(50);
  bme.endReading();

  //Temperature and humidity sensor (BME680) //Bme sensors returns float values
  //work not yet done t -> should be calibrated to standard
  float t = bme.temperature;
  
  String ts =  String(t,2);
  message = message + ts + space; //add temperature information to message
  
  

  //Humidity
  //work not yet done h -> should be calibrated to standard
  float h = bme.humidity;
  
  String hs =  String(h,2);
  message = message + hs + space; //add humidity information to message
  
  
  

  //Smoke Sensor
  float MQ2_Aout = analogRead(MQ2_input);  /*Analog value read function*/
  MQ2_Aout = constrain(MQ2_Aout, 0, 4095); //constrain the output to be minimum of zero and maximum of 4095
  
  String ss =  String(MQ2_Aout,2);
  message = message + ss + space; //add smoke information to message
  
  

  //Gas Sensor
  float MQ7_Aout = analogRead(MQ7_input);  /*Analog value read function*/
  MQ7_Aout = constrain(MQ7_Aout, 0, 4095); //constrain the output to be minimum of zero and maximum of 4095
  
  String gs =  String(MQ7_Aout,2);
  message = message + gs + space; //add gas information to message

  //Flame Sensor
  float Flame_Aout = analogRead(Flame_input);  /*Analog value read function*/
  
  //calibration of the flame sensor (changes the logic to positive logic
  Flame_Aout = map(Flame_Aout, 4095, 0, 0, 4095);
  //constrain min sensor value to 0 and max sensor value to 4095
  Flame_Aout = constrain(Flame_Aout, 0, 4095);

  String fs =  String(Flame_Aout,2);
  message = message + fs + space; //add flame information to message
  
  
  //Light Sensor
  float lux = lightMeter.readLightLevel();
  lux = constrain(lux, 0, 4095); //constrain the output to be minimum of zero and maximum of 4095
  
  String ls =  String(lux,2);
  message = message + ls + space; //add light information to message
  
  

  // Now message holds all sensor values as a string separated with space to be published on MQTT broker
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  
  //message pattern: temperature, humidity, smoke(Mq2), Gas(Mq7), flame, light
  client.publish(topicName, message.c_str());
  Serial.println("Message sent!");
  Serial.println(message);
  
  //blink a led after message is sent
  digitalWrite(ledBlink, HIGH);
  delay(1000);  // Publish every 2 seconds there is also a 1second delay at the start of the loop to make it a total of 2seconds delay
  digitalWrite(ledBlink, LOW);
}

//A function that is called to reconnect to MQTT if disconnected at any point
void reconnect() {
  while (!client.connected()) {
    Serial.println("Reconnecting to MQTT...");
    if (client.connect(clientid, mqttUser, mqttPassword)) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.print("Failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}
