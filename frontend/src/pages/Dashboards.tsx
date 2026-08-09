import { useEffect, useState } from "react";
interface HistoryEntry {
    timestamp: string;
    filename: string;
    is_fake: boolean;
    confidence: number;
}
// Update these numbers from docs/results_log.md whenever the model is retrained
const MODEL_RESULTS = [
    { name: "Validation split", accuracy: "0.850", eer: "0.200" },
    { name: "Held-out demo set", accuracy: "0.800", eer: "0.250" },
    { name: "Attack test (before defense)", accuracy: "0.750", eer: "0.300" },
    { name: "Attack test (after defense)", accuracy: "0.875", eer: "0.150" },
    { name: "Generalization test", accuracy: "0.650", eer: "0.400" },
];
export default function Dashboard() {
    const [entries, setEntries] = useState<HistoryEntry[]>([]);

    const [loading, setLoading] = useState(true);
    useEffect(() => {
        fetch("http://localhost:8000/history")
            .then((res) => res.json())
            .then((data) => setEntries(data.history))
            .catch(() => setEntries([]))
            .finally(() => setLoading(false));
    }, []);
    if (loading) return <p className="p-6">Loading dashboard...</p>;
    const total = entries.length;
    const fakeCount = entries.filter((e) => e.is_fake).length;
    const avgConfidence = total > 0
        ? entries.reduce((sum, e) => sum + e.confidence, 0) / total
        : 0;
    return (
        <div className="max-w-2xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
            <div className="grid grid-cols-3 gap-4">
                <div className="p-4 rounded-lg border border-gray-700 text-center">
                    <div className="text-2xl font-bold">{total}</div>
                    <div className="text-sm text-gray-400">Total analyzed</div>
                </div>
                <div className="p-4 rounded-lg border border-gray-700 text-center">
                    <div className="text-2xl font-bold text-red-400">
                        {total > 0 ? ((fakeCount / total) * 100).toFixed(0) : 0}%
                    </div>
                    <div className="text-sm text-gray-400">Flagged as fake</div>
                </div>
                <div className="p-4 rounded-lg border border-gray-700 text-center">
                    <div className="text-2xl font-bold">{(avgConfidence * 100).toFixed(0)}%</div>
                    <div className="text-sm text-gray-400">Avg. confidence</div>
                </div>
            </div>

            {/* Model Performance Summary */}
            <div className="mt-8">
                <h2 className="text-lg font-semibold mb-3">Model Performance Summary</h2>
                <table className="w-full text-left text-sm">
                    <thead>
                        <tr className="border-b border-gray-600 text-gray-400">
                            <th className="py-2">Test Set</th>
                            <th className="py-2">Accuracy</th>
                            <th className="py-2">EER</th>
                        </tr>
                    </thead>
                    <tbody>
                        {MODEL_RESULTS.map((r, i) => (
                            <tr key={i} className="border-b border-gray-800">
                                <td className="py-2">{r.name}</td>
                                <td>{r.accuracy}</td>
                                <td>{r.eer}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {total === 0 && (
                <p className="text-gray-400 mt-6">No analyses yet - upload a file to see stats here.</p>
            )}
        </div>
    );
}