from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.database import Base

class Contributor(Base):
    __tablename__ = "contributors"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrustedKey(Base):
    __tablename__ = "trusted_keys"
    contributor_id = Column(String, ForeignKey("contributors.id"), primary_key=True)
    public_key = Column(String)
    fingerprint = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    
class Package(Base):
    __tablename__ = "packages"
    id = Column(String, primary_key=True, index=True)
    contributor_id = Column(String, ForeignKey("contributors.id"))
    manifest_hash = Column(String)
    signature_valid = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String) # UPLOADED, VERIFIED, REJECTED

class TrustNode(Base):
    __tablename__ = "trust_nodes"
    id = Column(String, primary_key=True, index=True)
    node_type = Column(String) # CONTRIBUTOR, DATASET_BATCH, MODEL, INFERENCE, DETECTOR
    trust_score = Column(Float, default=0.2)
    crypto_locked = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

class DatasetBatch(Base):
    __tablename__ = "dataset_batches"
    id = Column(String, primary_key=True, index=True)
    package_id = Column(String, ForeignKey("packages.id"))
    trust_node_id = Column(String, ForeignKey("trust_nodes.id"))
    artifact_hash = Column(String)

class MLModel(Base):
    __tablename__ = "models"
    id = Column(String, primary_key=True, index=True)
    package_id = Column(String, ForeignKey("packages.id"))
    trust_node_id = Column(String, ForeignKey("trust_nodes.id"))
    artifact_hash = Column(String)
    format = Column(String) # PTH, ONNX

class InferenceRecord(Base):
    __tablename__ = "inference_records"
    id = Column(String, primary_key=True, index=True)
    model_id = Column(String, ForeignKey("models.id"))
    trust_node_id = Column(String, ForeignKey("trust_nodes.id"))
    input_hash = Column(String)
    output_hash = Column(String)
    record_hash = Column(String)
    signature = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    crypto_verified = Column(Boolean, default=True)

class Detector(Base):
    __tablename__ = "detectors"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    architecture_family = Column(String)
    health_state = Column(String) # HEALTHY, UNRELIABLE, FAILED, NOT_TESTED
    trust_node_id = Column(String, ForeignKey("trust_nodes.id"))

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    package_id = Column(String, ForeignKey("packages.id"))
    detector_id = Column(String, ForeignKey("detectors.id"))
    affected_asset = Column(String)
    reason = Column(String)
    evidence = Column(String) # JSON string
    severity = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class TrustEdge(Base):
    __tablename__ = "trust_edges"
    source_id = Column(String, ForeignKey("trust_nodes.id"), primary_key=True)
    target_id = Column(String, ForeignKey("trust_nodes.id"), primary_key=True)
    relationship = Column(String) # TRAINED_ON, USED_BY, JUDGED_BY

class MerkleEntry(Base):
    __tablename__ = "merkle_entries"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    record_id = Column(String)
    data_hash = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
