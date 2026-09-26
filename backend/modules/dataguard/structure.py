import os
import json
from typing import Dict, Any, List

def validate_coco_dataset(dataset_dir: str) -> Dict[str, Any]:
    findings = []
    is_valid = True
    
    annotations_dir = os.path.join(dataset_dir, "annotations")
    images_dir = os.path.join(dataset_dir, "images")
    
    if not os.path.exists(images_dir):
        findings.append("Missing 'images' directory")
        is_valid = False
        
    if not os.path.exists(annotations_dir):
        findings.append("Missing 'annotations' directory")
        is_valid = False
    
    # Check for instances json
    instances_path = os.path.join(annotations_dir, "instances.json")
    if not os.path.exists(instances_path):
        # Look for any json
        if os.path.exists(annotations_dir):
            jsons = [f for f in os.listdir(annotations_dir) if f.endswith('.json')]
            if not jsons:
                findings.append("No COCO annotation JSON found in annotations/")
                is_valid = False
            else:
                instances_path = os.path.join(annotations_dir, jsons[0])
    
    if is_valid and os.path.exists(instances_path):
        try:
            with open(instances_path, 'r') as f:
                coco_data = json.load(f)
                
            if "images" not in coco_data or "annotations" not in coco_data:
                findings.append("Invalid COCO format: missing 'images' or 'annotations' keys")
                is_valid = False
            else:
                image_ids = {img["id"] for img in coco_data["images"]}
                missing_images = 0
                for img in coco_data["images"]:
                    img_path = os.path.join(images_dir, img["file_name"])
                    if not os.path.exists(img_path):
                        missing_images += 1
                
                if missing_images > 0:
                    findings.append(f"{missing_images} images referenced in annotations are missing from disk")
                    is_valid = False
                    
        except json.JSONDecodeError:
            findings.append("Malformed JSON in annotations")
            is_valid = False
            
    return {
        "valid": is_valid,
        "format": "COCO",
        "findings": findings
    }

def validate_yolo_dataset(dataset_dir: str) -> Dict[str, Any]:
    findings = []
    is_valid = True
    
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")
    
    if not os.path.exists(images_dir):
        findings.append("Missing 'images' directory")
        is_valid = False
        
    if not os.path.exists(labels_dir):
        findings.append("Missing 'labels' directory")
        is_valid = False
        
    if is_valid:
        img_files = set(f.split('.')[0] for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg')))
        lbl_files = set(f.split('.')[0] for f in os.listdir(labels_dir) if f.endswith('.txt'))
        
        missing_labels = img_files - lbl_files
        if missing_labels:
            findings.append(f"{len(missing_labels)} images have no corresponding label files")
            
        missing_images = lbl_files - img_files
        if missing_images:
            findings.append(f"{len(missing_images)} label files have no corresponding images")
            is_valid = False
            
    return {
        "valid": is_valid,
        "format": "YOLO",
        "findings": findings
    }

def detect_dataset_format_and_validate(dataset_dir: str) -> Dict[str, Any]:
    if os.path.exists(os.path.join(dataset_dir, "annotations")):
        return validate_coco_dataset(dataset_dir)
    elif os.path.exists(os.path.join(dataset_dir, "labels")):
        return validate_yolo_dataset(dataset_dir)
    else:
        return {
            "valid": False,
            "format": "UNKNOWN",
            "findings": ["Dataset does not match COCO or YOLO structure"]
        }
