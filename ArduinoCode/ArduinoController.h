#ifndef ArduinoController_h
#define ArduinoController_h

#include <Arduino.h>

class ArduinoController {
  private:
    void parseData(String data);
    void sendDataBack(int currentMotorPos[], int currentServoPos[]);

  public:
    ArduinoController();
    void setup();
    void loop(int newMotorPos[], int newServoPos[]);
    void updateCurrentMSVals(int newMotorPos[], int newServoPos[]);
    static const int numMotors = 4; // Number of motors
    static const int numServos = 4; // Number of servos
    int motorPositions[numMotors];
    int servoPositions[numServos];
    int motorPosCurr[numMotors];
    int servoPosCurr[numServos];
};

#endif