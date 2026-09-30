import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        
    def start(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise RuntimeError(f"Could not open webcam with index {self.camera_index}")
            
    def stop(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            
    def get_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
        
    def is_running(self):
        return self.cap is not None and self.cap.isOpened()
