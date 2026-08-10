interface AcousticComparison {
  voice_rt60?: number | null;
  voice_drr?: number | null;
  bg_rt60?: number | null;
  bg_drr?: number | null;
}

interface ResultsPanelProps {
  result: {
    filename?: string;
    is_fake?: boolean;
    confidence?: number;
    rir_mismatch_score?: number | null;
    breathing_score?: number | null;
    acoustic_comparison?: AcousticComparison | null;
  };
}
interface PredictionResponse {
filename: string;
is_fake: boolean;
confidence: number;
rir_mismatch_score?: number;
breathing_score?: number;
flagged_segments: { start_time: number; end_time: number; reason: string }[];
acoustic_comparison?: AcousticComparison;


inference_time_ms?: number;
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

function MetricComparisonBar({
  label,
  voiceValue,
  bgValue,
  unit,
}: {
  label: string;
  voiceValue: number | null | undefined;
  bgValue: number | null | undefined;
  unit: string;
}) {
  if (voiceValue === undefined || voiceValue === null || bgValue === undefined || bgValue === null) {
    return null;
  }

  const maxVal = Math.max(Math.abs(voiceValue), Math.abs(bgValue), 0.001);
  const voiceWidth = Math.round((Math.abs(voiceValue) / maxVal) * 100);
  const bgWidth = Math.round((Math.abs(bgValue) / maxVal) * 100);

  return (
    <div className="my-3 p-3 bg-gray-900/60 rounded border border-gray-700/50">
      <h4 className="text-xs font-semibold text-gray-300 mb-2 uppercase tracking-wider">{label}</h4>
      <div className="space-y-2 text-xs">
        <div>
          <div className="flex justify-between text-gray-300 mb-1">
            <span>Voice Foreground</span>
            <span className="font-mono">{voiceValue.toFixed(3)} {unit}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-indigo-400 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min(100, Math.max(5, voiceWidth))}%` }}
            />
          </div>
        </div>
        <div>
          <div className="flex justify-between text-gray-400 mb-1">
            <span>Background Ambient</span>
            <span className="font-mono">{bgValue.toFixed(3)} {unit}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-teal-400 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min(100, Math.max(5, bgWidth))}%` }}
            />
          </div>
        </div>
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
          {result.inference_time_ms != null && (
            <p className="text-xs text-gray-500 mb-3">
              Analyzed in {result.inference_time_ms.toFixed(0)} ms
            </p>
          )}
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
      <p className="text-xs text-gray-500 mt-1 mb-3">
        Higher means the voice's room echo looks more artificial.
      </p>

      {result.acoustic_comparison && (
        <div className="mt-4 pt-3 border-t border-gray-700">
          <h3 className="text-sm font-semibold text-gray-200 mb-1">
            Voice vs Background Acoustic Comparison
          </h3>
          <MetricComparisonBar
            label="Reverberation Time (RT60)"
            voiceValue={result.acoustic_comparison.voice_rt60}
            bgValue={result.acoustic_comparison.bg_rt60}
            unit="s"
          />
          <MetricComparisonBar
            label="Direct-to-Reverberant Ratio (DRR)"
            voiceValue={result.acoustic_comparison.voice_drr}
            bgValue={result.acoustic_comparison.bg_drr}
            unit="dB"
          />
        </div>
      )}
    </div>
  );
}
