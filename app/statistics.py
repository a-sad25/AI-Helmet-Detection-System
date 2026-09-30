class Statistics:
    def __init__(self):
        self.total_helmet = 0
        self.total_no_helmet = 0
        self.confirmed_violations = 0
        
    def update(self, detections, new_violation_recorded):
        """
        Update the statistics counters based on detections.
        """
        for d in detections:
            if d["label"] == "helmet":
                self.total_helmet += 1
            elif d["label"] == "no_helmet":
                self.total_no_helmet += 1
                
        if new_violation_recorded:
            self.confirmed_violations += 1
            
    def get_helmet_detection_percentage(self):
        """
        Calculate the helmet detection ratio (based on frame/detection counts).
        """
        total = self.total_helmet + self.total_no_helmet
        if total == 0:
            return 100.0
        return (self.total_helmet / total) * 100.0
        
    def reset(self):
        """
        Reset all counters for a new session.
        """
        self.total_helmet = 0
        self.total_no_helmet = 0
        self.confirmed_violations = 0
