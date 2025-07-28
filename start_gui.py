#!/usr/bin/env python3
"""
Simple launcher for the GUI - handles setup automatically
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import selenium
        import yaml
        import requests
        return True
    except ImportError:
        return False

def run_setup():
    """Run the setup process"""
    try:
        if sys.platform.startswith('win'):
            # Windows
            result = subprocess.run(['setup.bat'], shell=True, capture_output=True, text=True)
        else:
            # Linux/Mac
            result = subprocess.run(['bash', 'setup.sh'], capture_output=True, text=True)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Setup failed: {e}")
        return False

def main():
    """Main launcher function"""
    print("🚀 YouTube View Generator Launcher")
    print("==================================")
    
    # Check if we're in the right directory
    if not os.path.exists("gui_app.py"):
        print("❌ Error: Please run this from the YouTube View Generator directory")
        input("Press Enter to exit...")
        return
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("📦 Dependencies not found. Running setup...")
        
        # Show setup dialog
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        result = messagebox.askyesno(
            "Setup Required",
            "This is your first time running the YouTube View Generator.\n\n"
            "The system needs to install some dependencies.\n"
            "This will take a few minutes.\n\n"
            "Continue with automatic setup?"
        )
        
        root.destroy()
        
        if not result:
            print("Setup cancelled by user")
            return
        
        print("Running automatic setup...")
        if not run_setup():
            print("❌ Setup failed. Please run setup manually:")
            if sys.platform.startswith('win'):
                print("   Double-click setup.bat")
            else:
                print("   Run: bash setup.sh")
            input("Press Enter to exit...")
            return
        
        print("✅ Setup completed successfully!")
    
    # Launch the GUI
    print("🎬 Starting GUI...")
    try:
        if sys.platform.startswith('win'):
            # Windows - use pythonw to avoid console window
            subprocess.run([sys.executable, 'gui_app.py'])
        else:
            # Linux/Mac
            subprocess.run([sys.executable, 'gui_app.py'])
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
