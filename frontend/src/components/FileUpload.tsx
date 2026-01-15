import { useState } from "react";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    alert("File ingested");
    setLoading(false);
  };

  return (
    <div className="upload-box">
      <h2>Ingest Knowledge via File</h2>
      <p>Upload a .pdf, .docx or .txt file with the knowledge you want to add to the system.</p>
      <input
        type="file"
        accept=".pdf, .docx, .txt"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload} disabled={loading}>{loading ? "Uploading..." : "Upload"}</button>
    </div>
  );
}