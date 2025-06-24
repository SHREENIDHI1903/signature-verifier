import os
import cv2
from sklearn import svm
from joblib import dump
from utils.preprocess import preprocess_signature
from utils.extract_features import extract_features

X, y = [], []

for label in ['genuine', 'forged']:
    folder_path = f'dataset/{label}'
    for file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        if img is None:
            continue
        processed = preprocess_signature(img)
        features = extract_features(processed)
        X.append(features)
        y.append(1 if label == 'genuine' else 0)

model = svm.SVC(kernel='linear', probability=True)
model.fit(X, y)
dump(model, 'models/svm_model.pkl')
print("Model trained and saved.")
