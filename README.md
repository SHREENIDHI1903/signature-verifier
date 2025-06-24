# ✍️ Signature Verification Web App

An AI-powered full-stack application for verifying handwritten signatures using a trained machine learning model.

## 🚀 Live Demo
👉 [View Demo](https://your-vercel-url.vercel.app)

## 🧠 What It Does
This web app allows users to upload a handwritten signature image and instantly checks whether the signature is genuine or forged — powered by SVM and feature extraction techniques.

## 🔧 Technologies Used

### Backend
- **FastAPI** – High-performance API framework
- **scikit-learn** – Trained SVM classifier
- **OpenCV** – Image pre-processing
- **Uvicorn** – ASGI server

### Frontend
- **React** – Dynamic, responsive interface
- **Axios** – API communication
- **react-dropzone** – Drag-and-drop file upload
- **react-toastify** – Toast notifications
- **Responsive Dashboard** with Light/Dark mode toggle

## ⚙️ Features
- Upload signature using drag-and-drop or file input
- Live image preview before submission
- Backend verification with live result
- Loading spinner, toast alerts, and theme toggle
- Verification history log (session-based)
- Full dashboard layout

## 🛠️ Running Locally

### 1. Clone the repository

		git clone https://github.com/your-username/signature-verifier.git
		cd signature-verifier

#### 2. Backend (FastAPI)
		cd backend
		pip install -r requirements.txt
		uvicorn main:app --reload

#### 3. Frontend (React)
		cd ../frontend
		npm install
		npm start
Open your browser at http://localhost:3000.

📷 Screenshots

📄 License
MIT License — feel free to use, fork, and build!




