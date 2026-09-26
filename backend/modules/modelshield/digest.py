import os
from backend.core.crypto.hashing import hash_file
from typing import Dict, Any

def verify_model_digest(model_path: str, expected_hash: str) -> Dict[str, Any]:
    if not os.path.exists(model_path):
        return {
            "verified": False,
            "message": "Model artifact not found",
            "actual_hash": None
        }
        
    actual_hash = hash_file(model_path)
    verified = (actual_hash == expected_hash)
    
    return {
        "verified": verified,
        "expected_hash": expected_hash,
        "actual_hash": actual_hash,
        "message": "Hash matched." if verified else "Hash mismatch. Potential tampering detected."
    }
