import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
from joblib import load
from utils.preprocess import preprocess_signature
from utils.extract_features import extract_features

router = APIRouter()

# Load SVM model
try:
    model = load("models/svm_model.pkl")
    print("✅ SVM model loaded")
except Exception as e:
    print("❌ Failed to load SVM model:", e)
    model = None

# Load scikit-learn signature detector
try:
    detector = load("models/sig_detector_sklearn.pkl")
    print("✅ Signature detector loaded (scikit-learn)")
except Exception as e:
    print("❌ Failed to load detector:", e)
    detector = None

@router.post("/verify/")
async def verify_signature(file: UploadFile = File(...)):
    try:
        # Read image from upload
        contents = await file.read()
        print("📥 Image uploaded and read")

        # Decode as image array
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            print("⚠️ Could not decode image")
            return {"result": "Invalid image format"}

        print("🖼️ Decoded image shape:", img.shape)

          # Signature detector check
        if detector:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (128, 128))
            from skimage.feature import hog
            features = hog(gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), feature_vector=True)
            pred_prob = detector.predict_proba([features])[0][1]
            print(f"🧠 Signature detector confidence: {pred_prob:.2f}")

            if pred_prob < 0.1:
                return {"result": "Rejected: Not a signature"}


        # Preprocess and extract features
        processed = preprocess_signature(img)
        print("⚙️ Preprocessed image shape:", processed.shape if processed is not None else "None")

        features = extract_features(processed)

        if features is None:
            print("⚠️ Feature extraction failed — result is None")
            return {"result": "Invalid signature input"}

        print("🔢 Feature vector shape:", features.shape)

        features = features.reshape(1, -1)

        if model is None:
            return {"result": "Model not available"}

        prediction = model.predict(features)
        print("🔍 Prediction result:", prediction)

        return {"result": "Genuine" if prediction[0] == 1 else "Forged"}

    except Exception as e:
        print("❌ Verification error:", e)
        return {"result": "Verification failed"}
