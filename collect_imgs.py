import cv2
import os
import time

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
GESTURES = ['up', 'down', 'left', 'right', 'bomb']

for gesture in GESTURES:
    os.makedirs(os.path.join(DATA_DIR, gesture), exist_ok=True)

gesture = input(f"Enter the gesture category from {GESTURES}: ").strip().lower()
if gesture not in GESTURES:
    print("Invalid gesture.")
    exit()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Failed to open camera.")
    exit()

time.sleep(2)

gesture_path = os.path.join(DATA_DIR, gesture)
existing = [f for f in os.listdir(gesture_path) if f.endswith('.jpg')]
start = len(existing)

for i in range(start, start + 500):
    ret, frame = cap.read()
    if not ret:
        continue
    img_path = os.path.join(gesture_path, f"{i}.jpg")
    cv2.imwrite(img_path, frame)
    cv2.imshow("Collecting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
