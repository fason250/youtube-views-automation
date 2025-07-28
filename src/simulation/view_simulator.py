from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import random
import time
import logging

class ViewSimulator:
    """
    Streamlined view simulator focused on human-like behavior without over-engineering
    """

    def __init__(self, video_url, proxy_config):
        self.video_url = video_url
        self.proxy_config = proxy_config
        self.driver = None

    def simulate_human_view(self):
        """
        Main method to simulate a human-like view of the video
        """
        try:
            self._setup_browser()
            self._navigate_naturally()
            self._watch_video()
            self._random_engagement()
            return True

        except Exception as e:
            logging.error(f"View simulation failed: {str(e)}")
            return False
        finally:
            self._cleanup()

    def _setup_browser(self):
        """
        Setup Chrome browser with human-like configuration
        """
        options = webdriver.ChromeOptions()

        # Proxy configuration
        if self.proxy_config and 'ip' in self.proxy_config:
            proxy_string = f"{self.proxy_config['ip']}:{self.proxy_config.get('port', 8080)}"
            options.add_argument(f'--proxy-server={proxy_string}')

        # Human-like browser settings optimized for Linux servers
        options.add_argument('--headless=new')  # Headless for efficiency
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Faster loading
        options.add_argument('--disable-javascript')  # Not needed for view counting
        options.add_argument('--single-process')  # Better for containers

        # Random window size (common resolutions)
        resolutions = [(1920, 1080), (1366, 768), (1440, 900), (1280, 720)]
        width, height = random.choice(resolutions)
        options.add_argument(f'--window-size={width},{height}')

        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')

        # Additional stealth options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Setup driver - try system chromedriver first, then download if needed
        try:
            # Try system chromedriver first (faster)
            self.driver = webdriver.Chrome(options=options)
        except Exception:
            try:
                # Fallback to webdriver-manager (slower but more reliable)
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logging.error(f"Failed to setup Chrome driver: {e}")
                raise

        # Execute stealth script
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _navigate_naturally(self):
        """
        Navigate to the video in a natural, human-like way
        """
        # More often go to YouTube homepage first (70% of the time - more realistic)
        if random.random() > 0.3:
            self.driver.get("https://www.youtube.com")
            time.sleep(random.uniform(3, 7))  # Longer wait time

            # Simulate browsing behavior on homepage
            self._simulate_homepage_browsing()

            # Sometimes search for the video instead of direct navigation
            if random.random() > 0.6:
                self._simulate_search_navigation()
                return

        # Navigate to the target video directly
        self.driver.get(self.video_url)
        time.sleep(random.uniform(4, 8))  # Longer wait for page load

        # Wait for video to be ready
        self._wait_for_video_ready()

    def _simulate_homepage_browsing(self):
        """
        Simulate realistic browsing behavior on YouTube homepage
        """
        # Random scrolling on homepage
        for _ in range(random.randint(2, 5)):
            self._random_scroll()
            time.sleep(random.uniform(1, 3))

        # Sometimes click on a random video thumbnail (but don't watch it)
        if random.random() > 0.7:
            try:
                # Find video thumbnails
                thumbnails = self.driver.find_elements(By.CSS_SELECTOR,
                    "a#thumbnail, ytd-thumbnail a")
                if thumbnails:
                    random_thumbnail = random.choice(thumbnails[:10])  # Only first 10
                    random_thumbnail.click()
                    time.sleep(random.uniform(2, 5))  # Brief stay
                    self.driver.back()  # Go back
                    time.sleep(random.uniform(1, 3))
            except:
                pass  # If clicking fails, continue

    def _simulate_search_navigation(self):
        """
        Navigate to video through search (more natural)
        """
        try:
            # Find search box
            search_box = self.driver.find_element(By.CSS_SELECTOR,
                "input#search, input[name='search_query']")

            # Extract video title or use video ID for search
            video_id = self.video_url.split('v=')[1].split('&')[0] if 'v=' in self.video_url else ""
            search_terms = [video_id, "video", "youtube video"]  # Fallback search terms

            search_term = random.choice(search_terms)

            # Type search term naturally
            search_box.clear()
            for char in search_term:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))  # Natural typing speed

            time.sleep(random.uniform(0.5, 1.5))

            # Press Enter or click search button
            if random.random() > 0.5:
                search_box.send_keys("\n")
            else:
                search_button = self.driver.find_element(By.CSS_SELECTOR,
                    "button#search-icon-legacy, button[aria-label*='Search']")
                search_button.click()

            time.sleep(random.uniform(2, 4))

            # Click on our target video from search results
            self.driver.get(self.video_url)
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            logging.debug(f"Search navigation failed, using direct navigation: {e}")
            self.driver.get(self.video_url)
            time.sleep(random.uniform(4, 8))

    def _wait_for_video_ready(self):
        """
        Wait for video to be ready and loaded
        """
        try:
            # Wait for video element to be present and ready
            video_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            # Wait a bit more for video to be fully loaded
            time.sleep(random.uniform(2, 4))

            # Check if video is actually playable
            ready_state = self.driver.execute_script("return arguments[0].readyState", video_element)
            if ready_state < 2:  # HAVE_CURRENT_DATA
                time.sleep(random.uniform(2, 5))  # Wait more if not ready

        except Exception as e:
            logging.debug(f"Video ready check failed: {e}")
            time.sleep(random.uniform(3, 6))  # Fallback wait

    def _watch_video(self):
        """
        Watch the video with human-like behavior to ensure YouTube counts it
        """
        try:
            # Wait for video element to load
            video_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            # Ensure video starts playing
            self._ensure_video_plays(video_element)

            # Get video duration
            duration = self.driver.execute_script("return arguments[0].duration", video_element)
            if not duration or duration <= 0:
                duration = 180  # Default 3 minutes if can't get duration

            # Calculate realistic watch time (60-95% of video for better counting)
            watch_percentage = random.uniform(0.6, 0.95)
            watch_time = duration * watch_percentage

            # Minimum watch time for YouTube to count the view (30 seconds)
            min_watch_time = max(30, duration * 0.3)  # At least 30 seconds or 30% of video
            watch_time = max(watch_time, min_watch_time)

            logging.debug(f"Watching video for {watch_time:.1f} seconds ({watch_percentage:.1%} of {duration:.1f}s)")

            # Simulate human watching behavior
            self._simulate_watching_behavior(watch_time, video_element)

        except Exception as e:
            logging.warning(f"Could not get video duration, using default watch time: {e}")
            # Default watch time if we can't get video info (ensure minimum 30 seconds)
            default_watch_time = random.uniform(45, 180)  # 45 seconds to 3 minutes
            self._simulate_watching_behavior(default_watch_time, None)

    def _ensure_video_plays(self, video_element):
        """
        Ensure the video actually starts playing
        """
        try:
            # Check if video is paused and click to play
            is_paused = self.driver.execute_script("return arguments[0].paused", video_element)
            if is_paused:
                video_element.click()
                time.sleep(random.uniform(1, 2))

            # Wait for video to actually start playing
            for _ in range(10):  # Try for up to 10 seconds
                current_time = self.driver.execute_script("return arguments[0].currentTime", video_element)
                if current_time > 0:
                    break
                time.sleep(1)

                # Try clicking again if still not playing
                if self.driver.execute_script("return arguments[0].paused", video_element):
                    video_element.click()
                    time.sleep(0.5)

            logging.debug("Video is playing")

        except Exception as e:
            logging.debug(f"Could not ensure video plays: {e}")
            # Try clicking in the center of the video area
            try:
                video_element.click()
                time.sleep(2)
            except:
                pass

    def _simulate_watching_behavior(self, watch_time, video_element):
        """
        Simulate realistic watching behavior during the video
        """
        start_time = time.time()
        end_time = start_time + watch_time
        last_progress_check = start_time

        logging.debug(f"Starting {watch_time:.1f} second watch session")

        while time.time() < end_time:
            current_time = time.time()
            elapsed = current_time - start_time
            remaining = end_time - current_time

            # Check video progress periodically
            if current_time - last_progress_check > 10:  # Every 10 seconds
                self._check_video_progress(video_element, elapsed)
                last_progress_check = current_time

            # Random actions during watching (more frequent and realistic)
            action_chance = random.random()

            if action_chance > 0.85:  # 15% chance - mouse movement
                self._random_mouse_movement()
            elif action_chance > 0.75:  # 10% chance - scrolling
                self._random_scroll()
            elif action_chance > 0.92:  # 8% chance - pause/resume
                self._pause_and_resume(video_element)
            elif action_chance > 0.96:  # 4% chance - volume adjustment
                self._adjust_volume()
            elif action_chance > 0.98:  # 2% chance - seek within video
                self._random_seek(video_element, elapsed, watch_time)

            # Variable wait times (more human-like)
            if remaining > 30:
                wait_time = random.uniform(3, 12)  # Longer waits early in video
            else:
                wait_time = random.uniform(1, 5)   # Shorter waits near end

            time.sleep(min(wait_time, remaining))

        logging.debug(f"Completed {watch_time:.1f} second watch session")

    def _check_video_progress(self, video_element, elapsed_time):
        """
        Check that video is actually progressing (not stuck)
        """
        if not video_element:
            return

        try:
            current_time = self.driver.execute_script("return arguments[0].currentTime", video_element)
            is_paused = self.driver.execute_script("return arguments[0].paused", video_element)

            # If video seems stuck or paused, try to fix it
            if is_paused or current_time < elapsed_time * 0.5:
                logging.debug("Video seems paused or stuck, attempting to resume")
                video_element.click()
                time.sleep(1)

        except Exception as e:
            logging.debug(f"Could not check video progress: {e}")

    def _adjust_volume(self):
        """
        Randomly adjust volume (human-like behavior)
        """
        try:
            # Try to find volume controls
            volume_controls = self.driver.find_elements(By.CSS_SELECTOR,
                ".ytp-volume-panel, .ytp-mute-button")
            if volume_controls:
                volume_control = random.choice(volume_controls)
                volume_control.click()
                time.sleep(random.uniform(0.5, 1.5))
                logging.debug("Adjusted volume")
        except:
            pass  # Volume adjustment failed, not critical

    def _random_seek(self, video_element, elapsed_time, total_watch_time):
        """
        Occasionally seek to different parts of the video (realistic behavior)
        """
        if not video_element or elapsed_time < 10:  # Don't seek too early
            return

        try:
            duration = self.driver.execute_script("return arguments[0].duration", video_element)
            if duration and duration > 30:
                # Seek to a random position within reasonable bounds
                max_seek_pos = min(duration * 0.8, elapsed_time + 30)  # Don't seek too far ahead
                seek_position = random.uniform(10, max_seek_pos)

                self.driver.execute_script(f"arguments[0].currentTime = {seek_position}", video_element)
                time.sleep(random.uniform(1, 3))
                logging.debug(f"Seeked to position {seek_position:.1f}s")

        except Exception as e:
            logging.debug(f"Seek operation failed: {e}")

    def _random_engagement(self):
        """
        Randomly perform engagement actions (like, subscribe, etc.) - more realistic rates
        """
        # Wait a bit before engaging (more natural)
        time.sleep(random.uniform(2, 5))

        # Scroll down to see engagement buttons
        self._random_scroll()
        time.sleep(random.uniform(1, 2))

        # Moderate chance of liking (15% - more realistic)
        if random.random() > 0.85:
            self._try_like_video()

        # Small chance of subscribing (3% - more realistic)
        if random.random() > 0.97:
            self._try_subscribe()

        # Small chance of commenting (1%)
        if random.random() > 0.99:
            self._try_comment()

        # Chance of scrolling to read comments (30%)
        if random.random() > 0.7:
            self._browse_comments()

    def _try_like_video(self):
        """
        Try to like the video
        """
        try:
            # Multiple selectors for like button (YouTube changes these)
            like_selectors = [
                "button[aria-label*='like']:not([aria-label*='dislike'])",
                "#segmented-like-button button",
                "ytd-toggle-button-renderer button[aria-pressed='false']",
                ".ytd-video-primary-info-renderer button[aria-label*='like']"
            ]

            for selector in like_selectors:
                try:
                    like_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if like_button.is_displayed() and like_button.is_enabled():
                        # Scroll to button if needed
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
                        time.sleep(random.uniform(0.5, 1))

                        like_button.click()
                        time.sleep(random.uniform(1, 3))
                        logging.debug("Liked the video")
                        return
                except:
                    continue

        except Exception as e:
            logging.debug(f"Could not like video: {e}")

    def _try_subscribe(self):
        """
        Try to subscribe to the channel
        """
        try:
            subscribe_selectors = [
                "button[aria-label*='Subscribe']",
                "#subscribe-button button",
                "ytd-subscribe-button-renderer button",
                ".ytd-video-owner-renderer button[aria-label*='Subscribe']"
            ]

            for selector in subscribe_selectors:
                try:
                    subscribe_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if (subscribe_button.is_displayed() and
                        subscribe_button.is_enabled() and
                        "Subscribe" in subscribe_button.get_attribute("aria-label")):

                        # Scroll to button
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", subscribe_button)
                        time.sleep(random.uniform(0.5, 1))

                        subscribe_button.click()
                        time.sleep(random.uniform(2, 4))
                        logging.debug("Subscribed to channel")
                        return
                except:
                    continue

        except Exception as e:
            logging.debug(f"Could not subscribe: {e}")

    def _try_comment(self):
        """
        Try to add a comment (very rarely)
        """
        try:
            # Scroll down to comments section
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(2, 4))

            # Find comment box
            comment_box = self.driver.find_element(By.CSS_SELECTOR,
                "#placeholder-area, #contenteditable-root")

            if comment_box.is_displayed():
                comment_box.click()
                time.sleep(random.uniform(1, 2))

                # Simple generic comments
                comments = ["Nice video!", "Great content", "Thanks for sharing", "👍", "Good job"]
                comment_text = random.choice(comments)

                comment_box.send_keys(comment_text)
                time.sleep(random.uniform(2, 4))

                # Try to find and click comment button
                comment_button = self.driver.find_element(By.CSS_SELECTOR,
                    "#submit-button button, button[aria-label*='Comment']")
                comment_button.click()

                logging.debug(f"Posted comment: {comment_text}")

        except Exception as e:
            logging.debug(f"Could not comment: {e}")

    def _browse_comments(self):
        """
        Scroll through and read comments (realistic behavior)
        """
        try:
            # Scroll to comments section
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(2, 4))

            # Random scrolling through comments
            for _ in range(random.randint(2, 5)):
                self._random_scroll()
                time.sleep(random.uniform(1, 3))

            logging.debug("Browsed comments")

        except Exception as e:
            logging.debug(f"Could not browse comments: {e}")

    def _random_scroll(self):
        """
        Perform random scrolling behavior
        """
        scroll_amount = random.randint(100, 500)
        direction = random.choice([1, -1])  # Up or down
        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount * direction})")
        time.sleep(random.uniform(0.5, 1.5))

    def _random_mouse_movement(self):
        """
        Perform random mouse movements
        """
        try:
            actions = ActionChains(self.driver)
            for _ in range(random.randint(1, 3)):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset)
            actions.perform()
        except:
            pass  # Mouse movement failed, not critical

    def _pause_and_resume(self, video_element=None):
        """
        Occasionally pause and resume the video (very human-like)
        """
        try:
            if not video_element:
                video_element = self.driver.find_element(By.TAG_NAME, "video")

            # Check if video is currently playing
            is_paused = self.driver.execute_script("return arguments[0].paused", video_element)

            if not is_paused:  # Only pause if currently playing
                video_element.click()  # Pause
                pause_duration = random.uniform(2, 12)  # Pause for 2-12 seconds
                logging.debug(f"Paused video for {pause_duration:.1f} seconds")
                time.sleep(pause_duration)
                video_element.click()  # Resume
                time.sleep(random.uniform(0.5, 2))  # Brief wait after resume
                logging.debug("Resumed video")

        except Exception as e:
            logging.debug(f"Pause/resume failed: {e}")

    def _cleanup(self):
        """
        Clean up browser resources
        """
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass  # Driver already closed