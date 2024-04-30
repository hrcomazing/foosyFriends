import serial
import time

class ArduinoCOM:
    def __init__(self, port, baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate)
        time.sleep(2)  # Wait for the connection to establish
        print(f"Connected to Arduino on port {port} at {baud_rate} baud rate.")

    def send_positions(self, motorPos, servoPos):
        """Sends desired positions to the Arduino."""
        data = ','.join(map(str, motorPos + servoPos))
        self.ser.write((data + "\n").encode())  # Send the combined data followed by a newline
        print(f"Sent to Arduino: {data}")
        time.sleep(0.1)  # Give Arduino time to respond
        if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()  # Read the response
            print(f"Received from Arduino: {response}")

    def receive_positions(self):
        """Receives and updates current positions from the Arduino."""
        if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()
            print(f"Received current positions from Arduino: {response}")
            positions = list(map(int, response.split(',')))
            motorCurrent = positions[:len(positions)//2]  # Assuming first half are motor positions
            servoCurrent = positions[len(positions)//2:]  # Assuming second half are servo positions
            print("Motor positions: ", motorCurrent)
            print("Servo positions: ", servoCurrent)
            return motorCurrent, servoCurrent
        else:
            print("No data to receive.")
            return [.5, .5, .5, .5], [1, 1, 1, 1]

    def close(self):
        """Closes the serial connection."""
        self.ser.close()
        print("Serial connection closed.")