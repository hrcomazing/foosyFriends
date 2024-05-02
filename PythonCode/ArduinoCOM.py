import serial
import time

class ArduinoCOM:
    def __init__(self, port, baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate)
        time.sleep(2)  # Wait for the connection to establish
        print(f"Connected to Arduino on port {port} at {baud_rate} baud rate.")
        self.motorCurrent = [1, 1, 1, 1]
        self.servoCurrent = [0, 0, 0, 0]

    def send_positions(self, motorPos, servoPos):
        """Sends desired positions to the Arduino."""
        data = ','.join(map(str, motorPos + servoPos))
        self.ser.write((data + "\n").encode())  # Send the combined data followed by a newline
        print(f"Sent to Arduino: {data}")
        #time.sleep(0.001)  # Give Arduino time to respond
        '''if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()  # Read the response
            print(f"Received from Arduino: {response}")'''

    def receive_positions(self):
        """Receives and updates current positions from the Arduino."""
        if self.ser.inWaiting() > 0:
            response = self.ser.readline().decode().rstrip()
            print(f"Received current positions from Arduino: {response}")
            positions = list(map(float, response.split(',')))
            #print(positions)
            self.motorCurrent = positions[:len(positions)//2]  # Assuming first half are motor positions
            self.servoCurrent = positions[len(positions)//2:]  # Assuming second half are servo positions
            print("Motor positions: ", self.motorCurrent)
            print("Servo positions: ", self.servoCurrent)
            return self.motorCurrent, self.servoCurrent
        else:
            print("No data to receive.")
            return self.motorCurrent, self.servoCurrent

    def close(self):
        """Closes the serial connection."""
        self.ser.close()
        print("Serial connection closed.")