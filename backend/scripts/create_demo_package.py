import os
import json
import zipfile
import shutil
from backend.core.crypto.hashing import hash_data
from backend.core.crypto.signing import sign_data

def create_demo_package():
    # 1. Ensure keys exist
    if not os.path.exists("trusted_keys/demo_private.pem"):
        print("Please run init_db.py --register first to generate keys.")
        return

    with open("trusted_keys/demo_private.pem", "rb") as f:
        priv_key = f.read()

    pkg_dir = "data/sample_package"
    os.makedirs(pkg_dir, exist_ok=True)
    os.makedirs(os.path.join(pkg_dir, "dataset", "images"), exist_ok=True)
    os.makedirs(os.path.join(pkg_dir, "dataset", "annotations"), exist_ok=True)
    os.makedirs(os.path.join(pkg_dir, "model"), exist_ok=True)
    os.makedirs(os.path.join(pkg_dir, "provenance"), exist_ok=True)

    # 2. Create dummy content
    # Dataset
    with open(os.path.join(pkg_dir, "dataset", "annotations", "instances.json"), "w") as f:
        json.dump({"images": [{"id": 1, "file_name": "test.jpg"}], "annotations": []}, f)
    
    with open(os.path.join(pkg_dir, "dataset", "images", "test.jpg"), "w") as f:
        f.write("fake image data")

    # Model
    model_path = os.path.join(pkg_dir, "model", "model.onnx")
    with open(model_path, "w") as f:
        f.write("fake model data")

    # Provenance
    with open(os.path.join(pkg_dir, "provenance", "training_manifest.json"), "w") as f:
        json.dump({"epochs": 10, "batch_size": 32}, f)

    # 3. Create manifest
    manifest = {
        "contributor_id": "demo_contributor",
        "dataset_hash": hash_data(b"fake image data"), # simplistic
        "model_hash": hash_data(b"fake model data"),
        "version": "1.0.0"
    }

    manifest_bytes = json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode('utf-8')
    manifest_hash = hash_data(manifest_bytes)
    
    with open(os.path.join(pkg_dir, "manifest.json"), "w") as f:
        f.write(json.dumps(manifest, sort_keys=True, separators=(',', ':')))

    # 4. Sign manifest
    signature = sign_data(priv_key, manifest_bytes)
    with open(os.path.join(pkg_dir, "package.sig"), "wb") as f:
        f.write(signature)

    # 5. Zip it up
    zip_path = "data/demo_package.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pkg_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, pkg_dir)
                zipf.write(file_path, arcname)

    print(f"Created demo package at {zip_path}")
    
    # Cleanup temp dir
    shutil.rmtree(pkg_dir)

if __name__ == "__main__":
    create_demo_package()
