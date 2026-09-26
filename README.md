# VisionTrust AI

**Zero-Trust AI Assurance Framework (ZTAAF)**
*SIH26228 | Offline / Air-Gapped Operation*

VisionTrust AI is an offline, zero-trust assurance layer for computer-vision pipelines. It evaluates the integrity and trustworthiness of the dataset, model, inference process, provenance artifacts, and assurance mechanisms themselves.

The product combines cryptographic verification, dataset integrity analysis, model behavioral analysis, inference provenance, verifier self-tests, and tamper-evident audit logging.

## Core Features
- **DataGuard**: Dataset integrity, duplicate flooding detection, label consistency, and anomaly checking.
- **ModelShield**: Digest verification, behavioral fingerprinting, access-level detection.
- **InferenceVault**: Cryptographically bound inference records appended to a Merkle audit log.
- **SentinelCore**: Verifier self-defense using canary sets to gate unreliable detector evidence.
- **TrustFlow**: Evidence correlation and directed trust propagation graph.
- **RedForge**: Offline laboratory for controlled attack generation and ground-truth validation.
- **AssuranceHub**: Analyst-facing dashboard reporting what passed, failed, and why.

---

## Quickstart (Offline Execution)

### 1. Setup Backend
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r backend/requirements.txt
```

### 2. Initialize Database and Trusted Key
```bash
python backend/scripts/init_db.py --init --register
```
*This creates the SQLite database and generates a `demo_contributor` key pair in `trusted_keys/`.*

### 3. Generate a Test Package (RedForge Demo)
```bash
python backend/scripts/create_demo_package.py
```
*This generates a signed VisionTrust package in `data/demo_package.zip`.*

### 4. Run Backend Server
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Run Frontend Server
```bash
cd frontend
npm install
npm run dev
```

### 6. Using the Product
1. Open the UI at `http://localhost:5173`.
2. Go to **Upload Package** and upload `data/demo_package.zip`.
3. The backend will verify the Ed25519 signature against the trusted key registry, calculate the SHA-256 hashes, and start DataGuard & ModelShield analyses.
4. Navigate to **Trust Graph** to view the dependencies and trust state.
5. Check **Audit Log** to view cryptographic actions.

## Documentation
- `docs/architecture.md`: Full architectural and implementation plan.
