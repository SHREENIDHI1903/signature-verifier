import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from joblib import dump
from skimage.feature import hog

# Parameters
DATA_DIR = "dataset/signature_classifier"
IMG_SIZE = (128, 128)  # Smaller image for faster processing

def load_images(folder, label):
    X, y = [], []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, IMG_SIZE)
            features = hog(img, pixels_per_cell=(8, 8), cells_per_block=(2, 2), feature_vector=True)
            X.append(features)
            y.append(label)
    return X, y

# Load datasets
X, y = [], []

sig_path = os.path.join(DATA_DIR, "signature")
non_path = os.path.join(DATA_DIR, "nonsignature")

X_sig, y_sig = load_images(sig_path, 1)
X_non, y_non = load_images(non_path, 0)

X.extend(X_sig)
X.extend(X_non)
y.extend(y_sig)
y.extend(y_non)

print(f"✅ Loaded {len(X)} samples")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = SVC(kernel="linear", probability=True)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"🎯 Accuracy: {acc:.2f}")

# Save
os.makedirs("models", exist_ok=True)
dump(clf, "models/sig_detector_sklearn.pkl")
print("✅ Saved as models/sig_detector_sklearn.pkl")
