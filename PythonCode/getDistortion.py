import cv2
import numpy as np
import glob

# Define the chessboard size and squares' size
chessboard_size = (7, 7)  # Adjust to your chessboard's number of inner corners (width-1, height-1)
square_size = 19.6/1000  # The actual size of the squares on your chessboard (in meters or any consistent unit)

# Prepare object points
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points from all images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Path to the folder containing your calibration images
images = glob.glob('/Users/hirshramani/PycharmProjects/foosyFriends/shotsWDan/*.jpg')

# Loop over each image to find chessboard corners
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        # Increase the accuracy of the corner locations
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1))
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

objpoints = [np.asarray(op, dtype=np.float32).reshape(-1, 1, 3) for op in objpoints]
imgpoints = [np.asarray(ip, dtype=np.float32).reshape(-1, 1, 2) for ip in imgpoints]

# Calibrate the camera
N_OK = len(objpoints)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

ret, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    K,
    D,
    rvecs,
    tvecs,
    cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW,
    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
)

print("Camera Matrix:\n", K)
print("Distortion Coefficients:\n", D)