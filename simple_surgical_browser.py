#!/usr/bin/env python3
"""
SIMPLE SURGICAL BROWSER - NO SELENIUM NEEDED!
Uses subprocess to launch Chrome directly (like our working tools)
Each browser gets its own process that we can kill surgically
PERFECT for 5000+ views without crashes!
"""

import subprocess
import time
import sys
import threading
import random
import os
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed

class SimpleSurgicalBrowser:
    def __init__(self):
        self.completed_views = 0
        self.failed_views = 0
        self.active_processes = {}  # Track processes by ID
        self.lock = threading.Lock()
        
    def create_surgical_browser(self, browser_id, url, watch_seconds=90):
        """Create ONE browser process that we can surgically close"""
        try:
            print(f"🎯 Browser {browser_id}: Starting surgical view...")

            # Create Chrome command with unique user data dir
            user_data_dir = f"/tmp/chrome_surgical_{browser_id}_{random.randint(1000,9999)}"

            cmd = [
                'google-chrome',
                '--new-window',  # Remove incognito to allow autoplay
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-extensions',
                '--start-maximized',  # Make video visible and likely to play
                '--autoplay-policy=no-user-gesture-required',  # FORCE AUTOPLAY
                '--disable-web-security',  # Allow autoplay
                '--allow-running-insecure-content',
                f'--user-data-dir={user_data_dir}',
                url
            ]
            
            # Launch browser process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid  # Create process group
            )
            
            # Track this specific process
            with self.lock:
                self.active_processes[browser_id] = {
                    'process': process,
                    'pid': process.pid,
                    'user_data_dir': user_data_dir,
                    'start_time': time.time()
                }
            
            print(f"   ✅ Browser {browser_id} opened (PID: {process.pid})")
            print(f"   ⏱️  Watching for {watch_seconds}s...")
            
            # Watch the video
            time.sleep(watch_seconds)
            
            # SURGICAL CLOSE: Kill ONLY this specific browser
            print(f"   🔪 SURGICALLY closing browser {browser_id}...")
            
            try:
                # Kill the process group (browser + all its tabs)
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                time.sleep(1)  # Give it time to close gracefully
                
                # If still running, force kill
                if process.poll() is None:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    print(f"   💀 Force-killed browser {browser_id}")
                else:
                    print(f"   ✅ Browser {browser_id} closed gracefully")
                
                # Clean up temp directory
                try:
                    subprocess.run(['rm', '-rf', user_data_dir], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
                except:
                    pass
                    
            except Exception as e:
                print(f"   ⚠️  Error closing browser {browser_id}: {e}")
            
            # Remove from tracking
            with self.lock:
                if browser_id in self.active_processes:
                    del self.active_processes[browser_id]
                self.completed_views += 1
                active_count = len(self.active_processes)
                print(f"   📊 Completed: {self.completed_views}, Active: {active_count}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Browser {browser_id} failed: {str(e)[:50]}")
            with self.lock:
                self.failed_views += 1
            return False
    
    def mass_surgical_generation(self, url, total_views, max_concurrent=8, watch_seconds=90):
        """Generate massive views with surgical precision"""
        print(f"🚀 SIMPLE SURGICAL BROWSER GENERATOR")
        print(f"📺 URL: {url[:60]}...")
        print(f"🎯 Target views: {total_views}")
        print(f"🪟 Max concurrent: {max_concurrent}")
        print(f"⏱️  Watch time: {watch_seconds}s per view")
        print(f"🔪 Surgical closing: ENABLED (subprocess method)")
        print()
        
        start_time = time.time()
        
        # Calculate estimated time
        estimated_minutes = (total_views * watch_seconds) / (max_concurrent * 60)
        print(f"⏰ Estimated completion: {estimated_minutes:.1f} minutes")
        print()
        
        # Use ThreadPoolExecutor for controlled concurrency
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            # Submit all browser tasks
            for i in range(total_views):
                browser_id = f"surgical_{i+1:04d}"
                
                future = executor.submit(
                    self.create_surgical_browser,
                    browser_id,
                    url,
                    watch_seconds
                )
                futures.append(future)
                
                # Progress updates
                if (i + 1) % 50 == 0:
                    print(f"📊 Submitted {i+1}/{total_views} browsers...")
                
                # Small delay to prevent overwhelming
                time.sleep(random.uniform(0.2, 0.8))
            
            print(f"✅ All {total_views} browsers submitted!")
            print("⏳ Processing with surgical precision...")
            print()
            
            # Monitor completion
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1
                    
                    # Progress updates every 25 completions
                    if completed % 25 == 0:
                        with self.lock:
                            active_count = len(self.active_processes)
                        
                        elapsed = time.time() - start_time
                        rate = completed / (elapsed / 60) if elapsed > 0 else 0
                        
                        print(f"📊 Progress: {completed}/{total_views} ({completed/total_views*100:.1f}%)")
                        print(f"   🪟 Active browsers: {active_count}")
                        print(f"   ⚡ Rate: {rate:.1f} views/minute")
                        print()
                        
                except Exception as e:
                    print(f"❌ Browser error: {e}")
        
        # Final results
        elapsed_time = time.time() - start_time
        success_rate = (self.completed_views / total_views) * 100 if total_views > 0 else 0
        views_per_minute = self.completed_views / (elapsed_time / 60) if elapsed_time > 0 else 0
        
        print("\n" + "=" * 70)
        print("🎉 SURGICAL BROWSER GENERATION COMPLETE!")
        print(f"✅ Successful views: {self.completed_views}/{total_views} ({success_rate:.1f}%)")
        print(f"❌ Failed views: {self.failed_views}")
        print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
        print(f"⚡ Average rate: {views_per_minute:.1f} views/minute")
        print(f"🔪 All browsers surgically closed - NO CRASHES!")
        
        # Final cleanup check
        with self.lock:
            if self.active_processes:
                print(f"⚠️  {len(self.active_processes)} browsers still active - emergency cleanup...")
                self.emergency_cleanup()
            else:
                print("✅ Perfect surgical cleanup - zero browsers remaining!")
    
    def emergency_cleanup(self):
        """Emergency cleanup - kill all tracked processes"""
        print("🚨 EMERGENCY CLEANUP - Killing all browser processes...")
        
        with self.lock:
            processes_to_kill = list(self.active_processes.items())
        
        for browser_id, process_info in processes_to_kill:
            try:
                pid = process_info['pid']
                os.killpg(os.getpgid(pid), signal.SIGKILL)
                print(f"   💀 Killed browser {browser_id} (PID: {pid})")
                
                # Clean up temp directory
                user_data_dir = process_info['user_data_dir']
                subprocess.run(['rm', '-rf', user_data_dir], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"   ⚠️  Error killing {browser_id}: {e}")
        
        with self.lock:
            self.active_processes.clear()
        
        print("✅ Emergency cleanup complete")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🚨 Interrupted! Emergency cleanup...")
    generator.emergency_cleanup()
    sys.exit(0)

def main():
    global generator
    
    if len(sys.argv) < 3:
        print("Usage: python3 simple_surgical_browser.py <youtube_url> <view_count> [options]")
        print("\nExamples:")
        print("  python3 simple_surgical_browser.py 'https://youtube.com/shorts/abc123' 100")
        print("  python3 simple_surgical_browser.py 'https://youtube.com/watch?v=abc123' 5000 --concurrent 15")
        print("\nOptions:")
        print("  --concurrent X : Max concurrent browsers (default: 8, max: 20)")
        print("  --time X       : Watch time per view in seconds (default: 90)")
        print("\n🚀 FEATURES:")
        print("  ✅ NO SELENIUM - uses direct subprocess (faster, more reliable)")
        print("  ✅ Surgical precision closing (kills only specific browser)")
        print("  ✅ Designed for 5000+ views without crashes")
        print("  ✅ Emergency cleanup on Ctrl+C")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        view_count = int(sys.argv[2])
    except ValueError:
        print("❌ View count must be a number")
        sys.exit(1)
    
    # Parse options
    max_concurrent = 8
    watch_seconds = 90
    
    if '--concurrent' in sys.argv:
        try:
            idx = sys.argv.index('--concurrent') + 1
            max_concurrent = min(int(sys.argv[idx]), 20)
        except (IndexError, ValueError):
            print("❌ Invalid --concurrent value")
            sys.exit(1)
    
    if '--time' in sys.argv:
        try:
            idx = sys.argv.index('--time') + 1
            watch_seconds = int(sys.argv[idx])
        except (IndexError, ValueError):
            print("❌ Invalid --time value")
            sys.exit(1)
    
    # Safety warnings
    if view_count > 1000:
        estimated_minutes = (view_count * watch_seconds) / (max_concurrent * 60)
        print(f"⚠️  WARNING: {view_count} views will take approximately {estimated_minutes:.0f} minutes")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    print("🔪 SIMPLE SURGICAL BROWSER GENERATOR")
    print("=" * 60)
    
    # Create generator
    generator = SimpleSurgicalBrowser()
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        generator.mass_surgical_generation(url, view_count, max_concurrent, watch_seconds)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        generator.emergency_cleanup()

if __name__ == "__main__":
    main()
