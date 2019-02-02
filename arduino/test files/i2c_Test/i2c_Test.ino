#include <Wire.h>

#define SLAVE_ADDRESS 0x08

char msg[50];

void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

}

void loop() {
  delay(100);
}

void receiveData(int byteCount) {
  int i = 0;
  while (Wire.available())
  {
    msg[i] = Wire.read();
    i ++;
  }
  msg[i] = '\0';
  Serial.print(msg);
  Serial.print(i);
}

void sendData() {
  Wire.write("ARDU");
}
