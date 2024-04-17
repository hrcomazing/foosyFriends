import cv2
import numpy as np


def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture device.")
        return

    # Check for CUDA capability
    if cv2.cuda.getCudaEnabledDeviceCount() == 0:
        print("No CUDA-capable device is detected")
        return

    # Define the range for orange color in HSV
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([15, 255, 255])

    # Create windows to display the videos
    cv2.namedWindow("Original Video", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Orange Ball Tracking", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture video frame")
            break

        # Upload frame to GPU
        gpu_frame = cv2.cuda_GpuMat()
        gpu_frame.upload(frame)

        # Convert the frame to HSV color space using GPU
        gpu_hsv = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2HSV)

        # Apply the orange color range mask
        gpu_mask = cv2.cuda.inRange(gpu_hsv, lower_orange, upper_orange)

        # Download mask back to CPU
        mask = gpu_mask.download()

        # Perform morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw circles around detected orange ball
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Filter out small contours to find the ball
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                if radius > 10:  # Check if the radius size is reasonable to be the ball
                    cv2.circle(frame, center, radius, (0, 255, 0), 3)

        # Display the original and the processed frames
        cv2.imshow("Original Video", frame)
        cv2.imshow("Orange Ball Tracking", mask)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()