from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import packages, verification, datasets, models, inference, reports

app = FastAPI(
    title="VisionTrust AI",
    description="Zero-Trust AI Assurance Framework",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(packages.router, prefix="/api/v1/packages", tags=["packages"])
app.include_router(verification.router, prefix="/api/v1/verification", tags=["verification"])
app.include_router(datasets.router, prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(inference.router, prefix="/api/v1/inference", tags=["inference"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
