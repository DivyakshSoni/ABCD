from fastapi import APIRouter, Depends, HTTPException
from backend.modules.dataguard.duplicates import find_duplicates_phash
import os

router = APIRouter()

@router.get("/{package_id}/analyze")
def analyze_dataset(package_id: str):
    dataset_dir = os.path.join("data/uploads", package_id, "dataset")
    if not os.path.exists(dataset_dir):
        raise HTTPException(status_code=404, detail="Dataset not found in package")
        
    # Run duplicate detection
    dup_results = find_duplicates_phash(dataset_dir)
    
    return {
        "package_id": package_id,
        "duplicates": dup_results
    }
