// MotorServoController.cpp
#include "MotorServoController.h"

MotorServoController::MotorServoController() {
    memset(motorAnglesDesired, 0, sizeof(motorAnglesDesired));
    memset(servoAnglesDesired, 0, sizeof(servoAnglesDesired));
    memset(motorAnglesCurrent, 0, sizeof(motorAnglesCurrent));
    memset(servoAnglesCurrent, 0, sizeof(servoAnglesCurrent));
}

void MotorServoController::parseJson(const String& jsonData) {
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, jsonData);
    if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.c_str());
        return;
    }
    const char* motorKey = "Motor Positions";
    const char* servoKey = "Servo Positions";

    // Extract data
    JsonArray motorArray = doc[motorKey];
    JsonArray servoArray = doc[servoKey];

    // Assuming motorAnglesDesired and servoAnglesDesired are correctly sized
    int motorCount = min(motorArray.size(), (size_t)4); // Example limit size to 4
    for (int i = 0; i < motorCount; i++) {
        motorAnglesDesired[i] = motorArray[i];
    }

    int servoCount = min(servoArray.size(), (size_t)4); // Example limit size to 4
    for (int i = 0; i < servoCount; i++) {
        servoAnglesDesired[i] = servoArray[i];
    }
}

void MotorServoController::sendJsonResponse(int* servoAngles, int* motorAngles) {
    StaticJsonDocument<256> doc;
    JsonArray motorArray = doc.createNestedArray("Motor Positions");
    for (size_t i = 0; i < 4; i++) {
        motorArray.add(motorAngles[i]);
    }
    
    // Add servo angles to JSON document
    JsonArray servoArray = doc.createNestedArray("Servo Positions");
    for (size_t i = 0; i < 4; i++) {
        servoArray.add(servoAngles[i]);
    }

    // Optionally update any internal state or additional fields in the document
    doc["status"] = "OK";

    // Print the JSON document to the Serial
    serializeJson(doc, Serial);

    // Assume updating current positions for internal use
        // Copy each element from motorAngles to motorAnglesCurrent
    for (int i = 0; i < 4; i++) {  // Assuming the size of the arrays is 4
        motorAnglesCurrent[i] = motorAngles[i];
    }

    // Copy each element from servoAngles to servoAnglesCurrent
    for (int i = 0; i < 4; i++) {  // Assuming the size of the arrays is 4
        servoAnglesCurrent[i] = servoAngles[i];
    }
  
}
