# AI Helmet Detection System

A real-time desktop application that uses a custom-trained **YOLO11n** model to detect whether people are wearing helmets through a webcam.

The application provides:
- Real-time helmet / no-helmet detection
- Bounding boxes with confidence scores
- Violation detection and screenshot capture
- CSV-based violation logging
- Session statistics and compliance information
- A Tkinter desktop interface

## Tech Stack

- Python 3
- Ultralytics YOLO
- OpenCV
- Pandas
- Pillow
- Tkinter

## Project Requirements

This guide is intended for running the project on a **new Windows PC**.

### Minimum requirements

- Windows 10 or Windows 11
- Python 3.8 or newer
- A working webcam
- Internet connection for installing Python packages
- At least 2 GB of free disk space is recommended
- The application can run on CPU; a compatible NVIDIA GPU can improve inference speed

> **Important:** Python must be added to PATH during installation.

---

# 1. Install Python

Download and install Python from:

https://www.python.org/downloads/

During installation, make sure to enable:

**Add Python.exe to PATH**

After installation, open **Command Prompt** or **PowerShell** and verify:

```bash
python --version
```

You should see something similar to:

```text
Python 3.x.x
```

If `python` does not work, try:

```bash
py --version
```

---

# 2. Download the Project

### Option A — Clone using Git

Install Git if it is not already installed:

https://git-scm.com/downloads

Then open Command Prompt / PowerShell and run:

```bash
git clone https://github.com/a-sad25/AI-Helmet-Detection-System.git
cd AI-Helmet-Detection-System
```

### Option B — Download ZIP

1. Open the repository:
   https://github.com/a-sad25/AI-Helmet-Detection-System
2. Click **Code → Download ZIP**
3. Extract the ZIP file
4. Open a terminal inside the extracted project folder

You should see files such as:

```text
AI-Helmet-Detection-System/
├── app/
├── best.pt
├── main.py
└── requirements.txt
```

---

# 3. Create a Virtual Environment

Creating a virtual environment keeps this project's Python packages separate from other projects.

Run:

```bash
python -m venv venv
```

Activate it:

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Command Prompt

```cmd
venv\Scripts\activate
```

After activation, your terminal should show something similar to:

```text
(venv) C:\...\AI-Helmet-Detection-System>
```

### If PowerShell blocks activation

Run PowerShell as a normal user and execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 4. Install Dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The required Python packages are:

- `ultralytics`
- `opencv-python`
- `pandas`
- `Pillow`

Tkinter is normally included with the standard Windows Python installation.

The first installation may take some time because Ultralytics also installs its required deep-learning dependencies.

---

# 5. Verify the Model File

The trained YOLO model is already included in the repository:

```text
best.pt
```

It **must remain in the project root**, alongside `main.py`:

```text
AI-Helmet-Detection-System/
├── app/
├── best.pt        ← required
├── main.py
└── requirements.txt
```

Do not move or rename `best.pt`.

The application checks for this file automatically before starting.

---

# 6. Connect a Webcam

Connect the webcam before starting the application.

The project currently uses:

```text
camera_index = 0
```

This normally means the computer's default webcam.

If the PC has multiple cameras and the wrong camera opens, the camera index can be changed in:

```text
main.py
```

For example:

```python
camera = Camera(camera_index=1)
```

Try `0`, `1`, or another available camera index.

---

# 7. Allow Camera Access in Windows

If the application cannot access the webcam:

1. Open **Windows Settings**
2. Go to **Privacy & security → Camera**
3. Turn on **Camera access**
4. Turn on **Let desktop apps access your camera**

Also close applications such as:

- Zoom
- Google Meet
- Microsoft Teams
- OBS
- Camera app

These applications may already be using the webcam.

---

# 8. Run the Application

From the project root, with the virtual environment activated:

```bash
python main.py
```

The desktop application should open.

Click:

**Start Camera**

to begin real-time helmet detection.

---

# 9. Using the Application

### Start Camera
Starts the webcam and begins YOLO inference.

### Stop Camera
Stops the webcam and detection process.

### Reset Statistics
Resets the current session's detection statistics.

### Open Violations Folder
Opens the folder containing captured violation screenshots.

### Exit
Closes the application.

---

# 10. How Detection Works

The included `best.pt` model contains two classes:

| Class ID | Class | Meaning |
|---|---|---|
| 0 | `helmet` | Helmet detected / safe |
| 1 | `no_helmet` | No helmet detected / violation |

The application uses a confidence threshold of:

```text
0.60
```

A violation is confirmed after the configured number of consecutive frames, helping reduce false alerts from brief detection errors.

---

# 11. Output Files

When violations are detected, the application can create output folders such as:

```text
violations/
logs/
```

These contain the generated violation screenshots and CSV logs.

These folders may not exist until the application records its first violation.

---

# 12. Project Structure

```text
AI-Helmet-Detection-System/
│
├── app/
│   ├── __init__.py
│   ├── camera.py
│   ├── detector.py
│   ├── statistics.py
│   ├── ui.py
│   └── violation_manager.py
│
├── best.pt                  # Trained YOLO model
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── README.md
└── .gitignore
```

---

# 13. Troubleshooting

## `python` is not recognized

Try:

```bash
py --version
```

If that works, use `py` instead of `python`:

```bash
py -m venv venv
py -m pip install -r requirements.txt
py main.py
```

If neither works, reinstall Python and enable **Add Python.exe to PATH**.

---

## `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'ultralytics'
```

Make sure the virtual environment is active, then run:

```bash
pip install -r requirements.txt
```

---

## Model not found

If you see an error saying `best.pt` was not found, make sure:

```text
best.pt
```

is in the same folder as:

```text
main.py
```

---

## Webcam could not be opened

Check that:

- The webcam is connected.
- Windows Camera access is enabled.
- Another application is not using the webcam.
- The correct camera index is being used.

You can change the index in `main.py`:

```python
camera = Camera(camera_index=0)
```

---

## Detection is slow

The model can run on CPU, but inference speed depends on the PC.

For better performance:

- Close unnecessary applications.
- Use a PC with a stronger CPU.
- Use a compatible NVIDIA GPU if available.

Lower FPS on a CPU-only machine is normal.

---

## PowerShell will not activate the virtual environment

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

Alternatively, use Command Prompt:

```cmd
venv\Scripts\activate
```

---

# 14. Recommended Quick Setup

For a fresh Windows PC, the shortest setup is:

```bash
git clone https://github.com/a-sad25/AI-Helmet-Detection-System.git
cd AI-Helmet-Detection-System

python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py
```

Then click **Start Camera**.

---

# 15. Model Information

The repository includes a custom-trained YOLO11n model.

Evaluation on the held-out test set:

- **Precision:** 84.4%
- **Recall:** 87.7%
- **mAP@50:** 92.6%
- **mAP@50-95:** 63.2%

These metrics describe the model's evaluation performance and may differ from real-world performance depending on lighting, camera quality, viewing angle, distance, and environment.

---

## Author

**Asad Aman**

GitHub: https://github.com/a-sad25
