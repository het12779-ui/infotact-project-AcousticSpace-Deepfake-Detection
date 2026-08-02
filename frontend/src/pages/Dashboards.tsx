import { useEffect, useState } from "react";
interface HistoryEntry {
    timestamp: string;
    filename: string;
    is_fake: boolean;
    confidence: number;
}
export default function Dashboard() {
    const [entries, setEntries] = useState<HistoryEntry[]>([]);
    1

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
            {total === 0 && (
                <p className="text-gray-400 mt-6">No analyses yet - upload a file to see stats here.</p>
            )}
        </div>
    );
}