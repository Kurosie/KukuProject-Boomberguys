import os
import pickle
import cv2
import mediapipe as mp

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

data, labels = [], []

for label in os.listdir(DATA_DIR):
    folder_path = os.path.join(DATA_DIR, label)
    if not os.path.isdir(folder_path):
        continue

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".jpg"):
            continue

        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue

        results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.multi_hand_landmarks:
            continue

        landmarks = results.multi_hand_landmarks[0]
        x_list = [lm.x for lm in landmarks.landmark]
        y_list = [lm.y for lm in landmarks.landmark]

        flat_data = []
        for lm in landmarks.landmark:
            flat_data.append(lm.x - min(x_list))
            flat_data.append(lm.y - min(y_list))

        data.append(flat_data)
        labels.append(label)

output_path = os.path.join(BASE_DIR, "data.pickle")
with open(output_path, "wb") as f:
    pickle.dump({"data": data, "labels": labels}, f)
