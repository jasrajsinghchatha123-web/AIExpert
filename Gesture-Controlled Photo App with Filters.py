import cv2, time, numpy as np
import mediapipe as mp
H = mp.solutions.hands
TIP = H.HandLandmark
ids = {
    "thumb": TIP.THUMB_TIP,
    "index": TIP.INDEX_FINGER_TIP,
    "middle": TIP.MIDDLE_FINGER_TIP,
    "ring": TIP.RING_FINGER_TIP,
    "pinky": TIP.PINKY_TIP,
}
hands = H.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
draw = mp.solutions.drawing_utils
pairs = {
    "middle": ("SEPIA", "NEGATIVE"),
    "ring": ("BLUR", "GLITCH"),
    "pinky": ("EDGE", "CARTOON"),
}
st = {k: 0 for k in pairs}
cur = "SEPIA"
DEB, CAP, TT, TP = 0.6, 1.2, 30, 20
la = lc = 0
pinch_on = False
MAIN, POP = "Gesture-Controlled Photo App", "Captured (ESC / Close to resume)"
paused = False
freeze = None
SEPIA_M = np.array([
    [0.272, 0.534, 0.131],
    [0.349, 0.686, 0.168],
    [0.393, 0.769, 0.189]
])
def apply(img, t):
    if t == "SEPIA":
        return np.clip(cv2.transform(img, SEPIA_M), 0, 255).astype(np.uint8)
    if t == "NEGATIVE":
        return cv2.bitwise_not(img)
    if t == "BLUR":
        return cv2.GaussianBlur(img, (15, 15), 0)
    if t == "GLITCH":
        h, w = img.shape[:2]
        r, g, b = img[:, :, 2], img[:, :, 1], img[:, :, 0]
        return cv2.merge([np.roll(b, -int(0.02 * w), 1), g, np.roll(r, int(0.04 * w), 1)])
    if t == "EDGE":
        return cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 80, 160)
    if t == "CARTOON":
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        e = cv2.adaptiveThreshold(cv2.medianBlur(g, 7), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        c = cv2.bilateralFilter(img, 9, 75, 75)
        return cv2.bitwise_and(c, c, mask=e)
    return img
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()
cv2.namedWindow(MAIN, cv2.WINDOW_NORMAL)
while True:
    if paused:
        cv2.imshow(MAIN, freeze)
        k = cv2.waitKey(50) & 0xFF
        if k == ord("q"):
            break
        if k == 27:
            paused = False
            pinch_on = False
            try:
                cv2.destroyWindow(POP)
            except:
                pass
            continue
        try:
            if cv2.getWindowProperty(POP, cv2.WND_PROP_VISIBLE) <= 0:
                paused = False
                pinch_on = False
        except cv2.error:
            paused = False
            pinch_on = False
        continue
    ok, img = cap.read()
    if not ok:
        break
    img = cv2.flip(img, 1)
    h, w = img.shape[:2]
    res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time()
    capture = False
    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]
        draw.draw_landmarks(img, hand, H.HAND_CONNECTIONS)
        lm = {
            k: (
                int(hand.landmark[v].x * w),
                int(hand.landmark[v].y * h)
            )
            for k, v in ids.items()
        }
        dist_pinch = np.hypot(
            lm["thumb"][0] - lm["index"][0],
            lm["thumb"][1] - lm["index"][1]
        )
        if dist_pinch < TP:
            if not pinch_on and (now - lc > CAP):
                capture = True
                lc = now
                pinch_on = True
        else:
            pinch_on = False
        for finger, filter_pair in pairs.items():
            dist = np.hypot(
                lm["thumb"][0] - lm[finger][0],
                lm["thumb"][1] - lm[finger][1]
            )
            if dist < TT:
                if now - la > DEB:
                    st[finger] = (st[finger] + 1) % len(filter_pair)
                    cur = filter_pair[st[finger]]
                    la = now
    filtered_img = apply(img, cur)
    if len(filtered_img.shape) == 2:
        filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)
    cv2.putText(
        filtered_img, f"Filter: {cur}", (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )
    if capture:
        freeze = filtered_img.copy()
        paused = True
        cv2.imshow(POP, freeze)
        cv2.imwrite(f"captured_{int(now)}.png", freeze)
    cv2.imshow(MAIN, filtered_img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cap.release()
hands.close()
cv2.destroyAllWindows()