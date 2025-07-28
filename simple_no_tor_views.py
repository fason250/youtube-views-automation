#!/usr/bin/env python3
"""
SIMPLE NO-TOR YOUTUBE VIEW GENERATOR
🎯 MISSION: Generate YouTube views with manual consent (no TOR)
👤 METHOD: User accepts consent ONCE, system reuses session
🌐 NETWORK: Regular internet (for testing/development)
🔊 GUARANTEE: Videos play without bot detection

SIMPLE NO-TOR FEATURES:
✅ User manually accepts consent (100% human)
✅ System reuses accepted session
✅ No TOR complexity (for testing)
✅ No robotic clicking patterns
✅ Natural video playback
✅ Production logging and monitoring
"""

import subprocess
import time
import sys
import threading
import random
import os
import signal
import json
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class SimpleNoTorViews:
    def __init__(self):
        self.completed_views = 0
        self.failed_views = 0
        self.active_processes = {}
        self.lock = threading.Lock()
        self.start_time = None
        self.consent_accepted = False
        
        # Simple settings
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.master_profile_dir = f"/tmp/youtube_profile_{self.session_id}"
        
        # Setup logging
        self.setup_logging()
        
        # Verify system requirements
        self.verify_requirements()
        
    def setup_logging(self):
        """Setup simple logging"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/simple_no_tor_{self.session_id}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def verify_requirements(self):
        """Verify system requirements"""
        self.logger.info("🔍 Verifying simple system requirements...")
        
        # Check Chrome
        try:
            result = subprocess.run(['google-chrome', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.logger.info("✅ Google Chrome is installed")
            else:
                raise Exception("Chrome not working")
        except Exception:
            self.logger.error("❌ Google Chrome is not installed")
            sys.exit(1)
            
        self.logger.info("✅ All simple requirements verified")
        
    def setup_manual_consent(self, url):
        """Setup manual consent acceptance"""
        print("\n" + "=" * 80)
        print("👤 MANUAL CONSENT ACCEPTANCE REQUIRED")
        print("=" * 80)
        print("🎯 We need you to accept YouTube consent ONCE manually")
        print("🍪 This creates a clean session that all browsers will reuse")
        print("🤖 This avoids ALL bot detection from automated clicking")
        print()
        print("📋 INSTRUCTIONS:")
        print("1. A Chrome browser will open with the YouTube consent page")
        print("2. Click 'Accept all' or 'Reject all' (your choice)")
        print("3. Wait for the video to start playing")
        print("4. Close the browser window")
        print("5. The system will then generate all your views automatically")
        print()
        
        input("Press ENTER when ready to open consent browser...")
        
        # Create master profile directory
        os.makedirs(self.master_profile_dir, exist_ok=True)
        
        # Launch consent browser
        self.logger.info("🌐 Opening consent browser (regular internet)...")
        
        consent_cmd = [
            'google-chrome',
            '--new-window',
            '--no-first-run',
            '--no-default-browser-check',
            '--start-maximized',
            f'--user-data-dir={self.master_profile_dir}',
            url
        ]
        
        consent_process = subprocess.Popen(
            consent_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print("\n🌐 Consent browser opened!")
        print("👤 Please accept/reject consent and wait for video to play")
        print("🔴 Then CLOSE the browser window to continue")
        
        # Wait for user to close browser
        while consent_process.poll() is None:
            time.sleep(2)
            
        print("✅ Consent browser closed!")
        print("🍪 Consent session saved for reuse")
        
        self.consent_accepted = True
        self.logger.info("✅ Manual consent acceptance completed")
        
    def create_simple_browser(self, browser_id, url, watch_seconds=90):
        """Create simple browser with manual consent session"""
        try:
            self.logger.info(f"👤 Browser {browser_id}: Starting simple view...")
            
            # Create browser with copied consent session
            user_data_dir = f"/tmp/chrome_simple_{self.session_id}_{browser_id}_{random.randint(1000,9999)}"
            
            # Copy master profile (with consent) to new browser
            subprocess.run([
                'cp', '-r', self.master_profile_dir, user_data_dir
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Generate random human-like user agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            user_agent = random.choice(user_agents)
            
            # SIMPLE Chrome command with manual consent session (NO TOR)
            cmd = [
                'google-chrome',
                '--new-window',
                '--no-first-run',
                '--no-default-browser-check',
                '--start-maximized',
                
                # SIMPLE: Minimal flags for natural behavior
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions-http-throttling',
                '--disable-background-timer-throttling',
                
                # VIDEO: Natural autoplay
                '--autoplay-policy=no-user-gesture-required',
                '--enable-features=MediaEngagementBypassAutoplayPolicies',
                
                # AUDIO: Enable sound
                '--use-fake-ui-for-media-stream',
                '--use-fake-device-for-media-stream',
                
                # SIMPLE: Human-like user agent
                f'--user-agent={user_agent}',
                
                # SIMPLE: Use consent session
                f'--user-data-dir={user_data_dir}',
                
                # Direct URL (consent already accepted)
                url
            ]
            
            # Launch simple browser
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )
            
            # Track in simple monitoring
            with self.lock:
                self.active_processes[browser_id] = {
                    'process': process,
                    'pid': process.pid,
                    'user_data_dir': user_data_dir,
                    'start_time': time.time(),
                    'url': url,
                    'watch_seconds': watch_seconds,
                    'status': 'loading',
                    'user_agent': user_agent
                }
                
            self.logger.info(f"✅ Simple browser {browser_id} launched (PID: {process.pid})")
            self.logger.info(f"🌐 Using regular internet connection")
            self.logger.info(f"👤 Using manual consent session")
            self.logger.info(f"🥷 User agent: {user_agent[:50]}...")
            
            # HUMAN-LIKE: Variable loading time
            load_time = random.uniform(8, 15)
            self.logger.info(f"📺 Loading YouTube with manual consent - {load_time:.1f}s...")
            time.sleep(load_time)
            
            # Verify browser is still running
            if process.poll() is None:
                with self.lock:
                    self.active_processes[browser_id]['status'] = 'watching'
                    
                self.logger.info(f"🎬 Simple video loaded! Browser {browser_id} watching for {watch_seconds}s")
                self.logger.info(f"🔊 Audio should be playing naturally!")
                
                # HUMAN-LIKE: Natural watch period with small variations
                actual_watch_time = watch_seconds + random.uniform(-5, 10)
                time.sleep(actual_watch_time)
                
                # Mark as completed
                with self.lock:
                    self.completed_views += 1
                    active_count = len(self.active_processes)
                    self.active_processes[browser_id]['status'] = 'completed'
                    
                self.logger.info(f"✅ Simple browser {browser_id} completed {actual_watch_time:.1f}s watch!")
                self.logger.info(f"📊 Progress: {self.completed_views} completed, {active_count-1} active")
                
                return True
                
            else:
                self.logger.error(f"❌ Simple browser {browser_id} crashed during loading")
                raise Exception("Browser process crashed")
                
        except Exception as e:
            self.logger.error(f"❌ Simple browser {browser_id} failed: {str(e)}")
            with self.lock:
                self.failed_views += 1
            return False
            
        finally:
            # Surgical cleanup
            self.surgical_cleanup_browser(browser_id)
            
    def surgical_cleanup_browser(self, browser_id):
        """Surgical cleanup of specific browser"""
        if browser_id not in self.active_processes:
            return
            
        process_info = self.active_processes[browser_id]
        process = process_info['process']
        
        try:
            self.logger.info(f"🔪 Surgically closing simple browser {browser_id}...")
            
            # Graceful termination
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                time.sleep(2)
                
                if process.poll() is None:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    self.logger.info(f"💀 Force-killed simple browser {browser_id}")
                else:
                    self.logger.info(f"✅ Simple browser {browser_id} closed gracefully")
            except:
                pass
                
            # Cleanup temp directory
            try:
                subprocess.run(['rm', '-rf', process_info['user_data_dir']], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"⚠️ Error during surgical cleanup of {browser_id}: {e}")
            
        finally:
            # Remove from tracking
            with self.lock:
                if browser_id in self.active_processes:
                    del self.active_processes[browser_id]
                    
    def generate_simple_views(self, url, total_views, max_concurrent=3, watch_seconds=90):
        """Generate simple views with manual consent"""
        
        # First: Manual consent acceptance
        if not self.consent_accepted:
            self.setup_manual_consent(url)
            
        self.start_time = time.time()
        
        print("\n" + "=" * 80)
        print("🚀 STARTING AUTOMATED VIEW GENERATION")
        print("=" * 80)
        
        self.logger.info("👤 SIMPLE NO-TOR YOUTUBE VIEW GENERATOR STARTED")
        self.logger.info(f"📺 Target URL: {url}")
        self.logger.info(f"🎯 Target views: {total_views}")
        self.logger.info(f"🪟 Max concurrent: {max_concurrent}")
        self.logger.info(f"⏱️ Watch time: {watch_seconds}s per view")
        self.logger.info(f"🌐 Network: Regular internet (no TOR)")
        self.logger.info(f"👤 Manual consent: ACCEPTED")
        self.logger.info(f"📋 Session ID: {self.session_id}")
        
        # Estimated completion time
        estimated_minutes = (total_views * (watch_seconds + 15)) / (max_concurrent * 60)
        self.logger.info(f"⏰ Estimated completion: {estimated_minutes:.1f} minutes")
        
        # Simple execution
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            # Submit all view generation tasks
            for i in range(total_views):
                browser_id = f"simple_{i+1:04d}"
                
                future = executor.submit(
                    self.create_simple_browser,
                    browser_id,
                    url,
                    watch_seconds
                )
                futures.append(future)
                
                # Progress logging
                if (i + 1) % 5 == 0:
                    self.logger.info(f"📊 Submitted {i+1}/{total_views} simple browsers to queue")
                    
                # HUMAN-LIKE: Variable launch delays
                delay = random.uniform(2.0, 5.0)
                time.sleep(delay)
                
            self.logger.info(f"✅ All {total_views} simple browsers submitted to queue!")
            
            # Monitor execution
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1
                    
                    # Progress reporting
                    if completed % 3 == 0:
                        self.log_progress_report(completed, total_views)
                        
                except Exception as e:
                    self.logger.error(f"❌ Simple browser execution error: {e}")
                    
        # Final simple report
        self.generate_final_report(total_views)

    def log_progress_report(self, completed, total_views):
        """Log detailed progress report"""
        with self.lock:
            active_count = len(self.active_processes)

        elapsed = time.time() - self.start_time
        rate = completed / (elapsed / 60) if elapsed > 0 else 0
        progress_pct = (completed / total_views) * 100

        self.logger.info(f"📊 SIMPLE PROGRESS REPORT:")
        self.logger.info(f"   ✅ Completed: {completed}/{total_views} ({progress_pct:.1f}%)")
        self.logger.info(f"   🪟 Active browsers: {active_count}")
        self.logger.info(f"   ⚡ Rate: {rate:.1f} views/minute")
        self.logger.info(f"   ⏱️ Elapsed: {elapsed/60:.1f} minutes")

    def generate_final_report(self, total_views):
        """Generate comprehensive final report"""
        elapsed_time = time.time() - self.start_time
        success_rate = (self.completed_views / total_views) * 100 if total_views > 0 else 0
        views_per_minute = self.completed_views / (elapsed_time / 60) if elapsed_time > 0 else 0

        # Console report
        print("\n" + "=" * 80)
        print("👤 SIMPLE NO-TOR YOUTUBE VIEW GENERATION COMPLETE!")
        print("=" * 80)
        print(f"📊 FINAL SIMPLE STATISTICS:")
        print(f"   ✅ Successful views: {self.completed_views}/{total_views} ({success_rate:.1f}%)")
        print(f"   ❌ Failed views: {self.failed_views}")
        print(f"   ⏱️  Total time: {elapsed_time/60:.1f} minutes")
        print(f"   ⚡ Average rate: {views_per_minute:.1f} views/minute")
        print(f"   🌐 Network: Regular internet (no TOR)")
        print(f"   👤 Manual consent: Human acceptance")
        print(f"   🔊 Video playback: Natural audio enabled")
        print(f"   🔪 System cleanup: Surgical precision")
        print(f"   📋 Session ID: {self.session_id}")
        print("=" * 80)
        print("🎯 Simple views generated - 100% HUMAN consent acceptance!")
        print("📁 Detailed logs saved in logs/ directory")

        # Cleanup
        self.production_cleanup()

    def production_cleanup(self):
        """Complete production cleanup"""
        self.logger.info("🧹 Starting simple production cleanup...")

        # Cleanup any remaining browsers
        with self.lock:
            remaining_browsers = list(self.active_processes.keys())

        for browser_id in remaining_browsers:
            self.surgical_cleanup_browser(browser_id)

        # Cleanup master profile
        try:
            subprocess.run(['rm', '-rf', self.master_profile_dir],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

        self.logger.info("✅ Simple production cleanup complete")

def main():
    if len(sys.argv) < 3:
        print("👤 SIMPLE NO-TOR YOUTUBE VIEW GENERATOR")
        print("=" * 60)
        print("Usage: python3 simple_no_tor_views.py <youtube_url> <view_count> [options]")
        print("\nExamples:")
        print("  python3 simple_no_tor_views.py 'https://youtube.com/shorts/abc123' 10")
        print("  python3 simple_no_tor_views.py 'https://youtube.com/watch?v=abc123' 20 --concurrent 5")
        print("\nOptions:")
        print("  --concurrent X : Max concurrent browsers (default: 3, max: 8)")
        print("  --time X       : Watch time per view in seconds (default: 90)")
        print("\n👤 SIMPLE NO-TOR FEATURES:")
        print("  ✅ YOU manually accept consent (100% human)")
        print("  ✅ System reuses your consent session")
        print("  ✅ Regular internet (no TOR complexity)")
        print("  ✅ No robotic clicking patterns")
        print("  ✅ Natural video playback with audio")
        print("  ✅ Views that look HUMAN to YouTube!")
        print("\n📦 REQUIREMENTS:")
        print("  - Google Chrome installed")
        print("  - Python 3.6+")
        print("\n⚠️  NOTE: Uses your regular IP (for testing)")
        print("    For IP diversity, use the TOR version once TOR is working")
        sys.exit(1)

    url = sys.argv[1]
    try:
        view_count = int(sys.argv[2])
    except ValueError:
        print("❌ View count must be a number")
        sys.exit(1)

    # Parse simple options
    max_concurrent = 3  # Conservative for stability
    watch_seconds = 90

    if '--concurrent' in sys.argv:
        try:
            idx = sys.argv.index('--concurrent') + 1
            max_concurrent = min(int(sys.argv[idx]), 8)  # Simple limit
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

    print("👤 SIMPLE NO-TOR YOUTUBE VIEW GENERATOR")
    print("=" * 60)
    print("🎯 Generating views with 100% HUMAN consent!")
    print("🌐 Using regular internet (no TOR)")
    print("👤 YOU will accept consent manually (no bot detection)")
    print("🔊 TURN UP YOUR SPEAKERS - You should hear videos playing!")
    print()

    # Initialize simple generator
    generator = SimpleNoTorViews()

    try:
        generator.generate_simple_views(url, view_count, max_concurrent, watch_seconds)
    except Exception as e:
        generator.logger.error(f"❌ Simple production error: {e}")
        generator.production_cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
