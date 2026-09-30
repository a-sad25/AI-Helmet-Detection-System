import os
import cv2
import time
from datetime import datetime
import pandas as pd

class ViolationManager:
    def __init__(self, violation_frames_threshold=5, cooldown_seconds=10):
        """
        Manages the temporal confirmation of no-helmet violations.
        - violation_frames_threshold: Consecutive frames needed to confirm a violation
        - cooldown_seconds: Time to wait before recording another violation
        """
        self.violation_frames_threshold = violation_frames_threshold
        self.cooldown_seconds = cooldown_seconds
        
        self.consecutive_no_helmet_frames = 0
        self.last_violation_time = 0
        self.violation_active = False
        
        self.violations_dir = "violations"
        self.logs_dir = "logs"
        self.csv_path = os.path.join(self.logs_dir, "violations.csv")
        
        self._ensure_directories()
        self._ensure_csv()
        
    def _ensure_directories(self):
        os.makedirs(self.violations_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
    def _ensure_csv(self):
        if not os.path.exists(self.csv_path):
            df = pd.DataFrame(columns=["timestamp", "status", "confidence", "screenshot_filename"])
            df.to_csv(self.csv_path, index=False)
            
    def process_detections(self, frame, detections):
        """
        Check for no_helmet detections and trigger violation if necessary.
        Returns a boolean indicating if a NEW violation was recorded in this frame.
        """
        has_no_helmet = any(d["label"] == "no_helmet" for d in detections)
        
        if has_no_helmet:
            self.consecutive_no_helmet_frames += 1
        else:
            self.consecutive_no_helmet_frames = 0
            self.violation_active = False
            
        # Check temporal confirmation
        if self.consecutive_no_helmet_frames >= self.violation_frames_threshold:
            if not self.violation_active:
                current_time = time.time()
                
                # Check cooldown period
                if (current_time - self.last_violation_time) >= self.cooldown_seconds:
                    # Find the most confident no_helmet detection
                    no_helmet_dets = [d for d in detections if d["label"] == "no_helmet"]
                    best_det = max(no_helmet_dets, key=lambda x: x["confidence"])
                    
                    self._record_violation(frame, best_det["confidence"])
                    
                    self.last_violation_time = current_time
                    self.violation_active = True
                    return True
                
        return False
        
    def _record_violation(self, frame, confidence):
        """
        Capture screenshot and log violation to CSV.
        """
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        filename = f"violation_{timestamp_str}.jpg"
        filepath = os.path.join(self.violations_dir, filename)
        
        # Save screenshot
        cv2.imwrite(filepath, frame)
        
        # Log to CSV
        new_row = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "no_helmet",
            "confidence": f"{confidence:.2f}",
            "screenshot_filename": filename
        }
        
        df = pd.DataFrame([new_row])
        df.to_csv(self.csv_path, mode='a', header=False, index=False)
