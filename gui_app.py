#!/usr/bin/env python3
"""
Simple GUI for YouTube View Generator - Easy for non-technical users
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import os
import subprocess
import queue
import time

class ViewGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube View Generator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Queue for thread communication
        self.message_queue = queue.Queue()
        
        # Variables
        self.is_running = False
        self.process = None
        
        self.setup_ui()
        self.check_queue()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube View Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # View count input
        ttk.Label(main_frame, text="Number of Views:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.views_var = tk.StringVar(value="100")
        views_entry = ttk.Entry(main_frame, textvariable=self.views_var, width=20)
        views_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Quick select buttons
        quick_frame = ttk.Frame(main_frame)
        quick_frame.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Button(quick_frame, text="100", width=8, 
                  command=lambda: self.views_var.set("100")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="500", width=8,
                  command=lambda: self.views_var.set("500")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="1000", width=8,
                  command=lambda: self.views_var.set("1000")).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="5000", width=8,
                  command=lambda: self.views_var.set("5000")).pack(side=tk.LEFT, padx=2)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Generating Views", 
                                      command=self.start_generation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self.stop_generation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📊 Run Demo", 
                  command=self.run_demo).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready to start")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=5, column=0, columnspan=2, pady=10)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Log output
        ttk.Label(main_frame, text="Output Log:").grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.log_text.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(8, weight=1)
        
        # Initial log message
        self.log_message("Welcome to YouTube View Generator!")
        self.log_message("1. Enter a YouTube URL")
        self.log_message("2. Choose number of views")
        self.log_message("3. Click 'Start Generating Views'")
        self.log_message("")
        self.log_message("💡 Tip: Start with small numbers (100-500) for testing")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Validate user inputs"""
        url = self.url_var.get().strip()
        views_str = self.views_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return False
        
        if "youtube.com" not in url and "youtu.be" not in url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return False
        
        try:
            views = int(views_str)
            if views <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of views (positive integer)")
            return False
        
        if views > 10000:
            result = messagebox.askyesno("Warning", 
                f"You requested {views} views. This will take a long time.\n"
                "Are you sure you want to continue?")
            if not result:
                return False
        
        return True
    
    def start_generation(self):
        """Start view generation in a separate thread"""
        if not self.validate_inputs():
            return
        
        if self.is_running:
            messagebox.showwarning("Warning", "View generation is already running!")
            return
        
        # Update UI
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.progress_var.set("Starting view generation...")
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Start generation in separate thread
        url = self.url_var.get().strip()
        views = int(self.views_var.get().strip())
        
        thread = threading.Thread(target=self.run_generation, args=(url, views))
        thread.daemon = True
        thread.start()
    
    def run_generation(self, url, views):
        """Run the actual view generation"""
        try:
            self.message_queue.put(f"🚀 Starting generation of {views} views for: {url}")
            
            # Run the main script
            cmd = [sys.executable, "run_simulation.py", url, str(views)]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output line by line
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.message_queue.put(line.strip())
            
            self.process.wait()
            
            if self.process.returncode == 0:
                self.message_queue.put("✅ View generation completed successfully!")
            else:
                self.message_queue.put("❌ View generation failed. Check the log above.")
                
        except Exception as e:
            self.message_queue.put(f"❌ Error: {str(e)}")
        finally:
            self.message_queue.put("FINISHED")
    
    def stop_generation(self):
        """Stop the running generation"""
        if self.process:
            self.process.terminate()
            self.log_message("🛑 Stopping view generation...")
        
        self.finish_generation()
    
    def run_demo(self):
        """Run the demo"""
        if self.is_running:
            messagebox.showinfo("Info", "Please wait for current operation to finish")
            return
        
        self.log_text.delete(1.0, tk.END)
        self.log_message("🎬 Running demo...")
        
        thread = threading.Thread(target=self.run_demo_thread)
        thread.daemon = True
        thread.start()
    
    def run_demo_thread(self):
        """Run demo in separate thread"""
        try:
            cmd = [sys.executable, "demo_dry_run.py"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.message_queue.put(line.strip())
            
            process.wait()
            self.message_queue.put("✅ Demo completed!")
            
        except Exception as e:
            self.message_queue.put(f"❌ Demo error: {str(e)}")
    
    def finish_generation(self):
        """Clean up after generation finishes"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_var.set("Ready to start")
        self.process = None
    
    def check_queue(self):
        """Check for messages from worker threads"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                if message == "FINISHED":
                    self.finish_generation()
                else:
                    self.log_message(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)

def main():
    """Main function"""
    # Check if we're in the right directory
    if not os.path.exists("run_simulation.py"):
        messagebox.showerror("Error", 
            "Please run this GUI from the YouTube View Generator directory\n"
            "(The directory containing run_simulation.py)")
        return
    
    root = tk.Tk()
    app = ViewGeneratorGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
