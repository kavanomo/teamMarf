void setup() {
  Serial.begin(9600);
  pinMode(7, INPUT);
}

void loop() {
  if (digitalRead(7) == LOW)
  {
    Serial.println("Wassup");
  }
  else
  {
    //This executes when switch is pressed
    Serial.println("Not much HBU");
  }
  

}
