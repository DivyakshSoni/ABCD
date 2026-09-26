import os
import shutil
import json
import random
from typing import Dict, Any

def inject_duplicate_flood(dataset_dir: str, output_dir: str, rate: float = 0.05) -> Dict[str, Any]:
    """
    Creates a controlled duplicate flooding attack for testing DataGuard.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Copy dataset
    if os.path.exists(os.path.join(output_dir, "images")):
        shutil.rmtree(output_dir)
    shutil.copytree(dataset_dir, output_dir)
    
    images_dir = os.path.join(output_dir, "images")
    if not os.path.exists(images_dir):
        return {"status": "FAILED", "message": "No images directory to infect"}
        
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    num_to_inject = max(1, int(len(image_files) * rate))
    
    injected_records = []
    
    for i in range(num_to_inject):
        src_image = random.choice(image_files)
        src_path = os.path.join(images_dir, src_image)
        
        dup_name = f"redforge_dup_{i}_{src_image}"
        dup_path = os.path.join(images_dir, dup_name)
        
        shutil.copy2(src_path, dup_path)
        injected_records.append({"source": src_image, "duplicate": dup_name})
        
    manifest = {
        "attack": "duplicate_flood",
        "rate": rate,
        "num_injected": num_to_inject,
        "records": injected_records
    }
    
    manifest_path = os.path.join(output_dir, "redforge_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
        
    return {
        "status": "SUCCESS",
        "attack": "duplicate_flood",
        "num_injected": num_to_inject,
        "manifest": manifest_path
    }
