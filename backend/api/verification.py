from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db import models
from backend.core.sentinelcore.trust_graph import TrustNode, TrustGraph
from backend.core.sentinelcore.propagation import propagate_trust
from backend.modules.dataguard.structure import detect_dataset_format_and_validate
from backend.modules.modelshield.digest import verify_model_digest
from typing import Dict, Any
import os

router = APIRouter()

@router.get("/{package_id}")
def verify_package(package_id: str, db: Session = Depends(get_db)):
    pkg = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
        
    package_dir = os.path.join("data/uploads", package_id)
    dataset_dir = os.path.join(package_dir, "dataset")
    model_dir = os.path.join(package_dir, "model")
    
    results = {
        "package_id": package_id,
        "signature_valid": pkg.signature_valid,
        "dataset_validation": None,
        "model_validation": None,
        "trust_graph_updated": False
    }
    
    # 1. Check dataset
    if os.path.exists(dataset_dir):
        ds_results = detect_dataset_format_and_validate(dataset_dir)
        results["dataset_validation"] = ds_results
        
    # 2. Check model (assuming .pth or .onnx)
    if os.path.exists(model_dir):
        model_files = [f for f in os.listdir(model_dir) if f.endswith(('.pth', '.onnx'))]
        if model_files:
            model_path = os.path.join(model_dir, model_files[0])
            # For MVP, assume the model_digest was passed in manifest and saved somewhere. 
            # We'll just run a basic dummy check if we don't have expected hash
            mod_results = verify_model_digest(model_path, "expected_hash_here")
            results["model_validation"] = {
                "found": True,
                "file": model_files[0],
                "digest_check": mod_results
            }
        else:
            results["model_validation"] = {"found": False, "message": "No model file found"}
            
    # 3. TrustFlow update
    if not pkg.signature_valid:
        # Crypto failure -> propagate distrust
        pkg.status = "REJECTED"
    else:
        pkg.status = "VERIFIED"
        
    db.commit()
    
    return results
