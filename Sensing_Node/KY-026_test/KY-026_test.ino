int Sensor_input = 39;    /*Digital pin 39 for sensor input*/
void setup() {
  Serial.begin(9600);  /*baud rate for serial communication*/
}
void loop() {
  int Flame_Aout = analogRead(Sensor_input);  /*Analog value read function*/
   //calibration of the flame sensor (changes the logic to positive logic
  Flame_Aout = map(Flame_Aout, 4095, 0, 0, 4095);
  //constrain min sensor value to 0 and max sensor value to 4095
  Flame_Aout = constrain(Flame_Aout, 0, 4095);
  Serial.print("Flame Sensor: ");  
  Serial.print(Flame_Aout);   /*Read value printed*/
  Serial.print("\t");
  Serial.print("\t");
  Serial.println();

  delay(1000);                 /*DELAY of 1 sec*/
}
