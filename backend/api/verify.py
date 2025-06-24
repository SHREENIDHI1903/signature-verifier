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

# Load the trained SVM model
try:
    model = load("models/svm_model.pkl")
except Exception as e:
    print("Model loading failed:", e)
    model = None  # Fallback if model isn't loaded

@router.post("/verify/")
async def verify_signature(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Decode the uploaded image
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return {"result": "Invalid or corrupted image"}

        # Preprocess and extract features
        processed = preprocess_signature(img)
        features = extract_features(processed).reshape(1, -1)

        # Predict using the loaded model
        if model is None:
            return {"result": "Model not available"}
        
        prediction = model.predict(features)
        return {"result": "Genuine" if prediction[0] == 1 else "Forged"}

    except Exception as e:
        print("Verification error:", e)
        return {"result": "Verification failed"}
