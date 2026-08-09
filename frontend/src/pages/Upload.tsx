import { useState } from "react";
import AudioUpload from "../components/AudioUpload";
import WaveformPlayer from "../components/WaveformPlayer";
import ResultsPanel from "../components/ResultsPanel";
import { useWebSocketPredict } from "../hooks/useWebSocketPredict";

export default function Upload() {
  const [result, setResult] = useState<any>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [useLive, setUseLive] = useState(false);
  const { stage, result: wsResult, error: wsError, analyze } = useWebSocketPredict();

  const handleUpload = (file: File) => {
    setSelectedFile(file);
    if (useLive) analyze(file);
  };
  const displayedResult = useLive ? wsResult : result;

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
<h1 className="text-2xl font-bold mb-4">Upload Audio for Analysis</h1>
<label className="flex items-center gap-2 text-sm mb-3">
<input type="checkbox" checked={useLive} onChange={(e) => setUseLive(e.target.checked)} />
Use live progress (WebSocket)
</label>
<AudioUpload onResult={setResult} onFileSelected={handleFileSelected} />
{useLive && stage && <p className="text-sm text-blue-400 mt-2">Stage: {stage}</p>}
{useLive && wsError && <p className="text-red-400 text-sm mt-2">{wsError}</p>}
<WaveformPlayer file={selectedFile} flaggedSegments={displayedResult?.flagged_segments || []} />
<ResultsPanel result={displayedResult} />
</div>
        <br />
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-semibold disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze Audio"}
        </button>
      </div >

  { error && (
    <div className="bg-red-900/40 border border-red-500 text-red-200 p-4 rounded mb-4">
      {error}
    </div>
  )}

{
  result && (
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
  )
}
    </div >
  );
}
