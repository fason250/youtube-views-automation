@echo off
echo 🚀 YouTube View Generator - Windows Setup
echo ==========================================
echo This script will install everything you need automatically!
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

:: Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ✅ pip found:
pip --version

:: Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created

:: Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

:: Upgrade pip
echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

:: Install dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

:: Test installation
echo.
echo 🧪 Testing installation...
python test_structure.py
if %errorlevel% neq 0 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)
echo ✅ Installation test passed

:: Create batch files for easy use
echo.
echo 📝 Creating easy-to-use scripts...

:: Create run_views.bat
echo @echo off > run_views.bat
echo call venv\Scripts\activate.bat >> run_views.bat
echo python run_simulation.py %%* >> run_views.bat

:: Create run_demo.bat
echo @echo off > run_demo.bat
echo call venv\Scripts\activate.bat >> run_demo.bat
echo python demo_dry_run.py >> run_demo.bat
echo pause >> run_demo.bat

echo ✅ User scripts created

echo.
echo 🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉
echo ==========================================
echo.
echo ✅ Everything is ready to use!
echo.
echo 📋 Quick Start Guide:
echo 1. Test the system:     run_demo.bat
echo 2. Generate views:      run_views.bat "YOUR_VIDEO_URL" VIEW_COUNT
echo.
echo 📝 Examples:
echo    run_views.bat "https://youtube.com/watch?v=abc123" 100
echo    run_views.bat "https://youtube.com/watch?v=abc123" 1000
echo.
echo 📊 The system will:
echo    • Use free proxies automatically (no payment needed)
echo    • Check that views are actually being counted
echo    • Use human-like behavior to avoid detection
echo    • Show progress and results in real-time
echo.
echo ⚠️  Important Notes:
echo    • Start with small numbers (100-500 views) for testing
echo    • Larger view counts take longer (this is intentional for safety)
echo    • The system prioritizes safety over speed
echo.
echo Press any key to exit...
pause >nul
