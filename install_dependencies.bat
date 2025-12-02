@echo off
echo ========================================
echo Face Recognition Attendance System
echo Dependency Installation Script
echo ========================================
echo.

REM Upgrade pip, setuptools, and wheel
echo [1/6] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)
echo.

REM Install NumPy first
echo [2/6] Installing NumPy...
pip install "numpy>=1.24.0,<2.0.0"
if %errorlevel% neq 0 (
    echo ERROR: Failed to install NumPy
    pause
    exit /b 1
)
echo.

REM Install InsightFace from local wheel
echo [3/6] Installing InsightFace from local wheel file...
pip install insightface-0.7.3-cp311-cp311-win_amd64.whl
if %errorlevel% neq 0 (
    echo ERROR: Failed to install InsightFace
    echo Please ensure you have the wheel file in the current directory
    pause
    exit /b 1
)
echo.

REM Install OpenCV and Supervision
echo [4/6] Installing OpenCV and Supervision...
pip install opencv-python==4.8.1.78
pip install supervision==0.16.0
pip install onnxruntime==1.16.3
if %errorlevel% neq 0 (
    echo ERROR: Failed to install vision libraries
    pause
    exit /b 1
)
echo.

REM Install Flask and web dependencies
echo [5/6] Installing Flask and web dependencies...
pip install Flask==3.0.0
pip install Flask-Cors==4.0.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Flask
    pause
    exit /b 1
)
echo.

REM Install remaining dependencies
echo [6/6] Installing remaining dependencies...
pip install pyttsx3==2.90
pip install Pillow==10.1.0
pip install scikit-learn==1.3.2
if %errorlevel% neq 0 (
    echo ERROR: Failed to install remaining dependencies
    pause
    exit /b 1
)
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.

echo Verifying installations...
echo.

python -c "import numpy; print('✓ NumPy version:', numpy.__version__)"
python -c "import insightface; print('✓ InsightFace installed successfully')"
python -c "import cv2; print('✓ OpenCV version:', cv2.__version__)"
python -c "import flask; print('✓ Flask version:', flask.__version__)"
python -c "import supervision; print('✓ Supervision installed successfully')"

echo.
echo ========================================
echo All dependencies installed successfully!
echo You can now run: python main.py
echo ========================================
echo.

pause
