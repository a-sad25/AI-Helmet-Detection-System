import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import os
import subprocess
import platform

class HelmetDetectionApp:
    def __init__(self, root, camera, detector, violation_manager, stats):
        self.root = root
        self.root.title("Helmet Detection System")
        self.root.geometry("1200x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.camera = camera
        self.detector = detector
        self.violation_manager = violation_manager
        self.stats = stats
        
        self.is_processing = False
        self.after_id = None
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Main layout configuration
        self.main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side: Video Feed
        self.video_frame = ttk.LabelFrame(self.main_frame, text=" Live Camera Feed ", padding=10)
        self.main_frame.add(self.video_frame, weight=4)
        
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right side: Control and Stats
        self.control_frame = ttk.Frame(self.main_frame, padding=10)
        self.main_frame.add(self.control_frame, weight=1)
        
        # Statistics Panel
        self.stats_group = ttk.LabelFrame(self.control_frame, text=" Statistics Session Summary ", padding=10)
        self.stats_group.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.stats_group, text="Helmet Detections:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.lbl_helmets = ttk.Label(self.stats_group, text="0", font=("Arial", 10, "bold"))
        self.lbl_helmets.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
        
        ttk.Label(self.stats_group, text="No-Helmet Detections:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.lbl_no_helmets = ttk.Label(self.stats_group, text="0", font=("Arial", 10, "bold"))
        self.lbl_no_helmets.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)
        
        ttk.Label(self.stats_group, text="Confirmed Violations:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.lbl_violations = ttk.Label(self.stats_group, text="0", foreground="red", font=("Arial", 10, "bold"))
        self.lbl_violations.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        
        ttk.Label(self.stats_group, text="Helmet Detection %:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.lbl_compliance = ttk.Label(self.stats_group, text="100.0%", font=("Arial", 10, "bold"))
        self.lbl_compliance.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)
        
        # Current Status Panel
        self.status_group = ttk.LabelFrame(self.control_frame, text=" Live Detection Status ", padding=10)
        self.status_group.pack(fill=tk.X, pady=(0, 20))
        
        self.lbl_current_status = ttk.Label(self.status_group, text="Standby", font=("Arial", 16, "bold"))
        self.lbl_current_status.pack(pady=15)
        
        # Controls Panel
        self.controls_group = ttk.LabelFrame(self.control_frame, text=" System Controls ", padding=10)
        self.controls_group.pack(fill=tk.X, pady=(0, 20))
        
        self.btn_start = ttk.Button(self.controls_group, text="Start Camera", command=self.start_camera)
        self.btn_start.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_stop = ttk.Button(self.controls_group, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.btn_stop.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_reset = ttk.Button(self.controls_group, text="Reset Statistics", command=self.reset_stats)
        self.btn_reset.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_folder = ttk.Button(self.controls_group, text="Open Violations Folder", command=self.open_folder)
        self.btn_folder.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_exit = ttk.Button(self.controls_group, text="Exit", command=self.on_closing)
        self.btn_exit.pack(fill=tk.X, padx=5, pady=5)
        
    def update_stats_ui(self):
        self.lbl_helmets.config(text=str(self.stats.total_helmet))
        self.lbl_no_helmets.config(text=str(self.stats.total_no_helmet))
        self.lbl_violations.config(text=str(self.stats.confirmed_violations))
        self.lbl_compliance.config(text=f"{self.stats.get_helmet_detection_percentage():.1f}%")
        
    def start_camera(self):
        try:
            self.camera.start()
            self.is_processing = True
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.lbl_current_status.config(text="Camera Active", foreground="green")
            self.process_video()
        except Exception as e:
            messagebox.showerror("Camera Error", str(e))
            
    def stop_camera(self):
        if not self.is_processing:
            return
            
        self.is_processing = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
            
        self.camera.stop()
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.lbl_current_status.config(text="Standby", foreground="black")
        self.canvas.delete("all")
        
        # Show Session Summary
        messagebox.showinfo(
            "SESSION SUMMARY",
            f"Helmet detections: {self.stats.total_helmet}\n"
            f"No-helmet detections: {self.stats.total_no_helmet}\n"
            f"Confirmed violations: {self.stats.confirmed_violations}"
        )
        
    def process_video(self):
        if not self.is_processing:
            return
            
        frame = self.camera.get_frame()
        if frame is not None:
            try:
                # Run detection on the frame
                annotated_frame, detections = self.detector.detect(frame)
                
                # Check for temporal violations and record if necessary
                new_violation = self.violation_manager.process_detections(annotated_frame, detections)
                
                # Update statistics
                self.stats.update(detections, new_violation)
                self.update_stats_ui()
                
                # Update current status
                has_no_helmet = any(d["label"] == "no_helmet" for d in detections)
                if has_no_helmet:
                    self.lbl_current_status.config(text="VIOLATION DETECTED", foreground="red")
                else:
                    self.lbl_current_status.config(text="Safe", foreground="green")
                
                # Convert the frame from BGR to RGB for Tkinter display
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                
                # Resize image to fit canvas while maintaining aspect ratio
                canvas_w = self.canvas.winfo_width()
                canvas_h = self.canvas.winfo_height()
                
                if canvas_w > 10 and canvas_h > 10:
                    img.thumbnail((canvas_w, canvas_h), Image.Resampling.LANCZOS)
                    
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(canvas_w//2, canvas_h//2, anchor=tk.CENTER, image=imgtk)
                self.canvas.imgtk = imgtk # Keep a reference to prevent garbage collection
                
            except Exception as e:
                print(f"Error processing frame: {e}")
                
        # Schedule the next frame check
        self.after_id = self.root.after(30, self.process_video)
        
    def reset_stats(self):
        self.stats.reset()
        self.update_stats_ui()
        
    def open_folder(self):
        path = os.path.abspath(self.violation_manager.violations_dir)
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
            
    def on_closing(self):
        self.stop_camera()
        self.root.destroy()
