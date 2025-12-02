# Face Recognition Attendance System - Installation Guide

## Quick Installation (Recommended)

### Method 1: Using requirements.txt (One Command Install)

This is the **easiest and recommended method** to install all dependencies at once.

#### Step 1: Ensure Python is Installed
Make sure you have Python 3.11 installed on your system.

```bash
python --version
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

#### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip setuptools wheel
```

#### Step 4: Install InsightFace (Special Case)
InsightFace requires a pre-built wheel file for Windows. Install it first:

```bash
pip install insightface-0.7.3-cp311-cp311-win_amd64.whl
```

**Note:** Make sure the `insightface-0.7.3-cp311-cp311-win_amd64.whl` file is in the current directory.

#### Step 5: Install All Other Dependencies
Now install all remaining dependencies with a single command:

```bash
pip install -r requirements.txt
```

That's it! All dependencies will be installed automatically.

---

## Method 2: Using the Batch Script (Windows Only)

If you prefer the automated batch script:

```bash
.\install_dependencies.bat
```

This script will:
1. Upgrade pip, setuptools, and wheel
2. Install NumPy
3. Install InsightFace from the wheel file
4. Install OpenCV and Supervision
5. Install Flask and web dependencies
6. Install remaining dependencies
7. Verify all installations

---

## Verification

After installation, verify that all packages are installed correctly:

```bash
# Check NumPy
python -c "import numpy; print('NumPy version:', numpy.__version__)"

# Check InsightFace
python -c "import insightface; print('InsightFace installed successfully')"

# Check OpenCV
python -c "import cv2; print('OpenCV version:', cv2.__version__)"

# Check Flask
python -c "import flask; print('Flask version:', flask.__version__)"

# Check Supervision
python -c "import supervision; print('Supervision installed successfully')"

# Check MySQL Connector
python -c "import mysql.connector; print('MySQL Connector installed successfully')"
```

---

## Dependencies List

The following packages will be installed:

### Core Dependencies
- **numpy** (>=1.24.0, <2.0.0) - Numerical computing

### Computer Vision & Face Recognition
- **opencv-python** (4.8.1.78) - Computer vision library
- **insightface** (0.7.3) - Face recognition (from wheel file)
- **onnxruntime** (1.16.3) - ONNX runtime for model inference
- **supervision** (0.16.0) - Computer vision utilities

### Web Framework
- **Flask** (3.0.0) - Web framework
- **Flask-Cors** (4.0.0) - CORS support for Flask

### Database
- **mysql-connector-python** (>=8.0.0) - MySQL database connector

### Image Processing
- **Pillow** (10.1.0) - Image processing library

### Machine Learning
- **scikit-learn** (1.3.2) - Machine learning utilities

### Text-to-Speech
- **pyttsx3** (2.90) - Text-to-speech conversion

---

## Troubleshooting

### Issue: InsightFace Installation Fails
**Solution:** Make sure you have the correct wheel file for your Python version and architecture. The provided wheel is for Python 3.11 on Windows (64-bit).

### Issue: MySQL Connector Fails
**Solution:** Ensure MySQL is installed on your system. You can also try:
```bash
pip install mysql-connector-python --upgrade
```

### Issue: OpenCV Import Error
**Solution:** Try reinstalling OpenCV:
```bash
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

### Issue: Permission Denied
**Solution:** Run the command prompt as Administrator or use:
```bash
pip install -r requirements.txt --user
```

---

## Running the Application

After successful installation, you can run the application using:

### CLI Mode
```bash
python main.py
```

### GUI Mode (Tkinter)
```bash
python modern_gui.py
```

### Web Server Mode (Flask)
```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

---

## System Requirements

- **Operating System:** Windows 10/11, Linux, or macOS
- **Python Version:** 3.11 (recommended)
- **RAM:** Minimum 4GB (8GB recommended)
- **Webcam:** Required for face capture and attendance
- **MySQL:** Required for database operations

---

## Additional Notes

1. **Virtual Environment:** Always use a virtual environment to avoid conflicts with other Python projects.

2. **GPU Support:** If you have an NVIDIA GPU, you can install CUDA-enabled ONNX Runtime for better performance:
   ```bash
   pip install onnxruntime-gpu
   ```

3. **Database Setup:** Make sure to configure your MySQL database settings in `config.py` before running the application.

4. **Face Encodings:** The system uses `face_encodings.pkl` to store registered faces. This file will be created automatically on first registration.

---

## Getting Help

If you encounter any issues:
1. Check the error message carefully
2. Verify all dependencies are installed correctly
3. Ensure your Python version is 3.11
4. Check that MySQL is running and accessible
5. Review the `config.py` file for correct configuration

---

**Happy Coding! 🚀**
