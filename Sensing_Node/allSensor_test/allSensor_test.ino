//for reading from sensors and processing sensor readings
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
#include <BH1750.h>
#include <Wire.h>
#include <stdio.h>
#include <string.h>


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

  }

void loop() {
  
  bme.beginReading();
  delay(50);
  bme.endReading();

  //Temperature and humidity sensor (BME680) //Bme sensors returns float values
  //work not yet done t -> should be calibrated to standard
  float t = bme.temperature;
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print("*C");
  
  //Humidity
  //work not yet done h -> should be calibrated to standard
  float h = bme.humidity;
  Serial.print("  Humidity: ");
  Serial.print(h);
  Serial.print("%");
  

  //Smoke Sensor
  int MQ2_Aout = analogRead(MQ2_input);  /*Analog value read function*/
  MQ2_Aout = constrain(MQ2_Aout, 0, 4095); //constrain the output to be minimum of zero and maximum of 4095
  
  Serial.print("  SmokeValue: ");
  Serial.print(MQ2_Aout);

  //Gas Sensor
  int MQ7_Aout = analogRead(MQ7_input);  /*Analog value read function*/
  MQ7_Aout = constrain(MQ7_Aout, 0, 4095); //constrain the output to be minimum of zero and maximum of 4095
  
  Serial.print("  GasValue: ");
  Serial.print(MQ7_Aout);

  //Flame Sensor
  int Flame_Aout = analogRead(Flame_input);  /*Analog value read function*/
  
  //calibration of the flame sensor (changes the logic to positive logic
  Flame_Aout = map(Flame_Aout, 4095, 0, 0, 4095);
  //constrain min sensor value to 0 and max sensor value to 4095
  Flame_Aout = constrain(Flame_Aout, 0, 4095);

  Serial.print("  FlameValue: ");
  Serial.print(Flame_Aout);
  
  
  //Light Sensor
  float lux = lightMeter.readLightLevel();
  lux = constrain(lux, 0, 4095); //constrain the output to be minimum of zero and maximum of 4095
  
  Serial.print("  LightValue: ");
  Serial.println(lux);
  
  //blink a led after message is sent
  digitalWrite(ledBlink, HIGH);
  delay(1000);  // Publish every 2 seconds there is also a 1second delay at the start of the loop to make it a total of 2seconds delay
  digitalWrite(ledBlink, LOW);
  delay(950); 
}
