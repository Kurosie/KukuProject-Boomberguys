import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "data.pickle")
model_path = os.path.join(base_dir, "model.p")

with open(data_path, "rb") as f:
    data_dict = pickle.load(f)

data = data_dict["data"]
labels = data_dict["labels"]

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_predict = model.predict(X_test)
print("Accuracy:", accuracy_score(y_predict, y_test))

with open(model_path, "wb") as f:
    pickle.dump({"model": model, "labels": {label: idx for idx, label in enumerate(set(labels))}}, f)
