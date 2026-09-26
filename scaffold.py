import os

dirs = [
    "backend/api",
    "backend/core/schemas",
    "backend/core/sentinelcore",
    "backend/core/crypto",
    "backend/modules/dataguard",
    "backend/modules/modelshield",
    "backend/modules/inferencevault",
    "backend/modules/driftlens",
    "backend/modules/redforge",
    "backend/llm",
    "backend/db",
    "frontend",
    "cli",
    "trusted_keys",
    "probes",
    "data/reference_datasets",
    "data/canary_sets",
    "data/sample_models",
    "docs",
    "tests"
]

for d in dirs:
    os.makedirs(f"b:/Projects/SIH/VisionTrustAI/{d}", exist_ok=True)

print("Directories created successfully.")
