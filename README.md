# Helmet Detection System

## Objective
This is a vocational training project that implements a real-time Helmet Detection System. It uses a custom-trained YOLO11n object-detection model to identify whether a person in a video feed is wearing a helmet or not. The system captures screenshots of violations and maintains a log for compliance monitoring.

## Technology Stack
- **Python 3**
- **Ultralytics YOLO** (Object Detection)
- **OpenCV** (Video capture and image processing)
- **Pandas** (Logging to CSV)
- **Tkinter** (Desktop UI)
- **Pillow** (Image rendering in UI)

## Model and Classes
The model (`best.pt`) is a custom-trained YOLO11n network.

**Classes:**
- `0 = helmet` (Displayed as a positive/safe detection in Green)
- `1 = no_helmet` (Displayed as a violation in Red)

## Training and Metrics
The model was trained on a custom dataset. The evaluation on a completely held-out test set (409 images) yielded the following metrics:
- **Precision:** 84.4%
- **Recall:** 87.7%
- **mAP@50:** 92.6%
- **mAP@50-95:** 63.2%

## Installation

1. Clone or download the repository.
2. Ensure you have Python installed (Python 3.8+ recommended).
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure your webcam is connected.
5. Ensure `best.pt` is located in the root directory of the project.

## How to Run
Run the main script from the root directory:
```bash
python main.py
```

## Controls
- **Start Camera:** Initializes the webcam and starts real-time detection.
- **Stop Camera:** Stops the video feed and halts detection.
- **Reset Statistics:** Clears the current session's detection counts and compliance rate.
- **Open Violations Folder:** Opens the directory where violation screenshots are saved.
- **Exit:** Closes the application.

## Project Structure
```text
helmet-detection-system/
│
├── best.pt                  # Trained YOLO11n weights
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
├── README.md                # Documentation
├── .gitignore               # Git exclusions
│
├── app/                     # Source code modules
│   ├── __init__.py
│   ├── camera.py            # Webcam interface
│   ├── detector.py          # YOLO inference
│   ├── statistics.py        # Detection counting and compliance
│   ├── ui.py                # Tkinter graphical interface
│   └── violation_manager.py # Violation logic and logging
│
├── violations/              # Saved screenshots of violations
└── logs/                    # CSV logs of violations
```

## Limitations
- Performance depends heavily on the local machine's CPU/GPU capabilities. Real-time inference without a discrete GPU may have lower frame rates.
- The system uses a simple temporal confirmation mechanism (e.g., 5 consecutive frames) for violation reporting, meaning brief occlusions could reset the violation counter.
- Hardcoded to use `camera_index=0`. If multiple cameras are attached, this might need to be changed in the code.
