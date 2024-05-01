#include "ArduinoController.h"

ArduinoController::ArduinoController() {
    memset(motorPositions, 0, sizeof(motorPositions));
    memset(servoPositions, 0, sizeof(servoPositions));
    memset(motorPosCurr, 0, sizeof(motorPosCurr));
    memset(servoPosCurr, 0, sizeof(servoPosCurr));
}

void ArduinoController::setup() {
    Serial.begin(115200);
    while (!Serial); // Wait for serial connection
    //Serial.println("Arduino is ready");
}

void ArduinoController::loop(float newMotorPos[], float newServoPos[]) {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');
        parseData(data);
        updateCurrentMSVals(newMotorPos, newServoPos);
        sendDataBack(motorPosCurr, servoPosCurr);
    }
}

void ArduinoController::parseData(String data) {
    //Serial.print("Parsing Data: " + data + " ");  // Debugging output to monitor incoming data
    int motorIndex = 0;
    int servoIndex = 0;
    int pos = 0; // Start position for the search

    while (pos != -1 && pos < data.length()) {
        int nextPos = data.indexOf(',', pos); // Find the next comma

        // Check if the next comma exists, if not, assume end of string
        String valueS = (nextPos == -1) ? data.substring(pos)/*.toInt()*/ : data.substring(pos, nextPos);//.toInt();
        float value = valueS.toFloat();
        //Serial.print("position ");
        //Serial.print(value, 3);
        // Determine where to place the value
        if (motorIndex < numMotors) {
            motorPositions[motorIndex++] = value;
            //Serial.print("Motor "); Serial.print(motorIndex); Serial.print(": "); Serial.print(value, 3);
        } else if (servoIndex < numServos) {
            servoPositions[servoIndex++] = value;
            //Serial.print("Servo "); Serial.print(servoIndex); Serial.print(": "); Serial.print(value, 3);
        }
        // Update position past the comma for the next iteration
        pos = (nextPos == -1) ? -1 : nextPos + 1;
    }

    // Debug output to confirm full array content after parsing
    /*Serial.print("Motor Positions: ");
    for (int i = 0; i < numMotors; i++) {
        Serial.print(motorPositions[i]); Serial.print(" ");
    }
    Serial.print(" ");

    Serial.print("Servo Positions: ");
    for (int i = 0; i < numServos; i++) {
        Serial.print(servoPositions[i]); Serial.print(" ");
    }
    Serial.print(" ");*/
}
    
void ArduinoController::sendDataBack(float currentMotorPos[], float currentServoPos[]) {
    for (int i = 0; i < numMotors; i++) {
        Serial.print(currentMotorPos[i]);
        if (i < numMotors - 1 || numServos > 0) {
            Serial.print(",");
        }
    }
    for (int i = 0; i < numServos; i++) {
        Serial.print(currentServoPos[i]);
        if (i < numServos - 1) {
            Serial.print(",");
        }
    }
    Serial.println();
}

void ArduinoController::updateCurrentMSVals(float newMotorPos[], float newServoPos[]) {
    memcpy(motorPosCurr, newMotorPos, sizeof(motorPosCurr));
    memcpy(servoPosCurr, newServoPos, sizeof(servoPosCurr));
}