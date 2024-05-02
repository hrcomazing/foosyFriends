#ifndef StepperControl_h
#define StepperControl_h

#include <Arduino.h>

class StepperControl {
public:
    StepperControl(int stepPin, int dirPin, int stepsPerRevolution);
    void setLowLim(int lim);
    void setHighLim(int lim);
    void moveTo(float position, float speed);
    void runAtSpeed(float speed, int direction);
    void stop();
    void update();
    int getCurrentPosition();
    float getCurrentPosNorm();

private:
    int _stepPin;               // Pin connected to the step input on the driver
    int _dirPin;                // Pin connected to the direction input on the driver
    int _stepsPerRevolution;    // Number of steps per revolution for this motor
    int _currentPosition;       // Current position in steps
    int _targetPosition;        // Target position in steps
    unsigned long _lastStepTime;// Last time the stepper moved a step
    int _highLim;               // Upper limit of the stepper's range
    int _lowLim;                // Lower limit of the stepper's range
    float _stepDelay;           // Delay between steps in microseconds
    float _maxSpeed;            // Maximum speed in steps per millisecond
    float _speed;               // Current speed in steps per millisecond
    float _acceleration;        // Acceleration in steps per millisecond squared
    int _runDirection;          // Direction of run, 1 for forward, -1 for backward
    enum MotorState { IDLE, MOVING, RUNNING }; // States of the stepper motor
    MotorState _state;          // Current state of the motor

    void stepMotor(int step);   // Function to move the stepper one step
    void runContinuous();       // Function to run motor continuously at set speed
    void stepToTarget();        // Function to move stepper to a specific position
};

#endif
