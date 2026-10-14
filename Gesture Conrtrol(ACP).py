import cv2
import mediapipe as mp
import pyautogui
import math
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
cap = cv2.VideoCapture(0)
print("Gesture Scroll System Started")
print("Open Palm: Scroll Up")
print("Closed Fist: Scroll Down")
print("Press Q to quit")
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Unable to access webcam.")
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    gesture = "No Hand Detected"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            landmarks = hand_landmarks.landmark
            finger_tips = [8, 12, 16, 20]
            finger_pips = [6, 10, 14, 18]
            fingers_up = 0
            for tip, pip in zip(finger_tips, finger_pips):
                if landmarks[tip].y < landmarks[pip].y:
                    fingers_up += 1
            thumb_tip = landmarks[4]
            index_mcp = landmarks[5]
            thumb_ip = landmarks[3]
            wrist = landmarks[0]
            thumb_distance = math.sqrt(
                (thumb_tip.x - index_mcp.x) ** 2
                + (thumb_tip.y - index_mcp.y) ** 2
            )
            if fingers_up >= 4:
                gesture = "Open Palm - Scrolling Up"
                pyautogui.scroll(3)
            elif fingers_up == 0:
                gesture = "Closed Fist - Scrolling Down"
                pyautogui.scroll(-3)
            else:
                gesture = "Neutral - No Scrolling"
    cv2.putText(
        frame,
        gesture,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )
    cv2.imshow("Gesture Controlled Scrolling", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
hands.close()
cv2.destroyAllWindows()