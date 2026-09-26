import React from 'react';
import { FileText, Download, ShieldCheck } from 'lucide-react';

const Reports = () => {
  return (
    <div className="p-8 h-full flex flex-col">
      <header className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Assurance Reports</h1>
        <p className="text-textSecondary">Generated transparency and compliance reports.</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-6 flex flex-col">
          <div className="flex justify-between items-start mb-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/10 rounded-lg text-primary">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg">Report: pkg_1a2b3c4d</h3>
                <p className="text-sm text-textSecondary">Generated today at 10:45 AM</p>
              </div>
            </div>
            <span className="badge-success flex items-center gap-1"><ShieldCheck className="w-3 h-3"/> Verified</span>
          </div>
          <p className="text-textSecondary mb-6 flex-1">
            Complete zero-trust analysis including cryptographic integrity, dataset pHash duplicates (0 found), behavioral analysis (PASS), and SentinelCore verifier health (HEALTHY).
          </p>
          <button className="btn-secondary flex items-center justify-center gap-2 w-full">
            <Download className="w-4 h-4" /> Export PDF
          </button>
        </div>

        <div className="card p-6 flex flex-col opacity-50">
          <div className="flex justify-between items-start mb-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-black/10 rounded-lg text-textSecondary">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg">No other reports</h3>
                <p className="text-sm text-textSecondary">Upload and verify a package to generate</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
