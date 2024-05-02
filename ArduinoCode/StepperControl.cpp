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
    _state = IDLE;
    _runDirection = 1;
    _initialStepDelay = 2000;  // Initial step delay for smooth start
    _minStepDelay = 200;       // Minimum step delay at full speed
    _maxStepDelay = 2000;      // Maximum step delay for slowest speed or start/stop
    _acceleration = 100;       // Number of steps to reach full speed
    _stepDelay = _initialStepDelay;
    _speedIncrement = (_maxStepDelay - _minStepDelay) / _acceleration;
}

void StepperControl::setLowLim(int lim) {
    _lowLim = lim;
}

void StepperControl::setHighLim(int lim) {
    _highLim = lim;
}

void StepperControl::moveTo(float position, float speed) {
    int newTarget = (int)(_lowLim + position * (_highLim - _lowLim));
    if (newTarget != _targetPosition) {
        _targetPosition = newTarget;
        _state = MOVING;
    }
    _maxSpeed = speed; // Adjust the maximum speed based on input
}

void StepperControl::runAtSpeed(float speed, int direction) {
    _runDirection = direction >= 0 ? 1 : -1;
    _maxSpeed = speed;
    _state = RUNNING;
}

void StepperControl::stop() {
    _state = IDLE;
}

void StepperControl::update() {
    if (_state != IDLE) {
        unsigned long currentTime = micros();
        if (currentTime - _lastStepTime >= _stepDelay) {
            _lastStepTime = currentTime;
            if (_state == MOVING) {
                stepToTarget();
            } else if (_state == RUNNING) {
                runContinuous();
            }
        }
    }
}

void StepperControl::stepMotor(int step) {
    digitalWrite(_dirPin, step > 0 ? HIGH : LOW);
    digitalWrite(_stepPin, HIGH);
    delayMicroseconds(100);  // Short pulse to trigger one step
    digitalWrite(_stepPin, LOW);
}

void StepperControl::runContinuous() {
    if (_speed < _maxSpeed) {
        _speed += _acceleration;
        if (_speed > _maxSpeed) {
            _speed = _maxSpeed;
        }
    } else if (_speed > _maxSpeed) {
        _speed -= _acceleration;
        if (_speed < _maxSpeed) {
            _speed = _maxSpeed;
        }
    }
    _stepDelay = 1000000 / _speed;
    stepMotor(_runDirection);
    _currentPosition += _runDirection;
}

void StepperControl::stepToTarget() {
    int stepsToGo = abs(_targetPosition - _currentPosition);
    if (stepsToGo > 0) {
        int direction = (_currentPosition < _targetPosition) ? 1 : -1;
        if (stepsToGo < _acceleration) {
            _speed -= _acceleration;  // Decelerate when approaching the target
            if (_speed < _minStepDelay) _speed = _minStepDelay;
        } else {
            _speed += _acceleration;  // Accelerate
            if (_speed > _maxSpeed) _speed = _maxSpeed;
        }
        _stepDelay = 1000000 / _speed;  // Calculate new delay based on speed
        stepMotor(direction);
        _currentPosition += direction;
    } else {
        _state = IDLE;  // Stop the motor when the target is reached
    }
}

int StepperControl::getCurrentPosition() {
    return _currentPosition;
}

float StepperControl::getCurrentPosNorm() {
    if (_highLim == _lowLim) {
        return 0.5; // Avoid division by zero
    }
    return float(_currentPosition - _lowLim) / float(_highLim - _lowLim);
}