import cv2
import numpy as np
import glob

# Define the chessboard size and squares' size
chessboard_size = (7, 9)  # Number of inner corners per a chessboard row and column
square_size = 25  # Define the size of chessboard squares in mm or inches

# Prepare object points based on the chessboard size and squares' size
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points from all images
objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

# List of calibration images
images = glob.glob('path/to/calibration/images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # If found, add object points, image points
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

# Calibrate the camera
ret, K, D, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera Matrix:\n", K)
print("Distortion Coefficients:\n", D)