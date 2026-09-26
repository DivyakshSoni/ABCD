import React from 'react';
import { GitMerge, Database, Cpu, Activity, Info } from 'lucide-react';

const TrustGraph = () => {
  return (
    <div className="p-8 h-full flex flex-col">
      <header className="mb-6">
        <h1 className="text-3xl font-bold mb-2">TrustFlow Graph</h1>
        <p className="text-textSecondary">Visualization of dependency propagation and computed trust scores.</p>
      </header>
      
      <div className="flex-1 card p-6 relative overflow-hidden flex items-center justify-center">
        {/* Placeholder for D3 / React Flow. For MVP we use a simple flex layout of nodes. */}
        <div className="absolute top-4 left-4 flex gap-4 text-sm text-textSecondary bg-background/50 p-3 rounded-lg border border-black/5 backdrop-blur-md">
          <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-success"></div> Trusted (&gt;0.7)</div>
          <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-warning"></div> Review (0.3 - 0.7)</div>
          <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-danger"></div> Untrusted/Locked (&lt;0.3)</div>
        </div>

        <div className="flex flex-col items-center gap-16">
          {/* Contributor */}
          <div className="flex items-center gap-8 relative">
            <div className="w-64 bg-surface p-4 rounded-xl border-l-4 border-success shadow-lg flex flex-col items-center z-10 relative">
              <div className="p-2 bg-success/10 rounded-full mb-2"><Database className="w-6 h-6 text-success" /></div>
              <h4 className="font-bold">Contributor A</h4>
              <p className="text-xs text-textSecondary">T=0.85</p>
            </div>
            
            {/* Edge line */}
            <div className="absolute top-1/2 left-1/2 w-8 h-16 border-r-2 border-b-2 border-black/20 -translate-x-1/2 rounded-br-xl"></div>
          </div>
          
          {/* Model */}
          <div className="flex gap-16">
            <div className="w-64 bg-surface p-4 rounded-xl border-l-4 border-warning shadow-lg flex flex-col items-center z-10">
              <div className="p-2 bg-warning/10 rounded-full mb-2"><Cpu className="w-6 h-6 text-warning" /></div>
              <h4 className="font-bold">YOLOv8 Model</h4>
              <p className="text-xs text-textSecondary">T=0.55 (Behavioral warning)</p>
            </div>
          </div>
          
          {/* Inference */}
          <div className="flex gap-8">
            <div className="w-64 bg-surface p-4 rounded-xl border-l-4 border-danger shadow-lg flex flex-col items-center z-10 relative">
              {/* Vertical line up */}
              <div className="absolute bottom-full left-1/2 w-0.5 h-16 bg-black/20 -translate-x-1/2"></div>
              
              <div className="p-2 bg-danger/10 rounded-full mb-2"><Activity className="w-6 h-6 text-danger" /></div>
              <h4 className="font-bold">Inference REC-001</h4>
              <p className="text-xs text-textSecondary">T=0.00 (Crypto Locked)</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default TrustGraph;
