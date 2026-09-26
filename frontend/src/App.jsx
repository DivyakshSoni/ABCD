import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Shield, Home, UploadCloud, Activity, Database, FileText } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import PackageUpload from './pages/PackageUpload';
import TrustGraph from './pages/TrustGraph';
import AuditLog from './pages/AuditLog';
import Reports from './pages/Reports';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-background">
        {/* Sidebar */}
        <aside className="w-64 border-r border-secondary bg-surface/80 backdrop-blur-md flex flex-col">
          <div className="p-6 flex items-center gap-3">
            <div className="p-2 bg-primary/20 rounded-lg shadow-[0_0_15px_rgba(201,181,156,0.5)]">
              <Shield className="w-6 h-6 text-primary" />
            </div>
            <span className="text-xl font-bold tracking-tight text-textPrimary">VisionTrust AI</span>
          </div>
          <nav className="flex-1 px-4 py-4 space-y-2">
            <Link to="/" className="flex items-center gap-3 px-4 py-3 rounded-lg text-textSecondary hover:bg-black/5 hover:text-textPrimary transition-colors">
              <Home className="w-5 h-5" />
              <span>Dashboard</span>
            </Link>
            <Link to="/upload" className="flex items-center gap-3 px-4 py-3 rounded-lg text-textSecondary hover:bg-black/5 hover:text-textPrimary transition-colors">
              <UploadCloud className="w-5 h-5" />
              <span>Upload Package</span>
            </Link>
            <Link to="/trust-graph" className="flex items-center gap-3 px-4 py-3 rounded-lg text-textSecondary hover:bg-black/5 hover:text-textPrimary transition-colors">
              <Activity className="w-5 h-5" />
              <span>Trust Graph</span>
            </Link>
            <Link to="/audit-log" className="flex items-center gap-3 px-4 py-3 rounded-lg text-textSecondary hover:bg-black/5 hover:text-textPrimary transition-colors">
              <Database className="w-5 h-5" />
              <span>Audit Log</span>
            </Link>
            <Link to="/reports" className="flex items-center gap-3 px-4 py-3 rounded-lg text-textSecondary hover:bg-black/5 hover:text-textPrimary transition-colors">
              <FileText className="w-5 h-5" />
              <span>Reports</span>
            </Link>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto bg-background">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<PackageUpload />} />
            <Route path="/trust-graph" element={<TrustGraph />} />
            <Route path="/audit-log" element={<AuditLog />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
