#ifndef ArduinoController_h
#define ArduinoController_h

#include <Arduino.h>

class ArduinoController {
  private:
    void parseData(String data);
    void sendDataBack(float currentMotorPos[], float currentServoPos[]);

  public:
    ArduinoController();
    void setup();
    void loop(float newMotorPos[], float newServoPos[]);
    void updateCurrentMSVals(float newMotorPos[], float newServoPos[]);
    static const int numMotors = 4; // Number of motors
    static const int numServos = 4; // Number of servos
    float motorPositions[numMotors];
    float servoPositions[numServos];
    float motorPosCurr[numMotors];
    float servoPosCurr[numServos];
};

#endif