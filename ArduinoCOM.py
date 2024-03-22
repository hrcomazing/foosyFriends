import serial
import json
import time


class ArduinoCOM:
    def __init__(self, port, baud_rate=9600):
        self.ser = serial.Serial(port, baud_rate)
        time.sleep(2)  # Wait for the connection to establish
        print(f"Connected to Arduino on port {port} at {baud_rate} baud rate.")

    def send_servo_angle(self, angle):
        """Sends a command to the Arduino to move the servo to a specified angle."""
        command = json.dumps({"angle": angle})
        self.ser.write((command + "\n").encode())  # Send the command
        print(f"Sent to Arduino: {command}")

        # Wait for the response
        time.sleep(0.1)  # Give Arduino time to respond
        if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()  # Read the response
            print(f"Received from Arduino: {response}")
            self.save_json_response(response)

    def save_json_response(self, response):
        """Saves the Arduino's JSON response to a file."""
        data = json.loads(response)
        with open("arduino_response.json", "w") as file:
            json.dump(data, file, indent=4)
            print("Response saved to arduino_response.json")

    def close(self):
        """Closes the serial connection."""
        self.ser.close()
        print("Serial connection closed.")


'''if __name__ == "__main__":
    try:
        controller = ArduinoCOM('COM3')  # Adjust 'COM3' to your Arduino's serial port
        while True:
            angle_input = input("Enter servo angle (0 to 180) or 'exit' to quit: ")
            if angle_input.lower() == 'exit':
                break
            elif angle_input.isdigit():
                angle = int(angle_input)
                if 0 <= angle <= 180:
                    controller.send_servo_angle(angle)
                else:
                    print("Angle must be between 0 and 180.")
            else:
                print("Please enter a valid number or 'exit'.")
    except KeyboardInterrupt:
        print("\nProgram exited.")
    finally:
        controller.close()'''