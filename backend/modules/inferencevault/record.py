import json
import uuid
import time
from datetime import datetime
from backend.core.crypto.hashing import hash_data
from backend.core.crypto.signing import sign_data
from typing import Dict, Any

class InferenceVault:
    def __init__(self, private_key_pem: bytes, public_key_pem: bytes):
        self.private_key = private_key_pem
        self.public_key = public_key_pem
        self.sequence_nonce = 0
        
    def create_record(
        self,
        input_hash: str,
        model_digest: str,
        preprocessing_config_hash: str,
        inference_config_hash: str,
        output: Any
    ) -> Dict[str, Any]:
        """
        Creates a cryptographically bound inference record.
        """
        self.sequence_nonce += 1
        record_id = f"inf_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().isoformat()
        
        # Structure the payload
        payload = {
            "record_id": record_id,
            "input_hash": input_hash,
            "model_digest": model_digest,
            "preprocessing_config_hash": preprocessing_config_hash,
            "inference_config_hash": inference_config_hash,
            "output": output,
            "timestamp": timestamp,
            "sequence_nonce": self.sequence_nonce,
            "system_version": "1.0.0"
        }
        
        # Serialize deterministically
        serialized = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
        
        record_hash = hash_data(serialized)
        signature = sign_data(self.private_key, serialized)
        
        record = {
            **payload,
            "record_hash": record_hash,
            "signature": signature.hex()
        }
        
        return record

    def verify_record(self, record: Dict[str, Any]) -> bool:
        """
        Verifies an existing record.
        """
        from backend.core.crypto.signing import verify_signature
        
        try:
            expected_hash = record["record_hash"]
            signature = bytes.fromhex(record["signature"])
            
            # Reconstruct payload
            payload = {
                "record_id": record["record_id"],
                "input_hash": record["input_hash"],
                "model_digest": record["model_digest"],
                "preprocessing_config_hash": record["preprocessing_config_hash"],
                "inference_config_hash": record["inference_config_hash"],
                "output": record["output"],
                "timestamp": record["timestamp"],
                "sequence_nonce": record["sequence_nonce"],
                "system_version": record["system_version"]
            }
            
            serialized = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
            actual_hash = hash_data(serialized)
            
            if actual_hash != expected_hash:
                return False
                
            return verify_signature(self.public_key, signature, serialized)
        except Exception:
            return False
