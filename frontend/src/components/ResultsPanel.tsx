interface ResultsPanelProps {
  result: any;
}

export default function ResultsPanel({ result }: ResultsPanelProps) {
  if (!result) return null;

  return (
    <div className="bg-gray-800 p-4 rounded border border-gray-700">
      <h2 className="text-xl font-semibold mb-2">Analysis Result</h2>
      <p className="text-sm mb-1">
        <strong>File:</strong> {result.filename || "Uploaded File"}
      </p>
      <p className="text-sm mb-1">
        <strong>Prediction:</strong>{" "}
        <span className={result.is_fake ? "text-red-400 font-bold" : "text-green-400 font-bold"}>
          {result.is_fake ? "Fake (Synthetic)" : "Real (Authentic)"}
        </span>
      </p>
      {result.confidence !== undefined && (
        <p className="text-sm">
          <strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%
        </p>
      )}
    </div>
  );
}
