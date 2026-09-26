from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import uuid
import os
import zipfile
import json
import shutil
from backend.db.database import get_db
from backend.db import models
from backend.core.schemas.package import PackageResponse
from backend.core.crypto.signing import verify_signature

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=PackageResponse)
async def upload_package(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP packages are allowed")
    
    package_id = f"pkg_{uuid.uuid4().hex[:8]}"
    package_dir = os.path.join(UPLOAD_DIR, package_id)
    os.makedirs(package_dir, exist_ok=True)
    
    zip_path = os.path.join(package_dir, file.filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(package_dir)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP archive")

    # Read manifest
    manifest_path = os.path.join(package_dir, "manifest.json")
    signature_path = os.path.join(package_dir, "package.sig")
    
    if not os.path.exists(manifest_path) or not os.path.exists(signature_path):
        raise HTTPException(status_code=400, detail="Missing manifest.json or package.sig")
        
    with open(manifest_path, 'rb') as f:
        manifest_data = f.read()
        
    with open(signature_path, 'rb') as f:
        signature_data = f.read()
        
    manifest = json.loads(manifest_data)
    contributor_id = manifest.get("contributor_id")
    if not contributor_id:
        raise HTTPException(status_code=400, detail="Missing contributor_id in manifest")
        
    # Check trusted key
    trusted_key = db.query(models.TrustedKey).filter(models.TrustedKey.contributor_id == contributor_id).first()
    signature_valid = False
    
    if trusted_key:
        signature_valid = verify_signature(
            trusted_key.public_key.encode('utf-8'),
            signature_data,
            manifest_data
        )
        
    from backend.core.crypto.hashing import hash_data
    manifest_hash = hash_data(manifest_data)
    
    new_package = models.Package(
        id=package_id,
        contributor_id=contributor_id,
        manifest_hash=manifest_hash,
        signature_valid=signature_valid,
        status="UPLOADED"
    )
    
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    
    return new_package

@router.get("/{package_id}", response_model=PackageResponse)
def get_package(package_id: str, db: Session = Depends(get_db)):
    pkg = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg
