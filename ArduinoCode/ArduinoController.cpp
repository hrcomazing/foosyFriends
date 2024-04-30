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

void ArduinoController::loop(int newMotorPos[], int newServoPos[]) {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');
        parseData(data);
        updateCurrentMSVals(newMotorPos, newServoPos);
        sendDataBack(motorPosCurr, servoPosCurr);
    }
}

void ArduinoController::parseData(String data) {
    int motorIndex = 0;
    int servoIndex = 0;
    int i = 0;

    int pos = 0;
    while (pos != -1) {
        int nextPos = data.indexOf(',', pos);
        int value = (nextPos == -1) ? data.substring(pos).toInt() : data.substring(pos, nextPos).toInt();
        if (i < numMotors) {
            motorPositions[motorIndex++] = value;
        } else {
            servoPositions[servoIndex++] = value;
        }
        i++;
        pos = (nextPos == -1) ? -1 : nextPos + 1;

    } 

}
void ArduinoController::sendDataBack(int currentMotorPos[], int currentServoPos[]) {
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

void ArduinoController::updateCurrentMSVals(int newMotorPos[], int newServoPos[]) {
    memcpy(motorPosCurr, newMotorPos, sizeof(motorPosCurr));
    memcpy(servoPosCurr, newServoPos, sizeof(servoPosCurr));
}