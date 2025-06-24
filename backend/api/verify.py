import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from fastapi import APIRouter, UploadFile, File
import numpy as np, cv2
from joblib import load
from utils.preprocess import preprocess_signature
from utils.extract_features import extract_features

router = APIRouter()
model = load("models/svm_model.pkl")

@router.post("/verify/")
async def verify_signature(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    processed = preprocess_signature(img)
    features = extract_features(processed).reshape(1, -1)
    prediction = model.predict(features)
    return {"result": "Genuine" if prediction[0] == 1 else "Forged"}
