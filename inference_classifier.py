import cv2
import pickle
import mediapipe as mp
from collections import deque
import os
from pynput.keyboard import Controller, Key

keyboard = Controller()

model_path = os.path.join(os.path.dirname(__file__), "model.p")
model_dict = pickle.load(open(model_path, "rb"))

model = model_dict["model"]
label_map = model_dict["labels"]
inv_labels = {v: k for k, v in label_map.items()}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)
history = deque(maxlen=5)
last_key = None

gesture_to_key = {
    "up": "w",
    "down": "s",
    "left": "a",
    "right": "d",
    "bomb": Key.space
}

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    data_aux = []
    x_, y_ = [], []

    detected = False
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                x_.append(lm.x)
                y_.append(lm.y)
            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

        if data_aux:
            prediction = model.predict([data_aux])[0]
            label = prediction
            history.append(label)
            most_common = max(set(history), key=history.count)

            if most_common in gesture_to_key:
                key = gesture_to_key[most_common]
                if key != last_key:
                    if last_key:
                        keyboard.release(last_key)
                    keyboard.press(key)
                    last_key = key
                detected = True

            cv2.putText(frame, f"Prediction: {most_common}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if not detected and last_key:
        keyboard.release(last_key)
        last_key = None
        cv2.putText(frame, "No hand detected", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Sign Language Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if last_key:
    keyboard.release(last_key)
cap.release()
cv2.destroyAllWindows()
