import cv2
import numpy as np
import imutils
from math import sqrt
import time
import serial
import json
from AntiFisheye import AntiFisheye
from ArduinoCOM import ArduinoCOM

# Camera and distortion parameters
K = np.array([[968.82202387, 0.00000000e+00, 628.92706997], [0.00000000e+00, 970.56156502, 385.82007021], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Example camera matrix
D = np.array([-0.04508764, -0.01990902, 0.08263842, -0.0700435])

# Initialization of tracking and time measurement
x_coords, y_coords = [], []
timestamps = []

# Dimensions of the table in inches
width_inches = 23.09
length_inches = 46.75
# Stepper motor response time (dummy values, in seconds)
v_stepper = 10


# Pixel coordinates of the table corners
ULCorner = (197, 135) # Upper Left (194,134)
URCorner = (1064, 135) # Upper Right (1061, 136)
BLCorner = (197, 617)  # Bottom Left (200, 626)
BRCorner = (1064, 617) # Bottom Right (1066, 609)

# helper methods
# Convert player area positions from inches to pixels
def convert_to_pixels(player_areas, ppi):
    return [(start * ppi + URCorner[1], end * ppi + URCorner[1]) for start, end in player_areas]


# Convert rod x-asymptotes from inches to pixels
def convert_rod_asymptotes(rod_asymptotes, ppi):
    return [x * ppi + ULCorner[0] for x in rod_asymptotes]


def normalize_y_position(y, top_pixel = URCorner[1], bottom_pixel = BRCorner[1]):

    if y < top_pixel:
        return 0
    elif y > bottom_pixel:
        return 1
    else:
        return (y - top_pixel) / (bottom_pixel - top_pixel)


# Function to predict the final position of the ball based on current and previous positions
def predict_final_position(x1, y1, x2, y2, time_diff):
    vx = (x2 - x1) / time_diff if time_diff > 0 else 0
    vy = (y2 - y1) / time_diff if time_diff > 0 else 0
    x_final = np.array(rod_x_asymptote_pixels)

    if vx != 0:
        y_final = y2 + vy * (x_final - x2) / vx
    else:
        # Create an array of y2 repeated for the length of x_final
        y_final = np.full_like(x_final, y2)

    return x_final, y_final, vx, vy


# Calculate pixel-per-inch ratio
width_pixels = URCorner[0] - ULCorner[0]  # stupid axis
length_pixels = BRCorner[1] - URCorner[1]  # axis players move on
ppi_width = width_pixels / width_inches
ppi_length = length_pixels / length_inches

# Define player areas per rod in inches
player_areas_per_rod_inches = [
    [(0, 7.4033), (7.4033, 14.8066), (14.8066, 22.2099)],
    [(0, 3.6445), (4.7865, 8.3435), (9.318, 12.9655), (13.9455, 17.969), (19.014, 23.09)],
    [(0, 12.551), (9.63, 22.195)],
    [(0, 8.3), (7.179, 15.479), (14.3, 22.575)]
]

# Rod x-asymptotes in inches
rod_x_asymptote_inches = [32.125, 20.5, 8.875, 3]

# Convert to pixels
player_areas_per_rod_pixels = [convert_to_pixels(areas, ppi_length) for areas in player_areas_per_rod_inches]
rod_x_asymptote_pixels = convert_rod_asymptotes(rod_x_asymptote_inches, ppi_width)

print("Player Areas per Rod in Pixels:", player_areas_per_rod_pixels)
print("Rod X-Asymptotes in Pixels:", rod_x_asymptote_pixels)

# Setup camera
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

# get everything ready for vision processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

# current position of the ball (x2, y2 used for prediciton and x,y used for vision)
x2, y2 = 0, 0
x, y = 0, 0

# to mark location of ball in camera frame
radius = 10

# Define range of orange color in HSV
lower_orange = np.array([0, 100, 100])
upper_orange = np.array([100, 255, 255])

# init communications change port as necessary
arduino = ArduinoCOM(port= '/dev/cu.usbmodem144301')  # Replace 'COM3' with your actual COM port

# init dummy values for coms arrays
motorCurrent = [0.5, 0.5, 0.5, 0.5]
motorDesired = [0.5, 0.5, 0.5, 0.5]
servoCurrent = [20, 20, 20, 69]
servoDesired = [0.5, 0.5, 0.5, 0.5]


# Main loop
while True:
    # video processing
    ret, frame = cap.read()
    current_time = time.time()
    if not ret:
        print("Failed to grab frame")
        break
    frame = imutils.resize(frame, width=1200)
    frame = AntiFisheye.undistort_fisheye_image(frame, K, D)
    fgmask = fgbg.apply(frame)
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # Bitwise-AND mask and foreground mask to isolate the orange colored moving object
    combined_mask = cv2.bitwise_and(mask, fgmask)
    # Find contours in the combined mask
    contours = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 100:  # Update this threshold as needed
            ((x, y), _) = cv2.minEnclosingCircle(c)
    
    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    cv2.imshow('Frame', frame)
    
    # set the values of x,y from vision to x2, y2 for prediction
    x2, y2 = x, y  # Random values for testing
    x_coords.append(x2)
    y_coords.append(y2)
    timestamps.append(current_time)

    # defence logic
    if len(x_coords) > 1:
        # Calculate velocity and predict final position
        time_diff = timestamps[-1] - timestamps[-2]
        x_final, y_final, vx, vy = predict_final_position(x_coords[-2], y_coords[-2], x_coords[-1], y_coords[-1], time_diff)

        for rod_index, x_rod in enumerate(rod_x_asymptote_pixels):
            time_to_intercept = np.abs((x_rod - x2) / vx) if vx != 0 else float('inf')
            for player_index, (start, end) in enumerate(player_areas_per_rod_pixels[rod_index]):
                if start <= y_final[rod_index] <= end:
                    motor_travel_time = np.abs((normalize_y_position(y_final[rod_index]) - motorCurrent[rod_index]) / v_stepper)
                    if motor_travel_time <= time_to_intercept:
                        stepper_position = (y_final[rod_index] - start) / (end - start)
                        print(f"Rod {rod_index+1} Player {player_index+1}: Move motor to position {stepper_position:.2f} to intercept")
                        motorDesired[rod_index] = stepper_position  # update desired motor position array
                    else:
                        print(f"Rod {rod_index+1}: Cannot intercept in time, requires {motor_travel_time:.2f}s, available {time_to_intercept:.2f}s")
    
    # send and receive coordinates via serial
    try:
        # Sending desired positions to the Arduino
        arduino.send_positions(motorDesired, servoDesired)

        # Receiving and printing current positions from the Arduino
        motorCurrent, servoCurrent = arduino.receive_positions()

    except Exception as e:
        print("An error occurred:", e)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


