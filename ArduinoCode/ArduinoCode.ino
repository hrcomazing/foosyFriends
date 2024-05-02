#include <Servo.h>
#include "StepperControl.h"
#include "ArduinoController.h"
#include <ArduinoJson.h>
#include <string.h>  // For memcpy

//Set up Serialization
ArduinoController coms;

// Constants for the number of motors and servos
static const int numMotors = 4;
static const int numServos = 4;

// Arrays to store the positions of motors and servos
float motorDesired[numMotors] = {0.5,0.5,0.5,0.5};
float servoDesired[numServos] = {0.0,0.0,0.0,0.0};

// Arrays to simulate current positions of motors and servos
float motorCurrent[numMotors] = {0.0,0.0,0.0,0.0};
float servoCurrent[numServos] = {0.0,0.0,0.0,0.0};


Servo servo1, servo2, servo3, servo4; // Declare servo objects
//float servoFlags[4] = {1.0, 1.0, 1.0, 1.0}; // Array to hold flags for each servo (0.0 for false, 1.0 for true)
unsigned long previousMillis[4] = {0, 0, 0, 0}; // Stores the last time each servo was updated
long interval = 100; // Interval at which to move servo (milliseconds)
int currentStep[4] = {0, 0, 0, 0}; // To track the sequence of movements for each servo


//servo 1
int servop4 = 10;

//servo 2
int servop3 = 11;

//servo 3
int servop2 = 12;

//servo 4
int servop1 = 13;

// Motor 4 pin definitions
const int stepPin1 = 2;
const int dirPin1 = 3;
const int limitSwitchLow1 = A6;
const int limitSwitchHigh1 = A7;

// Motor 3 pin definitions
const int stepPin2 = 4;
const int dirPin2 = 5;
const int limitSwitchLow2 = A4;
const int limitSwitchHigh2 = A5;

// Motor 2 pin definitions
const int stepPin3 = 6;
const int dirPin3 = 7;
const int limitSwitchLow3 = A2;
const int limitSwitchHigh3 = A3;

// Motor 1 pin definitions
const int stepPin4 = 8;
const int dirPin4 = 9;
const int limitSwitchLow4 = A0;
const int limitSwitchHigh4 = A1;

const int stepsPerRevolution = 200; // Common for all motors, adjust if needed

// Initialize the stepper control objects for each motor
StepperControl stepper4(stepPin1, dirPin1, stepsPerRevolution);
StepperControl stepper3(stepPin2, dirPin2, stepsPerRevolution);
StepperControl stepper2(stepPin3, dirPin3, stepsPerRevolution);
StepperControl stepper1(stepPin4, dirPin4, stepsPerRevolution);

void setup() {
  coms.setup();

  servo1.attach(servop1); // Attach each servo to a different pin
  servo2.attach(servop2);
  servo3.attach(servop3);
  servo4.attach(servop4);

  pinMode(limitSwitchLow1, INPUT_PULLUP);
  pinMode(limitSwitchHigh1, INPUT_PULLUP);
  pinMode(limitSwitchLow2, INPUT_PULLUP);
  pinMode(limitSwitchHigh2, INPUT_PULLUP);
  pinMode(limitSwitchLow3, INPUT_PULLUP);
  pinMode(limitSwitchHigh3, INPUT_PULLUP);
  pinMode(limitSwitchLow4, INPUT_PULLUP);
  pinMode(limitSwitchHigh4, INPUT_PULLUP);
  
  findLimits(stepper1, limitSwitchLow4, limitSwitchHigh4);
  findLimits(stepper2, limitSwitchLow3, limitSwitchHigh3);
  findLimits(stepper3, limitSwitchLow2, limitSwitchHigh2);
  findLimits(stepper4, limitSwitchLow1, limitSwitchHigh1);

}

void loop() {
  // The loop function can include logic to control each motor based on commands
  // received from the Serial Monitor or another input method.

  if (Serial.available() > 0) {
    
    //update current servo and motor values
    motorCurrent[0] = stepper1.getCurrentPosNorm();
    motorCurrent[1] = stepper2.getCurrentPosNorm();
    motorCurrent[2] = stepper3.getCurrentPosNorm();
    motorCurrent[3] = stepper4.getCurrentPosNorm();

    coms.loop(motorCurrent, servoCurrent);

    servoCurrent[0] = servoCurrent[0] + coms.servoPositions[0];
    servoCurrent[1] = servoCurrent[1] + coms.servoPositions[1];
    servoCurrent[2] = servoCurrent[2] + coms.servoPositions[2];
    servoCurrent[3] = servoCurrent[3] + coms.servoPositions[3];

  }

  //use the updated desired vals and move motor there
  stepper1.moveTo(coms.motorPositions[0], .3);
  stepper2.moveTo(coms.motorPositions[1], .3);
  stepper3.moveTo(coms.motorPositions[2], .3);
  stepper4.moveTo(coms.motorPositions[3], .3);
  stepper1.update();
  stepper2.update();
  stepper3.update();
  stepper4.update();

  unsigned long currentMillis = millis();

  for (int i = 0; i < 4; i++) {
    if (servoCurrent[i] != 0.0 && currentMillis - previousMillis[i] >= interval) {
      previousMillis[i] = currentMillis; // Update last move time for this servo
      
      switch (currentStep[i]) {
        case 0:
          moveServo(i, 90); // Initial vertical position
          interval = 215;
          break;
        case 1:
          moveServo(i, 135); // Slightly back
          interval = 115;
          break;
        case 2:
          moveServo(i, 90); // Return to initial vertical position
          currentStep[i] = -1; // Reset step to stop movement after one cycle
          servoCurrent[i] = 0.0; // Set the flag to 0.0 to indicate that the kick has occurred
          break;
      }
      currentStep[i]++;
    }
  }

}

void findLimits(StepperControl &stepper, int lowSwitch, int highSwitch) {
  //Serial.println("Finding low limit...");
  while (digitalRead(lowSwitch) == HIGH) {
    stepper.runAtSpeed(0.5, -1);
    stepper.update();
    delay(5); // Short delay to slow down the search
  }
  stepper.stop();
  stepper.setLowLim(stepper.getCurrentPosition());

  //Serial.println("Finding high limit...");
  while (digitalRead(highSwitch) == HIGH) {
    stepper.runAtSpeed(0.5, 1);
    stepper.update();
    delay(5); // Short delay to slow down the search
  }
  stepper.stop();
  stepper.setHighLim(stepper.getCurrentPosition());

  //Serial.println("Limits set.");
}

void moveServo(int servoIndex, int angle) {
  switch (servoIndex) {
    case 0:
      servo1.write(angle);
      break;
    case 1:
      servo2.write(angle);
      break;
    case 2:
      servo3.write(angle);
      break;
    case 3:
      servo4.write(angle);
      break;
  }
}
