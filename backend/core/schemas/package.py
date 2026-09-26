from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PackageBase(BaseModel):
    contributor_id: str
    manifest_hash: str
    signature_valid: bool

class PackageCreate(PackageBase):
    pass

class PackageResponse(PackageBase):
    id: str
    uploaded_at: datetime
    status: str
    
    class Config:
        from_attributes = True

class VerificationResult(BaseModel):
    package_id: str
    trusted_key_status: str
    signature_status: str
    manifest_status: str
    dataset_status: str
    model_status: str
