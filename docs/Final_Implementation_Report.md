# VisionTrust AI (ZTAAF) – Final Implementation Report

**Project Code:** SIH26228  
**Scope:** Offline / Air-Gapped Zero-Trust Assurance Framework MVP  

## 1. Executive Summary

This document serves as the comprehensive record of the working implementation of **VisionTrust AI**, the offline Zero-Trust AI Assurance Framework (ZTAAF) built for evaluating the integrity and trustworthiness of computer vision pipelines.

The framework successfully implements a strictly offline architecture (no cloud dependency), leveraging cryptographic foundations (Ed25519 signatures, SHA-256 hashes, Merkle trees) combined with analytical evaluation modules (pHash duplicate flooding, structural validation, and canary-based trust gating) to provide an analyst with a concrete trust signal for incoming AI packages.

---

## 2. Technical Stack

- **Backend Logic & API:** Python 3.11, FastAPI, Uvicorn
- **Database Store:** SQLite via SQLAlchemy ORM (Offline relational store)
- **Cryptography Base:** `cryptography` (Primitives for Ed25519, SHA-256)
- **Computer Vision & ML Analytics:** PyTorch, scikit-image, scikit-learn, ImageHash
- **Frontend Analyst Dashboard:** React (Vite), Tailwind CSS v4, Lucide React (Icons)

---

## 3. Implemented Modules

### 3.1. Cryptographic Engine & Trust Floor
- **Hashing (`backend/core/crypto/hashing.py`)**: Uses deterministic `SHA-256` for fingerprinting datasets, models, and manifests.
- **Digital Signatures (`backend/core/crypto/signing.py`)**: Asymmetric `Ed25519` key pairs verify the contributor's identity and detect tamper attempts on the package manifest.
- **Merkle Audit Log (`backend/core/crypto/merkle.py`)**: Inference records and verification events are structured into a tamper-evident Merkle Tree structure, allowing continuous, offline integrity proofs.

### 3.2. DataGuard (Dataset Verification)
- **Structural Integrity (`backend/modules/dataguard/structure.py`)**: Verifies the topological correctness of datasets (COCO JSON syntax / YOLO folder structures).
- **Poisoning Detection (`backend/modules/dataguard/duplicates.py`)**: Uses Perceptual Hashing (pHash) to detect duplicate flooding—a common vector for data poisoning attacks.

### 3.3. ModelShield (Model Verification)
- **Digest Verification (`backend/modules/modelshield/digest.py`)**: Validates the incoming `.pth` or `.onnx` models against the cryptographically signed manifest digest.
- **Behavioral Probing (`backend/modules/modelshield/behavior.py`)**: Foundational framework for sending black-box synthetic payloads to the model and capturing the activation statistics, verifying intended model behavior without relying on vendor claims.

### 3.4. SentinelCore & TrustFlow
- **TrustGraph (`backend/core/sentinelcore/trust_graph.py`)**: A directed acyclic graph that defines the relationship between the Contributor -> Dataset -> Model -> Inference Record. 
- **Propagation (`backend/core/sentinelcore/propagation.py`)**: A failure at any node (e.g., a signature failure or a pHash flood) immediately propagates a strict `0.0` trust score to all dependent downstream nodes, locking the pipeline.
- **Canary Defense (`backend/core/sentinelcore/canary.py`)**: Injects "canary" (known bad) inputs into the verification pipeline to ensure the anomaly detectors themselves haven't been compromised or bypassed.

### 3.5. InferenceVault
- **Cryptographic Binding (`backend/modules/inferencevault/record.py`)**: Binds an inference result (input image + model ID + outputs) into a single hashed struct that gets appended to the Merkle tree.

### 3.6. RedForge (Offline Attack Laboratory)
- **Controlled Injection (`backend/modules/redforge/attacks.py`)**: Allows evaluators to programmatically inject dataset duplicate floods to test DataGuard's deterministic rejection capabilities. Provided via `create_demo_package.py`.

### 3.7. AssuranceHub (Frontend)
- **Dashboard (`frontend/src/pages/Dashboard.jsx`)**: High-level real-time metrics summarizing verified packages, critical findings, and SentinelCore health.
- **Interactive Verification (`frontend/src/pages/PackageUpload.jsx`)**: Allows drag-and-drop ingestion of signed `.zip` payload packages for immediate backend verification.
- **Trust Graph UI (`frontend/src/pages/TrustGraph.jsx`)**: Visually maps the trust propagation and status of Contributor/Model/Inferences.
- **Audit Log (`frontend/src/pages/AuditLog.jsx`)**: Analyst view into the Merkle cryptographic history.

---

## 4. Database Schema Structure
The offline SQLite database (`visiontrust.db`) leverages the following ORM relationships:
- **Contributors**: `id`, `public_key`, `trust_score`.
- **Packages**: `id`, `contributor_id`, `manifest_hash`, `signature_valid`, `status`.
- **Datasets**: `id`, `package_id`, `format`, `image_count`, `hash_digest`.
- **Models**: `id`, `package_id`, `architecture`, `hash_digest`.
- **InferenceRecords**: `id`, `model_id`, `dataset_id`, `merkle_hash`.
- **TrustNodes & TrustEdges**: Represents the TrustFlow engine state.

---

## 5. Setup & Execution Commands
The system is built to operate immediately after standard package installations.

**Start the API Server**
```bash
.\venv\Scripts\activate
$env:PYTHONPATH="."
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Start the Analyst Dashboard**
```bash
cd frontend
npm run dev
```

**Generate Demo Data (RedForge)**
```bash
python -m backend.scripts.init_db --init --register
python -m backend.scripts.create_demo_package
```

---

## 6. End-to-End Workflow Delivered
1. **Key Generation**: A trusted authority registers an Ed25519 keypair for a Contributor.
2. **Payload Packaging**: Contributor cryptographically signs the manifest containing dataset/model hashes.
3. **Ingestion**: The analyst uploads the `.zip` package via AssuranceHub.
4. **Verification**: 
   - Signature is verified against the key registry.
   - Files are hashed and compared to manifest digests.
   - DataGuard scans for pHash duplicates.
5. **Propagation**: The TrustFlow engine assigns scores. If any cryptographic or severe analytic check fails, downstream trust is locked.
6. **Audit**: All actions append immutably to the Merkle log.

*This concludes the complete foundational MVP implementation of the VisionTrust AI Assurance Framework.*
