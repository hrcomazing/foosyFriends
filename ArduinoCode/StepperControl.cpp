#include "StepperControl.h"

StepperControl::StepperControl(int stepPin, int dirPin, int stepsPerRevolution) {
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    _stepPin = stepPin;
    _dirPin = dirPin;
    _stepsPerRevolution = stepsPerRevolution;
    _currentPosition = 0;
    _targetPosition = 0;
    _lastStepTime = 0;
    _highLim = 0;
    _lowLim = 0;
    _state = IDLE; // Motor starts in an idle state
    _runDirection = 1; // Default direction
}

void StepperControl::setLowLim(int lim){
    _lowLim = lim;
}

void StepperControl::setHighLim(int lim){
    _highLim = lim;
}

void StepperControl::moveTo(float position, float speed) {
    _targetPosition = (int)(_lowLim + position*(_highLim - _lowLim));
    _stepDelay = 2000 * (1 - speed);
    _state = MOVING;
}

void StepperControl::runAtSpeed(float speed, int direction) {
    _stepDelay = 2000 * (1 - speed);
    _runDirection = direction >= 0 ? 1 : -1; // Determine direction based on input
    _state = RUNNING;
}

void StepperControl::stop() {
    _state = IDLE;
}

void StepperControl::setIdle() {
    _state = IDLE;
}

void StepperControl::update() {
    switch (_state) {
        case MOVING:
            stepToTarget();
            break;
        case RUNNING:
            runContinuous();
            break;
        case IDLE:
            // Do nothing
            break;
    }
}

void StepperControl::stepMotor(int step) {
    digitalWrite(_dirPin, step > 0 ? HIGH : LOW);
    digitalWrite(_stepPin, HIGH);
    delayMicroseconds(100); // Short pulse to trigger one step
    digitalWrite(_stepPin, LOW);
}

void StepperControl::runContinuous() {
    unsigned long currentTime = micros();
    if (currentTime - _lastStepTime >= _stepDelay) {
        stepMotor(_runDirection);
        _currentPosition += _runDirection;
        _lastStepTime = currentTime;
    }
}

void StepperControl::stepToTarget() {
    unsigned long currentTime = micros();
    if (currentTime - _lastStepTime >= _stepDelay) {
        if (_currentPosition < _targetPosition) {
            stepMotor(1);
            _currentPosition++;
        } else {
            stepMotor(-1);
            _currentPosition--;
        }
        _lastStepTime = currentTime;
    }
}

int StepperControl::getCurrentPosition() {
    return _currentPosition;
}
