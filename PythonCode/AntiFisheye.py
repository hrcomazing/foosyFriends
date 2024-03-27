import cv2
import numpy as np


class AntiFisheye:

    def undistort_fisheye_image(img, K, D, dim2=None, dim3=None):

        dim1 = img.shape[:2][::-1]  # Dimension of the original image

        if dim2 is None:
            dim2 = dim1
        if dim3 is None:
            dim3 = dim1

        # Convert K and D to float64
        K = K.astype(np.float64)
        D = D.astype(np.float64)

        scaled_K = K.copy()
        scaled_K[0, 0] *= dim1[0] / dim3[0]
        scaled_K[1, 1] *= dim1[1] / dim3[1]
        scaled_K[0, 2] *= dim1[0] / dim3[0]
        scaled_K[1, 2] *= dim1[1] / dim3[1]

        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), scaled_K, dim1, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        return undistorted_img


'''
# Example usage
K = np.array([[1.30327767e+03, 0.00000000e+00, 7.04960207e+02], [0.00000000e+00, 1.30488170e+03, 5.03778850e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Example camera matrix
D = np.array([-0.01093008, -0.23537576, 0.6907555, -0.48150618])  # Example distortion coefficients

K = K.astype(np.float64)
D = D.astype(np.float64)

image_path = "/Users/hirshramani/PycharmProjects/foosyFriends/shotsWDan/Photo on 3-20-24 at 4.13 PM.jpg"  # Change to the path of your image
frame = cv2.imread(image_path)
# Correct the image
undistorted_img = AntiFisheye.undistort_fisheye_image(frame, K, D)

# Save or display the undistorted image
cv2.imshow("Undistorted Image", undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''