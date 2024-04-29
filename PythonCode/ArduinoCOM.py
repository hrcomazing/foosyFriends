import serial
import json
import time

class ArduinoCOM:
    def __init__(self, port, baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate)
        self.motorDesired = []
        self.servoDesired = []
        self.motorCurrent = []
        self.servoCurrent = []
        time.sleep(2)  # Wait for the connection to establish
        print(f"Connected to Arduino on port {port} at {baud_rate} baud rate.")

    def send_positions(self, motorPos, servoPos):
        """Sends desired positions to the Arduino."""
        self.motorDesired = motorPos
        self.servoDesired = servoPos
        data = {"Motor Positions": motorPos, "Servo Positions": servoPos}
        command = json.dumps(data)
        self.ser.write((command + "\n").encode())  # Send the command
        print(f"Sent to Arduino: {command}")
        time.sleep(0.1)  # Give Arduino time to respond
        '''if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()  # Read the response
            print(f"Received from Arduino: {response}")
            self.save_json_response(response)'''

    def receive_positions(self):
        """Receives and updates current positions from the Arduino."""
        if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()
            print(f"Received current positions from Arduino: {response}")
            self.save_json_response(response)
            positions = json.loads(response)
            self.motorCurrent = positions.get("Motor Positions", [])
            self.servoCurrent = positions.get("Servo Positions", [])
            return positions
        else:
            print("No data to receive.")
            return None

    def save_json_response(self, response):
        """Saves the Arduino's JSON response to a file."""
        data = json.loads(response)
        with open("arduino_response.json", "w") as file:
            json.dump(data, file, indent=4)
            print("Response saved to arduino_response.json.")

    def close(self):
        """Closes the serial connection."""
        self.ser.close()
        print("Serial connection closed.")


'''def main():
    # Create an instance of ArduinoCOM with the correct COM port
    arduino = ArduinoCOM(port='COM3')  # Replace 'COM3' with your actual COM port
    motor_positions_desired = [.5, .5, .5, .5]  # Example motor positions
    servo_positions_desired = [1, 1, 1, 1]  # Example servo positions
    motor_positions_current = [.5, .5, .5, .5]  # Example motor positions
    servo_positions_current = [1, 1, 1, 1]  # Example servo positions

    try:
        # Sending desired positions to the Arduino
        arduino.send_positions(motor_positions_desired, servo_positions_desired)

        # Receiving and printing current positions from the Arduino
        current_positions = arduino.receive_positions()
        if current_positions is not None:
            motor_positions_current = arduino.motorCurrent  # Example motor positions
            servo_positions_current = arduino.servoCurrent  # Example servo positions
            print("Current Motor Positions:", motor_positions_current)
            print("Current Servo Positions:", servo_positions_current)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Ensure the serial connection is closed properly
        arduino.close()
'''
'''if __name__ == '__main__':
    main()'''

