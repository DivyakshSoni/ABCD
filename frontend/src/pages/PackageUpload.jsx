import React, { useState } from 'react';
import { UploadCloud, CheckCircle, AlertTriangle, FileUp, X } from 'lucide-react';
import axios from 'axios';

const PackageUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setUploading(true);
    setError(null);
    setResult(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await axios.post('http://localhost:8000/api/v1/packages/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred during upload.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Upload Package</h1>
        <p className="text-textSecondary">Submit a signed artifact package for zero-trust assurance verification.</p>
      </header>

      {!result && !error && (
        <div 
          className={`card border-2 border-dashed ${file ? 'border-primary bg-primary/5' : 'border-black/20 hover:border-primary/50'} p-12 text-center transition-all cursor-pointer flex flex-col items-center justify-center min-h-[300px]`}
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileUpload').click()}
        >
          <input 
            type="file" 
            id="fileUpload" 
            className="hidden" 
            accept=".zip"
            onChange={(e) => setFile(e.target.files[0])}
          />
          
          {file ? (
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mb-4">
                <FileUp className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">{file.name}</h3>
              <p className="text-textSecondary mb-6">{(file.size / (1024*1024)).toFixed(2)} MB</p>
              
              <div className="flex gap-4">
                <button 
                  className="btn-secondary px-6"
                  onClick={(e) => { e.stopPropagation(); setFile(null); }}
                >
                  Cancel
                </button>
                <button 
                  className="btn-primary px-8"
                  onClick={(e) => { e.stopPropagation(); handleUpload(); }}
                  disabled={uploading}
                >
                  {uploading ? 'Uploading...' : 'Verify Package'}
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 bg-black/5 rounded-full flex items-center justify-center mb-4">
                <UploadCloud className="w-8 h-8 text-textSecondary" />
              </div>
              <h3 className="text-xl font-bold mb-2">Click or drag package to upload</h3>
              <p className="text-textSecondary">Requires a valid VisionTrust .zip package containing manifest and signature.</p>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="card p-6 border-danger/50 bg-danger/5">
          <div className="flex items-start gap-4">
            <div className="p-2 bg-danger/20 rounded-lg text-danger mt-1">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-danger mb-2">Verification Failed</h3>
              <p className="text-textPrimary">{error}</p>
              <button 
                className="btn-secondary mt-4"
                onClick={() => { setError(null); setFile(null); }}
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      )}

      {result && (
        <div className="card p-6 border-success/50 bg-success/5">
          <div className="flex items-start gap-4">
            <div className="p-2 bg-success/20 rounded-lg text-success mt-1">
              <CheckCircle className="w-6 h-6" />
            </div>
            <div className="w-full">
              <h3 className="text-xl font-bold text-success mb-2">Package Uploaded</h3>
              <div className="grid grid-cols-2 gap-4 my-4">
                <div className="bg-background/50 p-3 rounded-lg border border-black/5">
                  <p className="text-xs text-textSecondary uppercase tracking-wider mb-1">Package ID</p>
                  <p className="font-mono text-sm">{result.id}</p>
                </div>
                <div className="bg-background/50 p-3 rounded-lg border border-black/5">
                  <p className="text-xs text-textSecondary uppercase tracking-wider mb-1">Status</p>
                  <p className="font-bold text-primary">{result.status}</p>
                </div>
                <div className="bg-background/50 p-3 rounded-lg border border-black/5">
                  <p className="text-xs text-textSecondary uppercase tracking-wider mb-1">Contributor ID</p>
                  <p className="text-sm">{result.contributor_id}</p>
                </div>
                <div className="bg-background/50 p-3 rounded-lg border border-black/5">
                  <p className="text-xs text-textSecondary uppercase tracking-wider mb-1">Signature Validation</p>
                  <p className="text-sm">
                    {result.signature_valid ? 
                      <span className="text-success flex items-center gap-1"><CheckCircle className="w-4 h-4"/> Valid</span> : 
                      <span className="text-danger flex items-center gap-1"><AlertTriangle className="w-4 h-4"/> Invalid</span>}
                  </p>
                </div>
              </div>
              <button 
                className="btn-primary mt-4 w-full"
                onClick={() => { setResult(null); setFile(null); }}
              >
                Upload Another
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PackageUpload;
