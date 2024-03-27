import cv2
import numpy as np
from AntiFisheye import AntiFisheye

# Create a VideoCapture object
cap = cv2.VideoCapture(1)
K = np.array([[1.30327767e+03, 0.00000000e+00, 7.04960207e+02], [0.00000000e+00, 1.30488170e+03, 5.03778850e+02], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Example camera matrix
D = np.array([-0.01093008, -0.23537576, 0.6907555, -0.48150618])  # Example distortion coefficients

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

# Set the resolution of the video capture. Example: 1920x1080
print('got here')
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
    cv2.imshow('Frame', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and close all windows
cap.release()
cv2.destroyAllWindows()