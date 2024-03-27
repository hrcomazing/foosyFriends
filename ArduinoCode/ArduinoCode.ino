#include <Servo.h>
#include "StepperControl.h"

StepperControl stepper(8, 9, 200); // stepPin, dirPin, stepsPerRevolution

void setup() {
  // Set the target position and speed. Position is in steps, speed is 0 (fast) to 1 (slow).
  stepper.moveTo(400, 0.5); // Move to position 400 with medium speed
}

void loop() {
  // Continuously updates the motor to move towards the target position
  stepper.update();
  // Add any other logic you need here. The motor movement will be handled in the background.
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