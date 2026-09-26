# VisionTrust AI - Architecture & Implementation Plan

## 1. Project Overview
VisionTrust AI is an offline, air-gapped Zero-Trust AI Assurance Framework (ZTAAF). It evaluates the integrity and trustworthiness of a computer vision pipeline, applying zero-trust principles to the assurance layer itself. 

## 2. Core Architecture
- **Backend**: Python 3.11+, FastAPI, Pydantic, SQLite, SQLAlchemy.
- **Frontend**: React, Vite, Tailwind CSS, Recharts.
- **CLI**: Headless CLI using Typer or Click.
- **ML/CV**: PyTorch, TorchScript, ONNX Runtime, scikit-image, scikit-learn.
- **Crypto**: `hashlib` (SHA-256), `cryptography` (Ed25519), custom Merkle Tree.

## 3. Implementation Phases

### Phase 1: Foundation (Current)
- Initialize project structure.
- Setup FastAPI backend and basic SQLite database schema.
- Implement Trusted-Key Registry and Package Upload.
- Implement Cryptographic primitives (Ed25519, SHA-256).

### Phase 2: Inference & TrustFlow
- Implement InferenceVault (Signed records, Merkle audit log).
- Implement basic TrustFlow engine (Nodes, Edges, Evidence, Scoring).
- Implement SentinelCore canary framework.

### Phase 3: DataGuard & ModelShield
- Implement basic DataGuard (Structure validation, Duplicate detection via pHash).
- Implement basic ModelShield (Digest verification, Behavioral fingerprinting).
- Integrate ML detectors with TrustFlow.

### Phase 4: Frontend & CLI
- Build AssuranceHub (Dashboard, Trust Graph visualization).
- Complete CLI commands for offline air-gapped execution.
- Implement reporting capabilities.

### Phase 5: Advanced & Refinement
- RedForge (Controlled attacks).
- DriftLens (Distribution shift).
- Full end-to-end tests and offline packaging.

## 4. Module Boundaries
- `backend/core/crypto`: Hashing, signing, Merkle trees.
- `backend/core/sentinelcore`: Canaries, TrustFlow graph.
- `backend/modules/dataguard`: Dataset checks.
- `backend/modules/modelshield`: Model checks.
- `backend/modules/inferencevault`: Inference recording.
- `backend/api`: FastAPI routes.
- `cli`: Command-line interface wrapping backend logic.
- `frontend`: React SPA for AssuranceHub.
