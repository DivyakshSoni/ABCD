import React from 'react';
import { Database, ShieldAlert, Key, CheckCircle } from 'lucide-react';

const AuditLog = () => {
  const logs = [
    { id: 1, type: 'MERKLE_APPEND', record: 'inf_7b8c9d0e', status: 'SUCCESS', time: '5 mins ago', hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' },
    { id: 2, type: 'SIGNATURE_VERIFY', record: 'pkg_1a2b3c4d', status: 'SUCCESS', time: '10 mins ago', hash: 'N/A' },
    { id: 3, type: 'CRYPTO_FAILURE', record: 'inf_ff112233', status: 'FAILED', time: '1 hour ago', hash: 'mismatch' }
  ];

  return (
    <div className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Merkle Audit Log</h1>
        <p className="text-textSecondary">Tamper-evident history of cryptographic verifications and inference records.</p>
      </header>

      <div className="card p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-black/10 text-textSecondary text-sm uppercase">
                <th className="pb-3 font-medium">Event Type</th>
                <th className="pb-3 font-medium">Record ID</th>
                <th className="pb-3 font-medium">Status</th>
                <th className="pb-3 font-medium">Hash / Details</th>
                <th className="pb-3 font-medium">Time</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="border-b border-black/5 hover:bg-black/5 transition-colors">
                  <td className="py-4 font-mono text-sm flex items-center gap-2">
                    {log.type === 'CRYPTO_FAILURE' ? <ShieldAlert className="w-4 h-4 text-danger"/> : <Database className="w-4 h-4 text-primary"/>}
                    {log.type}
                  </td>
                  <td className="py-4 text-sm">{log.record}</td>
                  <td className="py-4">
                    <span className={log.status === 'SUCCESS' ? 'badge-success' : 'badge-danger'}>
                      {log.status}
                    </span>
                  </td>
                  <td className="py-4 font-mono text-xs text-textSecondary truncate max-w-xs">{log.hash}</td>
                  <td className="py-4 text-textSecondary text-sm">{log.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AuditLog;
