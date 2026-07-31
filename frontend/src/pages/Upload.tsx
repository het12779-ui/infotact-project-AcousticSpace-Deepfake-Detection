import { useState } from "react";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/v1/predict", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        throw new Error(`Upload failed with status ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Audio Deepfake Analysis</h1>
      <div className="border-2 border-dashed border-gray-700 p-6 rounded-lg mb-4 text-center">
        <input
          type="file"
          accept=".wav,.mp3,.flac,.ogg,.m4a"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="mb-4"
        />
        <br />
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-semibold disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze Audio"}
        </button>
      </div>

      {error && (
        <div className="bg-red-900/40 border border-red-500 text-red-200 p-4 rounded mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-gray-800 p-4 rounded border border-gray-700">
          <h2 className="text-xl font-semibold mb-2">Analysis Result</h2>
          <p>
            <strong>File:</strong> {result.filename}
          </p>
          <p>
            <strong>Prediction:</strong>{" "}
            <span className={result.is_fake ? "text-red-400" : "text-green-400"}>
              {result.is_fake ? "Fake" : "Real"}
            </span>
          </p>
          <p>
            <strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%
          </p>
        </div>
      )}
    </div>
  );
}
