import ArduinoCOM

if __name__ == "__main__":
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
        controller.close()