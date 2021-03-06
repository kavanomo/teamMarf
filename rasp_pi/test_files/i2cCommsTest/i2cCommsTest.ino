#include <Wire.h>

// definitions
#define SLAVE_ADDRESS 0x04

// message definitions
#define LEFT 0
#define RIGHT 1

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

// num of steps required to make a turn
#define STEPS 2

// STRUCTS
struct command {
  byte action_bit;
  byte num_turns;
  byte direc;
};

// GLOBAL DEFS
byte msg;
bool new_msg;
bool sol_on;
bool done;

void setup() {
  // i2c CONNECTION
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveCmd);
  Wire.onRequest(sendStatus);

  // COMPONENT SETUP
  pinMode(BUCKETD1, OUTPUT);
  pinMode(BUCKETD2, OUTPUT);
  pinMode(TOWERD1, OUTPUT);
  pinMode(TOWERD2, OUTPUT);
  pinMode(VACUUMD1, OUTPUT);
  pinMode(VACUUMD2, OUTPUT);
  pinMode(SOLENOID, OUTPUT);
  pinMode(TOWERLIMIT, INPUT);

  pintMode(

  // LIMIT SWITCH INTERRUPT
  attachInterrupt(digitalPinToInterrupt(TOWERLIMIT), towerISR, RISING);
}

void initialize() {
  digitalWrite(VACUUMD1, 1);
  digitalWrite(TOWERD1, 1);
  digitalWrite(TOWERD2, 1);
  sol_on = false;
  new_msg = false;
}

void deinitialize() {
  digitalWrite(VACUUMD1, 0);
  digitalWrite(SOLENOID, 0);
}

void towerISR()
{
  digitalWrite(TOWERD1, 0);
  digitalWrite(TOWERD2, 0);
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
    done = false;
    command parsed_msg = parseMessage(msg);

    switch (parsed_msg.action_bit)
    { 
      // init
      case 0:
      {
        initialize();
      }
      // vacuuming  
      case 1:
      {
        digitalWrite(SOLENOID, sol_on);
        if (sol_on == false)
        {
          //TODO: Figure out which way is up and which is down, and also how much a step is
          digitalWrite(TOWERD2,0);
          digitalWrite(TOWERD1, 1);
        }
        // if vacuuming, bring up the scan tower a little until it gets picked up
        else
        {
            digitalWrite(TOWERD1, 0);
            digitalWrite(TOWERD2, 1);
          }  
        }
      }
      // rotate bucket tree  
      case 2:
      {
        //TODO: Figure these directions out
        // 1 - CW, 0 - CCW
        if (parsed_msg.direc == 0)
        {
          digitalWrite(BUCKETD1, 1);
          digitalWrite(BUCKETD2, 0);
        }
        else
        {
          digitalWrite(BUCKETD1, 0);
          digitalWrite(BUCKETD2, 1);
        }
        int numSteps = (parsed_msg.num_turns * STEPS);
        for (int j = 0; j < numSteps; j++)
        {
          digitalWrite(VACUUMD2, 1);
          delay(100);
          digitalWrite(VACUUMD2, 0);
        }
        break;
      }
      // deinit 
      case 3:
      {
        deinitialize();
        break;
      }
      default:
      {
        break;
      }
    }
    done = true;
   }
}

void receiveCmd(int num_bytes) {
  msg = Wire.read();
  new_msg = true;
}

// returns whether or not Uno is completed its actions
void sendStatus() {
  Wire.write(done);
}
