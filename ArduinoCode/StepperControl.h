#ifndef StepperControl_h
#define StepperControl_h

#include "Arduino.h"

class StepperControl {
  public:
    StepperControl(int stepPin, int dirPin, int stepsPerRevolution);
    void moveTo(float position, float speed);
    void runAtSpeed(float speed, int direction); // Direction determines continuous run direction
    void stop(); // Stops any movement, effectively putting the motor in idle state
    void setIdle(); // Explicitly sets the motor to idle mode
    void update();
    void setLowLim(int lim);
    void setHighLim(int lim);
    int getCurrentPosition();

  private:
    enum MotorState {IDLE, MOVING, RUNNING}; // State of the motor
    MotorState _state; // Current state of the motor

    int _stepPin, _dirPin;
    int _stepsPerRevolution;
    int _currentPosition, _targetPosition;
    int _lowLim;
    int _highLim;
    unsigned long _lastStepTime;
    float _stepDelay;
    int _runDirection; // Added to control the direction in RUNNING state

    void stepMotor(int step);
    void runContinuous();
    void stepToTarget();
};

#endif