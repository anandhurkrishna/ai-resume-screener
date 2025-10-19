import React, { useState } from "react";
import axios from "axios";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("⚠ Please select a file first");
      return;
    }
    setError("");
    setResponse(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/upload_resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (err) {
      setError("❌ Error uploading resume: " + err.message);
    }
  };

  return (
    <div style={{ fontFamily: "Poppins, sans-serif", background: "#f4f6f9", minHeight: "100vh", padding: "40px" }}>
      <div
        style={{
          maxWidth: "600px",
          margin: "auto",
          background: "#fff",
          borderRadius: "10px",
          padding: "30px",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          textAlign: "center",
        }}
      >
        <h1 style={{ color: "#333" }}>🧠 AI Resume Screener</h1>
        <p style={{ color: "#666", fontSize: "14px" }}>Upload your resume to analyze details automatically.</p>

        <div style={{ marginTop: "20px" }}>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            style={{
              marginRight: "10px",
              border: "1px solid #ccc",
              padding: "6px",
              borderRadius: "5px",
            }}
          />
          <button
            onClick={handleUpload}
            style={{
              padding: "8px 16px",
              borderRadius: "6px",
              backgroundColor: "#4CAF50",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Upload Resume
          </button>
        </div>

        {error && <p style={{ color: "red", marginTop: "15px" }}>{error}</p>}

        {response && (
          <div
            style={{
              marginTop: "30px",
              textAlign: "left",
              background: "#f9f9f9",
              padding: "20px",
              borderRadius: "8px",
              border: "1px solid #eee",
            }}
          >
            <h3>✅ Extracted Resume Details</h3>
            <p><b>File:</b> {response.filename}</p>
            <p><b>Candidate Name:</b> {response.info.name || "N/A"}</p>
            <p><b>Email:</b> {response.info.email || "N/A"}</p>
            <p><b>Phone:</b> {response.info.phone || "N/A"}</p>
            <p><b>Skills:</b> {response.info.skills.length > 0 ? response.info.skills.join(", ") : "No skills detected"}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadResume;