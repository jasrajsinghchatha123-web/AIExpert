import cv2
import numpy as np
def apply_filter(frame, choice):
    if choice == 0:
        return frame
    elif choice == 1:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif choice == 2:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        return hsv
    elif choice == 3:
        return cv2.bitwise_not(frame)
    elif choice == 4:
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif choice == 5:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)
    elif choice == 6:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.convertScaleAbs(sobelx) + cv2.convertScaleAbs(sobely)
        return sobel
    elif choice == 7:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return cv2.convertScaleAbs(laplacian)
    elif choice == 8:
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)
    return frame
cap = cv2.VideoCapture(0)
choice = 0
print("\n===== Real-Time Image Processing =====")
print("0 - Original")
print("1 - Grayscale")
print("2 - HSV")
print("3 - Negative")
print("4 - Blur")
print("5 - Canny Edge")
print("6 - Sobel Edge")
print("7 - Laplacian Edge")
print("8 - Sepia")
print("Q - Quit\n")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    result = apply_filter(frame, choice)
    cv2.imshow("Real-Time Filters", result)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('0'):
        choice = 0
    elif key == ord('1'):
        choice = 1
    elif key == ord('2'):
        choice = 2
    elif key == ord('3'):
        choice = 3
    elif key == ord('4'):
        choice = 4
    elif key == ord('5'):
        choice = 5
    elif key == ord('6'):
        choice = 6
    elif key == ord('7'):
        choice = 7
    elif key == ord('8'):
        choice = 8
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()