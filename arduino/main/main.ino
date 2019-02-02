#include <Wire.h>

// definitions
#define SLAVE_ADDRESS 0x08

// message definitions
#define LEFT 0
#define RIGHT 1
#define PICKUP 0
#define VACUUM 1
#define ROTATE 2
#define INIT 3

// COMPONENT DEFS
// D1 - on/off, D2 - direction
#define BUCKETD1 0
#define BUCKETD2 1
#define TOWERD1 2
#define TOWERD2 3
#define VACUUMD1 4
#define VACUUMD2 5
#define SOLENOID 6
#define TOWERLIMIT 7

// STRUCTS
struct command {
  byte action_bit;
  byte num_turns;
  byte direc;
}

// GLOBAL DEFS
byte msg;
bool new_msg = false;
bool sol_on = false;

void setup() {
  // i2c CONNECTION
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  //Wire.onRequest(sendData);

  // COMPONENT SETUP
  pinMode(BUCKETD1, OUTPUT);
  pinMode(BUCKETD2, OUTPUT);
  pinMode(TOWERD1, OUTPUT);
  pinMode(TOWERD2, OUTPUT);
  pinMode(VACUUMD1, OUTPUT);
  pinMode(VACUUMD2, OUTPUT);
  pinMode(SOLENOID, OUTPUT);
  pinMode(TOWERLIMIT, INPUT);

}

void init() {
  digitalWrite(VACUUMD1, 1);
}

void deinit() {
  digitalWrite(VACUUMD1, 0);
  digitalWrite(SOLENOID, 0);
  sol_on = false;
}

command parseMessage(byte msg) {
  command parsed_msg;
  parsed_msg.action_bit = msg >> 3;
  parsed_msg.num_turns = (msg >> 1) & B00000011;
  parsed_msg.direc = msg & B00000001;
  return parsed_msg;
}

void loop() {
  delay(10);
  if (new_msg)
  {
    new_msg = false;
    parsed_msg = parseMessage(msg);

    
   }
}

void receiveData(int num_bytes) {
  msg = Wire.read();
  new_msg = true;
}
