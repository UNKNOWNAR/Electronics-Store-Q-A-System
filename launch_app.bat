@echo off
echo 🛒 Electronics Store Q&A System Launcher
echo ========================================

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please create a virtual environment first:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r streamlit_requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Launch Streamlit app
echo 🚀 Launching Streamlit app...
echo 📱 The app will open in your default web browser
echo 🛑 Press Ctrl+C to stop the server
echo ========================================

python run_streamlit.py

pause
