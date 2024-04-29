// MotorServoController.h
#ifndef MotorServoController_h
#define MotorServoController_h

#include <Arduino.h>
#include <ArduinoJson.h>

class MotorServoController {
private:
    static const int numMotors = 4;
    static const int numServos = 4;

public:
    MotorServoController();
    void parseJson(const String& jsonData);
    void sendJsonResponse(int* servoAngles, int* motorAngles); 
    int motorAnglesDesired[numMotors];
    int servoAnglesDesired[numServos];
    int motorAnglesCurrent[numMotors];
    int servoAnglesCurrent[numServos];
};

#endif
