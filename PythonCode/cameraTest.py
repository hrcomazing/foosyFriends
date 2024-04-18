import cv2
import numpy as np
import imutils
from AntiFisheye import AntiFisheye
import math

# Create a VideoCapture object
cap = cv2.VideoCapture(1)
K = np.array([[1.30327767e+03, 0.00000000e+00, 7.04960207e+02], [0.00000000e+00, 1.30488170e+03, 5.03778850e+02], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Example camera matrix
D = np.array([-0.01093008, -0.23537576, 0.6907555, -0.48150618])  # Example distortion coefficients
orangeLower = (55, 170, 180)
orangeUpper = (160, 240, 255)
# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

# Set the resolution of the video capture. Example: 1920x1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Capture and display video frames in a loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    # Display the resulting frame

    frame = AntiFisheye.undistort_fisheye_image(frame, K, D)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    mask = cv2.inRange(blurred, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("masked", mask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        # Calculate the circularity
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
       
        circularity = 4 * math.pi * area / (perimeter ** 2)

        # Check if the circularity is within your desired range, for example, > 0.8
        if circularity > 0.3 and radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            print(x, ",", y)
            
    cv2.imshow('Frame', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and close all windows
cap.release()
cv2.destroyAllWindows()