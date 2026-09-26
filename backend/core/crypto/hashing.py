import hashlib
import os

def hash_data(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def hash_file(filepath: str, chunk_size: int = 8192) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def hash_dict(d: dict) -> str:
    import json
    # Canonicalize dictionary: sort keys, remove whitespace
    serialized = json.dumps(d, sort_keys=True, separators=(',', ':'))
    return hash_data(serialized.encode('utf-8'))
