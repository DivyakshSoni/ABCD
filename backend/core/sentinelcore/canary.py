from typing import Dict, Any

class DetectorRegistry:
    def __init__(self):
        self.detectors = {}
        
    def register(self, detector_id: str, name: str, architecture: str):
        self.detectors[detector_id] = {
            "name": name,
            "architecture": architecture,
            "health_state": "NOT_TESTED",
            "last_test": None
        }
        
    def run_canary(self, detector_id: str, canary_func) -> bool:
        """
        Runs a predefined canary test for a detector.
        If it fails, marks the detector as UNRELIABLE.
        """
        if detector_id not in self.detectors:
            return False
            
        try:
            passed = canary_func()
            if passed:
                self.detectors[detector_id]["health_state"] = "HEALTHY"
            else:
                self.detectors[detector_id]["health_state"] = "UNRELIABLE"
            return passed
        except Exception:
            self.detectors[detector_id]["health_state"] = "FAILED"
            return False

# Global registry for MVP
registry = DetectorRegistry()
