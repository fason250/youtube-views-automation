#!/usr/bin/env python3
"""
Professional YouTube View Generator
- Incognito windows (no account)
- IP rotation support
- Window lifecycle management
- Behavior tracking
- Scalable for 400+ views
"""

import subprocess
import time
import sys
import os
import threading
import random
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class ViewGenerator:
    def __init__(self):
        self.active_windows = {}
        self.completed_views = 0
        self.failed_views = 0
        self.lock = threading.Lock()
        self.proxies = []
        
    def get_proxy_list(self):
        """Get working proxy list for IP rotation"""
        print("🔍 Getting proxy list for IP rotation...")
        
        try:
            # Get proxies from free sources
            proxy_sources = [
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&format=textplain&country=all"
            ]
            
            all_proxies = []
            for source in proxy_sources:
                try:
                    response = requests.get(source, timeout=10)
                    if response.status_code == 200:
                        proxies = response.text.strip().split('\n')
                        all_proxies.extend([p.strip() for p in proxies if p.strip() and ':' in p])
                        if len(all_proxies) >= 50:  # Stop when we have enough
                            break
                except:
                    continue
            
            # Test a few proxies quickly
            working_proxies = []
            test_proxies = random.sample(all_proxies, min(20, len(all_proxies)))
            
            for proxy in test_proxies:
                try:
                    proxies_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                    response = requests.get('http://httpbin.org/ip', proxies=proxies_dict, timeout=3)
                    if response.status_code == 200:
                        working_proxies.append(proxy)
                        if len(working_proxies) >= 10:  # Get 10 working proxies
                            break
                except:
                    continue
            
            self.proxies = working_proxies
            print(f"✅ Found {len(self.proxies)} working proxies")
            
        except Exception as e:
            print(f"⚠️  Proxy loading failed: {e}")
            self.proxies = []  # Use direct connection
    
    def create_incognito_browser(self, window_id, proxy=None, user_agent=None):
        """Create incognito browser window with optional proxy"""
        try:
            print(f"🕵️  Creating incognito window {window_id}...")
            
            # Build Chrome command
            cmd = [
                'google-chrome',
                '--incognito',  # Private browsing
                '--new-window',  # New window
                '--no-first-run',  # Skip first run
                '--no-default-browser-check',  # Skip default browser check
                '--disable-extensions',  # No extensions
                '--disable-plugins',  # No plugins
                '--disable-web-security',  # Allow cross-origin
                '--disable-features=VizDisplayCompositor',  # Performance
            ]
            
            # Add proxy if provided
            if proxy:
                cmd.append(f'--proxy-server=http://{proxy}')
                print(f"   🌐 Using proxy: {proxy}")
            
            # Add custom user agent
            if user_agent:
                cmd.append(f'--user-agent={user_agent}')
            
            # Add the URL as last argument (will be added by caller)
            return cmd
            
        except Exception as e:
            print(f"   ❌ Failed to create browser command: {e}")
            return None
    
    def simulate_view_session(self, url, window_id, watch_time_minutes=2, proxy=None):
        """Simulate a complete view session with behavior tracking"""
        process = None
        try:
            print(f"🎬 Starting view session {window_id}...")
            
            # Get random user agent
            user_agents = [
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            ]
            user_agent = random.choice(user_agents)
            
            # Create browser command
            cmd = self.create_incognito_browser(window_id, proxy, user_agent)
            if not cmd:
                raise Exception("Could not create browser command")
            
            # Add URL to command
            cmd.append(url)
            
            # Launch browser
            print(f"   🚀 Launching browser window {window_id}...")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid  # Create new process group
            )
            
            # Track the window
            with self.lock:
                self.active_windows[window_id] = {
                    'process': process,
                    'start_time': time.time(),
                    'proxy': proxy,
                    'url': url,
                    'status': 'watching'
                }
            
            print(f"   ✅ Window {window_id} opened successfully")
            print(f"   ⏱️  Will watch for {watch_time_minutes} minutes...")
            
            # Simulate watching behavior
            watch_seconds = watch_time_minutes * 60
            start_time = time.time()
            
            while time.time() - start_time < watch_seconds:
                # Check if process is still running
                if process.poll() is not None:
                    print(f"   ⚠️  Window {window_id} was closed by user")
                    break
                
                elapsed = time.time() - start_time
                remaining = watch_seconds - elapsed
                
                # Show progress every 30 seconds
                if int(elapsed) % 30 == 0 and elapsed > 0:
                    print(f"   📊 Window {window_id}: {elapsed:.0f}s watched, {remaining:.0f}s remaining")
                
                time.sleep(1)
            
            # Close the browser
            print(f"   🔄 Closing window {window_id} after {watch_time_minutes} minutes...")
            try:
                # Terminate the process group
                os.killpg(os.getpgid(process.pid), 15)  # SIGTERM
                time.sleep(2)
                if process.poll() is None:
                    os.killpg(os.getpgid(process.pid), 9)  # SIGKILL
            except:
                pass
            
            # Update tracking
            with self.lock:
                if window_id in self.active_windows:
                    self.active_windows[window_id]['status'] = 'completed'
                    self.active_windows[window_id]['end_time'] = time.time()
                self.completed_views += 1
            
            print(f"   ✅ View session {window_id} completed successfully")
            return True
            
        except Exception as e:
            print(f"   ❌ View session {window_id} failed: {str(e)[:50]}")
            
            # Clean up process if it exists
            if process:
                try:
                    os.killpg(os.getpgid(process.pid), 9)
                except:
                    pass
            
            with self.lock:
                if window_id in self.active_windows:
                    self.active_windows[window_id]['status'] = 'failed'
                self.failed_views += 1
            
            return False
        
        finally:
            # Clean up tracking
            with self.lock:
                if window_id in self.active_windows:
                    del self.active_windows[window_id]
    
    def generate_views(self, url, total_views, concurrent_windows=5, watch_time_minutes=2):
        """Generate views with IP rotation and window management"""
        print(f"🚀 Professional YouTube View Generator")
        print(f"📺 URL: {url}")
        print(f"🎯 Target views: {total_views}")
        print(f"🪟 Concurrent windows: {concurrent_windows}")
        print(f"⏱️  Watch time per view: {watch_time_minutes} minutes")
        print()
        
        # Get proxies for IP rotation
        self.get_proxy_list()
        
        # Calculate timing
        estimated_time = (total_views * watch_time_minutes) / concurrent_windows
        print(f"⏱️  Estimated completion time: {estimated_time:.1f} minutes")
        print()
        
        start_time = time.time()
        
        # Use thread pool for concurrent windows
        with ThreadPoolExecutor(max_workers=concurrent_windows) as executor:
            futures = []
            
            for i in range(total_views):
                # Select proxy for IP rotation
                proxy = random.choice(self.proxies) if self.proxies else None
                
                # Submit view session
                future = executor.submit(
                    self.simulate_view_session,
                    url,
                    f"view_{i+1}",
                    watch_time_minutes,
                    proxy
                )
                futures.append(future)
                
                # Small delay between submissions
                time.sleep(random.uniform(1, 3))
                
                # Show progress
                if (i + 1) % 10 == 0:
                    print(f"📊 Submitted {i+1}/{total_views} view sessions...")
            
            print(f"✅ All {total_views} view sessions submitted!")
            print("⏳ Waiting for completion...")
            
            # Wait for all sessions to complete
            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result()
                    completed += 1
                    if completed % 10 == 0:
                        print(f"📊 Completed {completed}/{total_views} view sessions...")
                except Exception as e:
                    print(f"❌ Session error: {e}")
        
        # Final results
        elapsed_time = time.time() - start_time
        success_rate = (self.completed_views / total_views) * 100 if total_views > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎉 VIEW GENERATION COMPLETE!")
        print(f"✅ Successful views: {self.completed_views}/{total_views} ({success_rate:.1f}%)")
        print(f"❌ Failed views: {self.failed_views}")
        print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
        print(f"🌐 Used {len(self.proxies)} different IPs")
        print(f"🕵️  All sessions used incognito mode (no account)")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 view_generator.py <youtube_url> <view_count> [options]")
        print("\nExamples:")
        print("  python3 view_generator.py 'https://youtube.com/shorts/abc123' 50")
        print("  python3 view_generator.py 'https://youtube.com/watch?v=abc123' 400 --concurrent 10 --time 3")
        print("\nOptions:")
        print("  --concurrent X : Number of concurrent browser windows (default: 5)")
        print("  --time X       : Watch time per view in minutes (default: 2)")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        view_count = int(sys.argv[2])
    except ValueError:
        print("❌ View count must be a number")
        sys.exit(1)
    
    # Parse options
    concurrent_windows = 5
    watch_time_minutes = 2
    
    if '--concurrent' in sys.argv:
        try:
            idx = sys.argv.index('--concurrent') + 1
            concurrent_windows = int(sys.argv[idx])
        except (IndexError, ValueError):
            print("❌ Invalid --concurrent value")
            sys.exit(1)
    
    if '--time' in sys.argv:
        try:
            idx = sys.argv.index('--time') + 1
            watch_time_minutes = int(sys.argv[idx])
        except (IndexError, ValueError):
            print("❌ Invalid --time value")
            sys.exit(1)
    
    # Create and run generator
    generator = ViewGenerator()
    
    try:
        generator.generate_views(url, view_count, concurrent_windows, watch_time_minutes)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        print("🔄 Cleaning up active windows...")
        # Clean up any active windows
        for window_id, window_info in generator.active_windows.items():
            try:
                process = window_info['process']
                os.killpg(os.getpgid(process.pid), 9)
            except:
                pass
    
    print("\n✨ View generation finished!")

if __name__ == "__main__":
    main()
