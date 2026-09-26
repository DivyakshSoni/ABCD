import os
import torch
from torchvision import transforms
from PIL import Image
from typing import Dict, Any

def behavioral_fingerprint(model_path: str, probes_dir: str) -> Dict[str, Any]:
    if not os.path.exists(model_path):
        return {"status": "UNAVAILABLE", "message": "Model artifact not found"}
        
    if not os.path.exists(probes_dir):
        return {"status": "UNAVAILABLE", "message": "Probes directory not found"}

    try:
        # MVP: Attempt to load via torch.jit
        model = torch.jit.load(model_path)
        model.eval()
    except Exception as e:
        return {
            "status": "LIMITED_COVERAGE", 
            "message": f"Could not load model as TorchScript. {str(e)}"
        }
        
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    results = {}
    probe_files = [f for f in os.listdir(probes_dir) if f.lower().endswith(('.jpg', '.png'))]
    
    if not probe_files:
        return {"status": "UNAVAILABLE", "message": "No probe images found"}

    with torch.no_grad():
        for probe_file in probe_files:
            img_path = os.path.join(probes_dir, probe_file)
            try:
                img = Image.open(img_path).convert('RGB')
                tensor = transform(img).unsqueeze(0)
                output = model(tensor)
                # Just take the argmax or top-k as the fingerprint for MVP
                pred = torch.argmax(output, dim=1).item()
                results[probe_file] = pred
            except Exception as e:
                results[probe_file] = f"ERROR: {str(e)}"
                
    return {
        "status": "COMPLETED",
        "access_level": "BLACK_BOX",
        "fingerprint": results,
        "message": "Behavioral fingerprint generated from reference probes."
    }
