import os
import imagehash
from PIL import Image
from typing import Dict, Any, List

def find_duplicates_phash(dataset_dir: str, threshold: int = 5) -> Dict[str, Any]:
    """
    Finds near-duplicates using perceptual hashing (pHash).
    Returns a dictionary of duplicate clusters.
    """
    images_dir = os.path.join(dataset_dir, "images")
    if not os.path.exists(images_dir):
        return {"clusters": [], "message": "No images directory found"}
        
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    hashes = {}
    clusters = []
    visited = set()
    
    # Calculate hashes
    for img_file in image_files:
        try:
            img_path = os.path.join(images_dir, img_file)
            with Image.open(img_path) as img:
                hash_val = imagehash.phash(img)
                hashes[img_file] = hash_val
        except Exception as e:
            continue
            
    # Find clusters
    files_list = list(hashes.keys())
    for i in range(len(files_list)):
        f1 = files_list[i]
        if f1 in visited:
            continue
            
        cluster = [f1]
        visited.add(f1)
        h1 = hashes[f1]
        
        for j in range(i + 1, len(files_list)):
            f2 = files_list[j]
            if f2 in visited:
                continue
                
            h2 = hashes[f2]
            # Hamming distance
            diff = h1 - h2
            if diff <= threshold:
                cluster.append(f2)
                visited.add(f2)
                
        if len(cluster) > 1:
            clusters.append(cluster)
            
    return {
        "num_clusters": len(clusters),
        "clusters": clusters,
        "message": f"Found {len(clusters)} potential duplicate/near-duplicate groups."
    }
