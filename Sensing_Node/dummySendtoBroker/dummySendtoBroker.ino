#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Hollar";
const char* password = "123456789";
const char* mqttServer = "192.168.43.174";
const int mqttPort = 1883;
const char* mqttUser = "firedetection";
const char* mqttPassword = "firedetection";
const char* clientid = "esp1";
const char* topicName = "/data/1";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.begin((char *)ssid, (char *)password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

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

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  //work on message that it will publish as a sting and name it message
  //pattern: temperature, humidity, smoke(Mq2), Gas(Mq7), flame, light
  
  String message = "Hello from first ESP32!";
  client.publish(topicName, message.c_str());
  Serial.println("Message sent!");
  delay(2000);  // Publish every 2 seconds
}


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
