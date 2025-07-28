@echo off
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python demo_dry_run.py
pause
