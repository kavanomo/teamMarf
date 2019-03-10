#include <Wire.h>

// definitions
#define SLAVE_ADDRESS 0x04

// message definitions
#define LEFT 0
#define RIGHT 1

// COMPONENT DEFS
// D1 - on/off, D2 - direction
#define BUCKETD1 8
#define BUCKETD2 9
#define TOWERD1 2
#define TOWERD2 3
#define VACUUMD1 4
#define VACUUMD2 5
#define SOLENOID 6
#define TOWERLIMIT 7

#define TOWERPD A1
#define VACUUMPD A0

// photodiode thresholds
#define TOWERPDTHRESH 3
#define VACUUMPDTHRESH 3

// num of steps required to make a turn
#define STEPS1 33
#define STEPS2 67
#define STEPS3 100

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

  Serial.println("Let's go!");

  // LIMIT SWITCH INTERRUPT
  attachInterrupt(digitalPinToInterrupt(TOWERLIMIT), towerISR, RISING);
}

void initialize() {
  Serial.println("Ready!");
}

void deinitialize() {
  Serial.println("Good bye!");
}

void towerISR()
{
  Serial.println("Tower ISR!");
}

command parseMessage(byte msg) {
  command parsed_msg;
  parsed_msg.action_bit = msg >> 3;
  parsed_msg.num_turns = (msg >> 1) & B00000011;
  parsed_msg.direc = msg & B00000001;
  return parsed_msg;
}

void loop() {
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
        break;
      }
      // vacuuming  
      case 1:
      {
        Serial.println("Vacuuming!");
        sol_on = !sol_on;
        // move down by one so we don't interfere when the vacuum goes back
        if (sol_on == false)
        {
          //TODO: Figure out which way is up and which is down, and also how much a step is
          Serial.println("Bringing tower down a little");
        }
        // if vacuuming, bring up the scan tower a little until it gets picked up
        else
        {
          Serial.println("Bringing tower up a little");
        }
        break;
      }
      // rotate bucket tree  
      case 2:
      {
        Serial.println("Rotating!");
        int direction = parsed_msg.direc;
        if (direction == 0){
          digitalWrite(BUCKETD2, LOW);
          Serial.println("The direction was 0");
        }
        else {
          digitalWrite(BUCKETD2, HIGH);
          Serial.println("The direction was 1");
        }

        int numSteps = parsed_msg.num_turns;
        if (numSteps == 1){
          Serial.println("1 Turn");
          numSteps = STEPS1;
        }
        else if (numSteps == 2){
          Serial.println("2 Turn");
          numSteps = STEPS2;
        }
        else if (numSteps == 3){
          Serial.println("3 Turn");
          numSteps = STEPS3;
        }
        
        for (int i = 0; i < 1; i++)
        {
          Serial.println("Step");
          digitalWrite(BUCKETD1, HIGH);
          delay(15);
          digitalWrite(BUCKETD1, LOW);
          delay(15); 
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
  Serial.println("New message received!");
  new_msg = true;
}

// returns whether or not Uno is completed its actions
void sendStatus() {
  Wire.write(done);
}
