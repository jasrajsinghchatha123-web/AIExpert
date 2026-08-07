import cv2
import numpy as np
def apply_filter(frame , mode):
    if mode == 0:
        return frame
    elif mode == 1:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif mode == 2:
        kernel = np.array([
            [0.272 , 0.534 , 0.131],
            [0.349 , 0.686 , 0.168],
            [0.393 , 0.769 , 0.189]
        ])
        sepia = cv2.transform(frame, kernel)
        return cv2.convertScaleAbs(sepia)
    elif mode == 3:
        return cv2.bitwise_not(frame)
    elif mode == 4:
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif mode == 5:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)
    elif mode == 6:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
        return cv2.convertScaleAbs(sobelx + sobely)
    elif mode == 7:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        return cv2.convertScaleAbs(lap)
    return frame
cap = cv2.VideoCapture(0)
mode = 0
print("Keys:")
print("0: Original")
print("1: Grayscale")
print("2: Sepia")
print("3: Negative")
print("4: Gaussian Blur")
print("5: Canny Edge Detection")
print("6: Sobel Edge Detection")
print("7: Laplacian Edge Detection")
print("Q - Quit")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    output_frame = apply_filter(frame, mode)
    cv2.imshow('Real-Time Color Filters and Edge Detection', output_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('0'):
        mode = 0
    elif key == ord('1'):
        mode = 1
    elif key == ord('2'):
        mode = 2
    elif key == ord('3'):
        mode = 3
    elif key == ord('4'):
        mode = 4
    elif key == ord('5'):
        mode = 5
    elif key == ord('6'):
        mode = 6
    elif key == ord('7'):
        mode = 7
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()