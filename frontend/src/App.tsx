import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Upload from "./pages/Upload";
import History from "./pages/History";
import Dashboard from "./pages/Dashboards";
import ModelInfoBadge from "./components/ModelInfoBadge";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="flex gap-4 p-4 border-b border-gray-700">
        <nav className="flex flex-wrap items-center gap-4 p-4 border-b border-gray-700"></nav>
        <Link to="/" className="font-semibold">AcousticSpace</Link>
        <Link to="/">Upload</Link>
        <Link to="/history">History</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/" className="font-semibold">AcousticSpace</Link>
        <ModelInfoBadge />
      </nav>
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/history" element={<History />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
