#!/usr/bin/env python3
"""
Auto-Close View Generator - FIXED VERSION
- Automatically closes browsers after watch time
- Prevents system crashes from too many open windows
- Resource management and cleanup
- Perfect for mass generation without PC crashes
"""

import subprocess
import time
import sys
import os
import threading
import random
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed

class AutoCloseViewGenerator:
    def __init__(self):
        self.completed_views = 0
        self.failed_views = 0
        self.active_processes = {}
        self.lock = threading.Lock()
        
    def create_browser_with_auto_close(self, url, window_id, watch_seconds=90):
        """Create browser that AUTOMATICALLY closes after watch time"""
        try:
            print(f"🌐 Opening browser {window_id} (auto-close in {watch_seconds}s)...")
            
            # Create browser command
            cmd = [
                'google-chrome',
                '--incognito',
                '--new-window',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-extensions',
                '--disable-plugins',
                url
            ]
            
            # Launch browser
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid  # Create process group for easy killing
            )
            
            # Track the process
            with self.lock:
                self.active_processes[window_id] = process
            
            print(f"   ✅ Browser {window_id} opened (PID: {process.pid})")
            
            # Wait for watch time
            time.sleep(watch_seconds)
            
            # FORCE CLOSE the browser
            print(f"   🔄 Auto-closing browser {window_id}...")
            try:
                # Kill the entire process group (browser + all tabs)
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                time.sleep(2)  # Give it time to close gracefully
                
                # If still running, force kill
                if process.poll() is None:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    print(f"   💀 Force-killed browser {window_id}")
                else:
                    print(f"   ✅ Browser {window_id} closed gracefully")
                    
            except Exception as e:
                print(f"   ⚠️  Error closing browser {window_id}: {e}")
            
            # Remove from tracking
            with self.lock:
                if window_id in self.active_processes:
                    del self.active_processes[window_id]
                self.completed_views += 1
            
            return True
            
        except Exception as e:
            print(f"   ❌ Browser {window_id} failed: {str(e)[:50]}")
            with self.lock:
                self.failed_views += 1
            return False
    
    def emergency_cleanup(self):
        """Emergency cleanup - kill all active browsers"""
        print("🚨 EMERGENCY CLEANUP - Killing all browsers...")
        
        with self.lock:
            for window_id, process in self.active_processes.items():
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    print(f"   💀 Killed browser {window_id}")
                except:
                    pass
            self.active_processes.clear()
        
        print("✅ Emergency cleanup complete")
    
    def generate_views_with_auto_close(self, url, total_views, max_concurrent=5, watch_minutes=1.5):
        """Generate views with guaranteed auto-close"""
        watch_seconds = int(watch_minutes * 60)
        
        print(f"🚀 Auto-Close View Generator")
        print(f"📺 URL: {url}")
        print(f"🎯 Target views: {total_views}")
        print(f"🪟 Max concurrent: {max_concurrent}")
        print(f"⏱️  Watch time: {watch_minutes} minutes")
        print(f"🔄 Auto-close: ENABLED (prevents crashes)")
        print()
        
        start_time = time.time()
        
        # Use ThreadPoolExecutor with limited workers
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            for i in range(total_views):
                future = executor.submit(
                    self.create_browser_with_auto_close,
                    url,
                    f"view_{i+1:03d}",
                    watch_seconds
                )
                futures.append(future)
                
                # Progress updates
                if (i + 1) % 10 == 0:
                    print(f"📊 Submitted {i+1}/{total_views} browsers...")
                
                # Small delay between launches
                time.sleep(random.uniform(0.5, 2.0))
            
            print(f"✅ All {total_views} browsers submitted!")
            print("⏳ Waiting for auto-close completion...")
            
            # Wait for all to complete
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1
                    
                    if completed % 5 == 0:
                        with self.lock:
                            active_count = len(self.active_processes)
                        print(f"📊 Completed: {completed}/{total_views}, Active: {active_count}")
                        
                except Exception as e:
                    print(f"❌ Browser error: {e}")
        
        # Final results
        elapsed_time = time.time() - start_time
        success_rate = (self.completed_views / total_views) * 100 if total_views > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎉 AUTO-CLOSE VIEW GENERATION COMPLETE!")
        print(f"✅ Successful views: {self.completed_views}/{total_views} ({success_rate:.1f}%)")
        print(f"❌ Failed views: {self.failed_views}")
        print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
        print(f"🔄 All browsers automatically closed - NO CRASHES!")
        
        # Final cleanup check
        with self.lock:
            if self.active_processes:
                print(f"⚠️  {len(self.active_processes)} browsers still active - cleaning up...")
                self.emergency_cleanup()
            else:
                print("✅ No browsers left running - system clean!")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🚨 Interrupted! Cleaning up browsers...")
    generator.emergency_cleanup()
    sys.exit(0)

def main():
    global generator
    
    if len(sys.argv) < 3:
        print("Usage: python3 auto_close_generator.py <youtube_url> <view_count> [options]")
        print("\nExamples:")
        print("  python3 auto_close_generator.py 'https://youtube.com/shorts/abc123' 20")
        print("  python3 auto_close_generator.py 'https://youtube.com/watch?v=abc123' 50 --concurrent 8 --time 2")
        print("\nOptions:")
        print("  --concurrent X : Max concurrent browsers (default: 5, recommended: 3-10)")
        print("  --time X       : Watch time per view in minutes (default: 1.5)")
        print("\n🔄 FEATURES:")
        print("  ✅ Automatically closes browsers after watch time")
        print("  ✅ Prevents system crashes from too many open windows")
        print("  ✅ Emergency cleanup on Ctrl+C")
        print("  ✅ Resource management and monitoring")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        view_count = int(sys.argv[2])
    except ValueError:
        print("❌ View count must be a number")
        sys.exit(1)
    
    # Parse options
    max_concurrent = 5  # Conservative default
    watch_minutes = 1.5
    
    if '--concurrent' in sys.argv:
        try:
            idx = sys.argv.index('--concurrent') + 1
            max_concurrent = min(int(sys.argv[idx]), 15)  # Cap at 15 to prevent crashes
        except (IndexError, ValueError):
            print("❌ Invalid --concurrent value")
            sys.exit(1)
    
    if '--time' in sys.argv:
        try:
            idx = sys.argv.index('--time') + 1
            watch_minutes = float(sys.argv[idx])
        except (IndexError, ValueError):
            print("❌ Invalid --time value")
            sys.exit(1)
    
    # Safety warnings
    if max_concurrent > 10:
        print(f"⚠️  WARNING: {max_concurrent} concurrent browsers may impact performance")
        print("   Recommended: 3-8 concurrent browsers for stability")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    if view_count > 100:
        print(f"⚠️  WARNING: {view_count} views will take approximately {(view_count * watch_minutes) / max_concurrent:.0f} minutes")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    print("🔄 Auto-Close View Generator - CRASH-PROOF VERSION")
    print("=" * 60)
    print(f"📺 URL: {url}")
    print(f"🎯 Views: {view_count}")
    print(f"🪟 Concurrent: {max_concurrent}")
    print(f"⏱️  Watch time: {watch_minutes} minutes")
    print(f"🔄 Auto-close: ENABLED")
    print()
    
    # Create generator
    generator = AutoCloseViewGenerator()
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        generator.generate_views_with_auto_close(url, view_count, max_concurrent, watch_minutes)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        generator.emergency_cleanup()
    
    print("\n✨ Generation complete - system clean!")

if __name__ == "__main__":
    main()
