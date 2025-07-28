import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from .proxy.proxy_manager import ProxyManager
from .simulation.view_simulator import ViewSimulator
from .safety_controller import SafetyController
from .view_counter_checker import ViewCountChecker

class ViewGenerator:
    """
    Simple, focused view generator that takes a URL and view count,
    then safely delivers those views with automatic timing and safety controls.
    """
    
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.safety_controller = SafetyController()
        self.view_counter_checker = ViewCountChecker()
        self.active_threads = 0
        self.completed_views = 0
        self.failed_views = 0
        self.initial_view_count = None
        
    def generate_views(self, video_url, target_views):
        """
        Main method: Generate the specified number of views for the video URL
        """
        logging.info(f"Starting view generation: {target_views} views for {video_url}")

        # Get initial view count for verification
        logging.info("Getting initial view count...")
        self.initial_view_count = self.view_counter_checker.get_current_view_count(video_url)
        if self.initial_view_count is not None:
            logging.info(f"Initial view count: {self.initial_view_count:,}")
        else:
            logging.warning("Could not get initial view count - will skip verification")

        # Calculate safe timing and threading
        timing_plan = self.safety_controller.calculate_safe_timing(target_views)
        logging.info(f"Estimated completion time: {timing_plan['estimated_hours']:.1f} hours")
        logging.info(f"Using {timing_plan['max_concurrent']} concurrent threads")
        
        # Start view generation
        start_time = time.time()
        self._execute_view_generation(video_url, target_views, timing_plan)
        
        # Report results
        elapsed_time = time.time() - start_time
        success_rate = (self.completed_views / target_views) * 100

        logging.info(f"View generation completed!")
        logging.info(f"Successful views: {self.completed_views}/{target_views} ({success_rate:.1f}%)")
        logging.info(f"Failed views: {self.failed_views}")
        logging.info(f"Total time: {elapsed_time/3600:.1f} hours")

        # Verify view count increase
        if self.initial_view_count is not None:
            logging.info("Checking if views were actually counted by YouTube...")
            final_view_count = self.view_counter_checker.get_current_view_count(video_url)

            if final_view_count is not None:
                actual_increase = final_view_count - self.initial_view_count
                logging.info(f"YouTube view count change: +{actual_increase:,} (from {self.initial_view_count:,} to {final_view_count:,})")

                if actual_increase > 0:
                    effectiveness = (actual_increase / self.completed_views) * 100 if self.completed_views > 0 else 0
                    logging.info(f"✅ Views are being counted! Effectiveness: {effectiveness:.1f}%")
                else:
                    logging.warning("❌ No view count increase detected. Views may not be counting properly.")
            else:
                logging.warning("Could not verify final view count")
        
    def _execute_view_generation(self, video_url, target_views, timing_plan):
        """
        Execute the actual view generation with proper threading and timing
        """
        max_workers = timing_plan['max_concurrent']
        delay_between_views = timing_plan['delay_between_views']
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for i in range(target_views):
                # Get next proxy
                proxy = self.proxy_manager.get_next_proxy()
                if not proxy:
                    logging.warning("No more proxies available, stopping")
                    break
                
                # Submit view task
                future = executor.submit(self._generate_single_view, video_url, proxy, i+1)
                futures.append(future)
                
                # Progress reporting
                if (i + 1) % 100 == 0:
                    logging.info(f"Queued {i+1}/{target_views} views")
                
                # Safety delay between submissions
                time.sleep(delay_between_views)
            
            # Wait for completion and track results
            for future in as_completed(futures):
                try:
                    success = future.result()
                    if success:
                        self.completed_views += 1
                    else:
                        self.failed_views += 1
                        
                    # Progress update every 50 completions
                    total_processed = self.completed_views + self.failed_views
                    if total_processed % 50 == 0:
                        logging.info(f"Progress: {total_processed}/{target_views} processed "
                                   f"({self.completed_views} successful)")
                        
                except Exception as e:
                    logging.error(f"View generation error: {e}")
                    self.failed_views += 1
    
    def _generate_single_view(self, video_url, proxy, view_number):
        """
        Generate a single view using the provided proxy
        """
        try:
            # Check if this view is safe to proceed
            if not self.safety_controller.is_view_safe(proxy['ip']):
                logging.debug(f"View {view_number} skipped for safety (IP: {proxy['ip']})")
                return False
            
            # Create simulator and generate view
            simulator = ViewSimulator(video_url, proxy)
            success = simulator.simulate_human_view()
            
            if success:
                self.safety_controller.record_successful_view(proxy['ip'], proxy.get('country', 'Unknown'))
                logging.debug(f"View {view_number} completed successfully")
                return True
            else:
                logging.debug(f"View {view_number} failed")
                return False
                
        except Exception as e:
            logging.error(f"Error in view {view_number}: {e}")
            return False
