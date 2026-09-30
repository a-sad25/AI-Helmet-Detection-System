import os
import sys
import tkinter as tk
from tkinter import messagebox

from app.camera import Camera
from app.detector import HelmetDetector
from app.violation_manager import ViolationManager
from app.statistics import Statistics
from app.ui import HelmetDetectionApp

# Configuration Constants
CONFIDENCE_THRESHOLD = 0.60
VIOLATION_FRAMES_THRESHOLD = 5
COOLDOWN_SECONDS = 10
# Robust model path handling for PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

def main():
    root = tk.Tk()
    root.withdraw() # Hide root while initializing components
    
    try:
        # Pre-flight check
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file '{MODEL_PATH}' not found.\n"
                "Please ensure it is in the project root directory before starting."
            )
            
        print("Initializing components...")
        
        # Initialize modules
        camera = Camera(camera_index=0)
        
        detector = HelmetDetector(
            model_path=MODEL_PATH, 
            conf_threshold=CONFIDENCE_THRESHOLD
        )
        
        violation_manager = ViolationManager(
            violation_frames_threshold=VIOLATION_FRAMES_THRESHOLD,
            cooldown_seconds=COOLDOWN_SECONDS
        )
        
        stats = Statistics()
        
        # Show main window and initialize UI
        root.deiconify() 
        app = HelmetDetectionApp(root, camera, detector, violation_manager, stats)
        
        print("Application started successfully.")
        
        # Start Tkinter event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Initialization Error", f"Failed to start application:\n\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
