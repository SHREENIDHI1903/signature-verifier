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

# Load your trained model
try:
    model = load("models/svm_model.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", e)
    model = None

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
