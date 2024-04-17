#include <Servo.h>
#include "StepperControl.h"

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
StepperControl stepper1(stepPin1, dirPin1, stepsPerRevolution);
StepperControl stepper2(stepPin2, dirPin2, stepsPerRevolution);
StepperControl stepper3(stepPin3, dirPin3, stepsPerRevolution);
StepperControl stepper4(stepPin4, dirPin4, stepsPerRevolution);

void setup() {
  Serial.begin(9600);
  pinMode(limitSwitchLow1, INPUT_PULLUP);
  pinMode(limitSwitchHigh1, INPUT_PULLUP);
  pinMode(limitSwitchLow2, INPUT_PULLUP);
  pinMode(limitSwitchHigh2, INPUT_PULLUP);
  pinMode(limitSwitchLow3, INPUT_PULLUP);
  pinMode(limitSwitchHigh3, INPUT_PULLUP);
  pinMode(limitSwitchLow4, INPUT_PULLUP);
  pinMode(limitSwitchHigh4, INPUT_PULLUP);
  
  findLimits(stepper1, limitSwitchLow1, limitSwitchHigh1);
  findLimits(stepper2, limitSwitchLow2, limitSwitchHigh2);
  findLimits(stepper3, limitSwitchLow3, limitSwitchHigh3);
  findLimits(stepper4, limitSwitchLow4, limitSwitchHigh4);
}

void loop() {
  // The loop function can include logic to control each motor based on commands
  // received from the Serial Monitor or another input method.
  stepper1.moveTo(.7, .3);
  stepper2.moveTo(.7, .3);
  stepper3.moveTo(.7, .3);
  stepper4.moveTo(.7, .3);
  stepper1.update();
  stepper2.update();
  stepper3.update();
  stepper4.update();
}

void findLimits(StepperControl &stepper, int lowSwitch, int highSwitch) {
  Serial.println("Finding low limit...");
  while (digitalRead(lowSwitch) == HIGH) {
    stepper.runAtSpeed(0.2, -1);
    stepper.update();
    delay(5); // Short delay to slow down the search
  }
  stepper.stop();
  stepper.setLowLim(stepper.getCurrentPosition());

  Serial.println("Finding high limit...");
  while (digitalRead(highSwitch) == HIGH) {
    stepper.runAtSpeed(0.1, 1);
    stepper.update();
    delay(5); // Short delay to slow down the search
  }
  stepper.stop();
  stepper.setHighLim(stepper.getCurrentPosition());

  Serial.println("Limits set.");
  //Serial.print("Low limit: ");
  //Serial.println(stepper._lowLim);
  //Serial.print("High limit: ");
  //Serial.println(stepper._highLim);
}
/*
Servo servo;  // Create a servo object
int servoPin = 10;  // Servo is connected to digital pin 9

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 bits per second
  servo.attach(servoPin);  // Attach the servo to the servoPin
}

void loop() {
  if (Serial.available() > 0) {
    String jsonData = Serial.readStringUntil('\n');  // Read the incoming data until newline
    int angle = parseJson(jsonData);  // Parse the angle from the JSON data
    if (angle >= 0 && angle <= 180) {
      servo.write(angle);  // Move the servo to the specified angle
      sendJsonResponse(angle);  // Send back a JSON response
    }
  }
}

int parseJson(String jsonData) {
  // Simple parsing: Assumes the format {"angle":90}
  int startPos = jsonData.indexOf(":") + 1;
  int endPos = jsonData.indexOf("}");
  String angleStr = jsonData.substring(startPos, endPos);
  return angleStr.toInt();  // Convert angle to integer
}

void sendJsonResponse(int angle) {
  String jsonResponse = "{\"status\":\"OK\",\"angle\":";
  int angleFound = servo.read();
  jsonResponse += angleFound;
  jsonResponse += "}";
  Serial.println(jsonResponse); 
  Serial.write(angle); // Send the JSON response
}
*/