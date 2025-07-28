#!/usr/bin/env python3
"""
Simple Browser Opener - No Hanging
Just opens browsers to YouTube URLs - simple and reliable
"""

import subprocess
import time
import sys
import os
import threading

class SimpleBrowserOpener:
    def __init__(self):
        self.opened_count = 0
        
    def open_browser_simple(self, url, browser_number):
        """Open browser using system command - much more reliable"""
        try:
            print(f"🌐 Opening browser {browser_number}...")
            
            # Try different browser commands
            browser_commands = [
                ['google-chrome', url],
                ['chromium-browser', url], 
                ['firefox', url],
                ['xdg-open', url]  # Generic Linux opener
            ]
            
            success = False
            for cmd in browser_commands:
                try:
                    # Open browser in background
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"   ✅ Browser {browser_number} opened with {cmd[0]}")
                    success = True
                    break
                except FileNotFoundError:
                    continue
            
            if not success:
                print(f"   ❌ No browser found for browser {browser_number}")
                return False
            
            self.opened_count += 1
            return True
            
        except Exception as e:
            print(f"   ❌ Browser {browser_number} failed: {e}")
            return False
    
    def open_multiple_browsers(self, url, count, delay_between=2):
        """Open multiple browsers with delays"""
        print(f"🚀 Opening {count} browsers to: {url}")
        print(f"⏱️  Delay between browsers: {delay_between} seconds")
        print()
        
        for i in range(count):
            print(f"--- Browser {i+1}/{count} ---")
            
            success = self.open_browser_simple(url, i+1)
            
            if success:
                print(f"✅ Browser {i+1} opened successfully")
            else:
                print(f"❌ Browser {i+1} failed")
            
            # Wait between browsers (except last one)
            if i < count - 1:
                print(f"⏳ Waiting {delay_between} seconds...")
                time.sleep(delay_between)
                print()
        
        print(f"\n🎉 Finished! Opened {self.opened_count}/{count} browsers")
        print("💡 Check your screen - browsers should be visible")
        print("🔄 Close browsers manually when done")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 simple_browser.py <youtube_url> <count> [delay]")
        print("\nExamples:")
        print("  python3 simple_browser.py 'https://youtube.com/shorts/abc123' 3")
        print("  python3 simple_browser.py 'https://youtube.com/watch?v=abc123' 5 1")
        print("\nArguments:")
        print("  youtube_url : The YouTube URL to open")
        print("  count       : Number of browsers to open")
        print("  delay       : Seconds between each browser (default: 2)")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        count = int(sys.argv[2])
    except ValueError:
        print("❌ Count must be a number")
        sys.exit(1)
    
    # Optional delay parameter
    delay = 2
    if len(sys.argv) > 3:
        try:
            delay = int(sys.argv[3])
        except ValueError:
            print("❌ Delay must be a number")
            sys.exit(1)
    
    print("🌐 Simple Browser Opener")
    print("=" * 40)
    print(f"📺 URL: {url}")
    print(f"🔢 Count: {count}")
    print(f"⏱️  Delay: {delay} seconds")
    print()
    
    opener = SimpleBrowserOpener()
    opener.open_multiple_browsers(url, count, delay)

if __name__ == "__main__":
    main()
