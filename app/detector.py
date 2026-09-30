import os
import cv2
from ultralytics import YOLO

class HelmetDetector:
    def __init__(self, model_path="best.pt", conf_threshold=0.60):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        # Load the pre-trained YOLO model
        self.model = YOLO(self.model_path)
        
    def detect(self, frame):
        """
        Run inference on the frame and draw bounding boxes.
        Returns the annotated frame and a list of detections.
        """
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        
        annotated_frame = frame.copy()
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Get confidence and class
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                # Class 0: helmet (safe), Class 1: no_helmet (violation)
                if cls == 0:
                    label_name = "helmet"
                    color = (0, 255, 0) # Green for helmet
                elif cls == 1:
                    label_name = "no_helmet"
                    color = (0, 0, 255) # Red for no_helmet
                else:
                    continue # Ignore unexpected class IDs
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label background and text
                label = f"{label_name} {conf:.2f}"
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(annotated_frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
                cv2.putText(annotated_frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                detections.append({
                    "class": cls,
                    "label": label_name,
                    "confidence": conf,
                    "bbox": (x1, y1, x2, y2)
                })
                
        return annotated_frame, detections
