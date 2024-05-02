import cv2
import numpy as np
import imutils
import math
from AntiFisheye import AntiFisheye

K = np.array([[968.82202387, 0.00000000e+00, 628.92706997], [0.00000000e+00, 970.56156502, 385.82007021], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Example camera matrix
D = np.array([-0.04508764, -0.01990902, 0.08263842, -0.0700435])
radius = 10

def track_colored_object():
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open video capture device.")
        exit()

    # Set the resolution of the video capture. Example: 1920x1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Create Background Subtractor object
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    x, y = 0, 0

    # Define range of orange color in HSV
    lower_orange = np.array([0, 100, 100])
    upper_orange = np.array([100, 255, 255])

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = imutils.resize(frame, width=1200)
        # Apply the background subtractor to get the foreground mask
        frame = AntiFisheye.undistort_fisheye_image(frame, K, D)
        frame = frame[120:590, 160:1000]
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
                print(f"Updated position: ({x}, {y})")
            else:
                print(f"Current position: ({x}, {y})")
        else:
            print(f"Current position: ({x}, {y})")

        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)


        # Display the resulting frame
        cv2.imshow('Frame', frame)
        cv2.imshow('Foreground', fgmask)
        cv2.imshow('Color Filter', combined_mask)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_colored_object()