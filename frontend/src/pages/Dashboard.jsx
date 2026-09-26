import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, AlertTriangle, Box, RefreshCw } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    packagesReceived: 0,
    verified: 0,
    rejected: 0,
    warnings: 0,
    criticalFindings: 0,
    inferenceRecords: 0
  });
  
  // Dummy data for MVP layout
  const recentPackages = [
    { id: 'pkg_1a2b3c4d', contributor: 'Demo Contributor', status: 'VERIFIED', time: '10 mins ago' },
    { id: 'pkg_9f8e7d6c', contributor: 'External Vendor A', status: 'REJECTED', time: '1 hour ago' }
  ];

  return (
    <div className="p-8">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Assurance Dashboard</h1>
          <p className="text-textSecondary">Real-time overview of your pipeline's zero-trust assurance state.</p>
        </div>
        <button className="btn-secondary flex items-center gap-2">
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card p-6 flex flex-col justify-between group hover:border-primary/50 transition-colors">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-textSecondary font-medium">Packages Verified</h3>
            <div className="p-2 bg-success/10 rounded-lg text-success">
              <ShieldCheck className="w-5 h-5" />
            </div>
          </div>
          <div className="text-4xl font-bold">{stats.verified}</div>
        </div>
        
        <div className="card p-6 flex flex-col justify-between group hover:border-primary/50 transition-colors">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-textSecondary font-medium">Packages Rejected</h3>
            <div className="p-2 bg-danger/10 rounded-lg text-danger">
              <Box className="w-5 h-5" />
            </div>
          </div>
          <div className="text-4xl font-bold">{stats.rejected}</div>
        </div>
        
        <div className="card p-6 flex flex-col justify-between group hover:border-primary/50 transition-colors">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-textSecondary font-medium">Critical Findings</h3>
            <div className="p-2 bg-danger/10 rounded-lg text-danger">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <div className="text-4xl font-bold">{stats.criticalFindings}</div>
        </div>
        
        <div className="card p-6 flex flex-col justify-between group hover:border-primary/50 transition-colors">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-textSecondary font-medium">Inference Records</h3>
            <div className="p-2 bg-primary/10 rounded-lg text-primary">
              <Activity className="w-5 h-5" />
            </div>
          </div>
          <div className="text-4xl font-bold">{stats.inferenceRecords}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="col-span-2 card p-6">
          <h2 className="text-xl font-bold mb-6">Recent Packages</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-white/10 text-textSecondary text-sm uppercase">
                  <th className="pb-3 font-medium">Package ID</th>
                  <th className="pb-3 font-medium">Contributor</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium">Time</th>
                </tr>
              </thead>
              <tbody>
                {recentPackages.map((pkg, i) => (
                  <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-4 font-mono text-sm text-primary">{pkg.id}</td>
                    <td className="py-4">{pkg.contributor}</td>
                    <td className="py-4">
                      <span className={pkg.status === 'VERIFIED' ? 'badge-success' : 'badge-danger'}>
                        {pkg.status}
                      </span>
                    </td>
                    <td className="py-4 text-textSecondary text-sm">{pkg.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        <div className="card p-6">
          <h2 className="text-xl font-bold mb-6">Detector Health</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/5">
              <span>SentinelCore</span>
              <span className="badge-success">HEALTHY</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/5">
              <span>DataGuard: pHash</span>
              <span className="badge-success">HEALTHY</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/5">
              <span>ModelShield: Probe</span>
              <span className="badge-success">HEALTHY</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
