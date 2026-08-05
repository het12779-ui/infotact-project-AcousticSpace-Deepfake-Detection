interface ResultsPanelProps {
  result: any;
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const percentage = Math.round(value * 100);
  return (
    <div className="my-2">
      <div className="flex justify-between text-sm font-medium mb-1">
        <span>{label}</span>
        <span>{percentage}%</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2.5">
        <div
          className="bg-blue-500 h-2.5 rounded-full transition-all duration-300"
          style={{ width: `${Math.min(100, Math.max(0, percentage))}%` }}
        />
      </div>
    </div>
  );
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
        <p className="text-sm mb-1">
          <strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%
        </p>
      )}

      {result.rir_mismatch_score !== undefined && result.rir_mismatch_score !== null && (
        <ScoreBar label="RIR mismatch score" value={result.rir_mismatch_score} />
      )}
      {result.breathing_score !== undefined && result.breathing_score !== null && (
        <ScoreBar label="Breathing pattern score" value={result.breathing_score} />
      )}
      <p className="text-xs text-gray-500 mt-1 mb-2">
        Higher means the voice's room echo looks more artificial.
      </p>
    </div>
  );
}
