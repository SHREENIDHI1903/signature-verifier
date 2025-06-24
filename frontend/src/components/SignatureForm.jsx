import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './SignatureForm.css';

export default function SignatureForm() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const onDrop = useCallback((acceptedFiles) => {
    const selectedFile = acceptedFiles[0];
    setFile(selectedFile);
    if (selectedFile) {
      const objectUrl = URL.createObjectURL(selectedFile);
      setPreviewUrl(objectUrl);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!file) {
    toast.error("Please select a file before submitting.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  setIsLoading(true);
  try {
    const response = await axios.post(
      "https://signature-api-n9zv.onrender.com/api/verify/",
      formData
    );

    const result = response.data.result;
    console.log("🧠 API result:", result);

    if (result === "Genuine" || result === "Forged") {
      toast.success(`✅ Verified as ${result}!`);
    } else {
      toast.error(`❌ Unexpected result: ${result}`);
    }

    const timestamp = new Date().toLocaleTimeString();
    setHistory((prev) => [
      { name: file.name, result, time: timestamp },
      ...prev,
    ]);
  } catch (error) {
    console.error("Verification error:", error.response?.data || error.message);
    toast.error("❌ Verification failed. Please try again.");
  }

  setIsLoading(false);
};

return (
  <div className="dashboard-container">
    <div className="sidebar">
      <h1>SIGNA_SCAN</h1>
      <p>Verify handwritten signatures instantly</p>
    </div>

    <div className="main-panel">
      <div className="upload-section">
        <h2>Upload a Signature</h2>
        <div {...getRootProps({ className: 'drop-zone' })}>
          <input {...getInputProps()} />
          <p>{isDragActive ? 'Drop it here...' : 'Drag & drop or click to select'}</p>
        </div>

        {previewUrl && (
          <div className="preview-box">
            <img src={previewUrl} alt="Preview" />
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <button type="submit" disabled={!file || isLoading}>
            {isLoading ? 'Verifying...' : 'Verify'}
          </button>
        </form>

        {isLoading && <div className="spinner"></div>}
      </div>

      {/* ABOUT THIS PROJECT SECTION */}
      <div className="about-section" style={{
        marginTop: "2rem",
        padding: "1rem",
        backgroundColor: "#f5f5f5",
        borderRadius: "8px",
        fontSize: "0.95rem"
      }}>
        <h3>🧠 How Signature Verification Works</h3>
        <ul style={{ paddingLeft: "1.2rem" }}>
        <p>This system verifies handwritten signatures using machine learning. Here's how it works:</p>
        <ul style={{ paddingLeft: "1.2rem" }}>
          <li><strong>Step 1:</strong> A <em>Signature Detector</em> (SVM + HOG features) filters out non-signature inputs like selfies or photos.</li>
          <li><strong>Step 2:</strong> If valid, the <em>Verification Model</em> (SVM) checks if the signature is <strong>Genuine</strong> or <strong>Forged</strong>.</li>
          
        </ul>
        <p>The detector uses <em>HOG</em> to extract edge features, feeding them into an <em>SVM</em> trained on positive and negative examples.</p>
      </div>



      {history.length > 0 && (
        <div className="history-log">
          <h3>Verification History</h3>
          <ul>
            {history.map((entry, index) => (
              <li key={index}>
                <strong>{entry.name}</strong> → {entry.result} <em>({entry.time})</em>
              </li>
            ))}
          </ul>
        </div>
      )}
      <ToastContainer />
    </div>
  </div>
);

}
