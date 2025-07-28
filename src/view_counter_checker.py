import requests
import re
import time
import logging
from urllib.parse import urlparse, parse_qs

class ViewCountChecker:
    """
    Checks YouTube view counts to verify that views are actually being counted
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def extract_video_id(self, youtube_url):
        """
        Extract video ID from various YouTube URL formats including Shorts
        """
        try:
            parsed_url = urlparse(youtube_url)

            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                if parsed_url.path == '/watch':
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                elif parsed_url.path.startswith('/embed/'):
                    return parsed_url.path.split('/embed/')[1].split('?')[0]
                elif parsed_url.path.startswith('/shorts/'):
                    # Handle YouTube Shorts URLs like /shorts/VIDEO_ID
                    return parsed_url.path.split('/shorts/')[1].split('?')[0]
            elif parsed_url.hostname in ['youtu.be']:
                return parsed_url.path[1:].split('?')[0]

            # Try to extract from any URL containing v= parameter
            if 'v=' in youtube_url:
                match = re.search(r'v=([a-zA-Z0-9_-]{11})', youtube_url)
                if match:
                    return match.group(1)

            # Try to extract 11-character video ID from path
            match = re.search(r'/([a-zA-Z0-9_-]{11})', youtube_url)
            if match:
                return match.group(1)

        except Exception as e:
            logging.error(f"Failed to extract video ID from {youtube_url}: {e}")

        return None
    
    def get_current_view_count(self, youtube_url):
        """
        Get the current view count for a YouTube video
        """
        video_id = self.extract_video_id(youtube_url)
        if not video_id:
            logging.error(f"Could not extract video ID from URL: {youtube_url}")
            return None
        
        try:
            # Method 1: Try to get from YouTube page HTML
            view_count = self._get_views_from_page(video_id)
            if view_count is not None:
                return view_count
            
            # Method 2: Try alternative approach
            view_count = self._get_views_alternative(video_id)
            if view_count is not None:
                return view_count
                
            logging.warning(f"Could not retrieve view count for video {video_id}")
            return None
            
        except Exception as e:
            logging.error(f"Error getting view count for {video_id}: {e}")
            return None
    
    def _get_views_from_page(self, video_id):
        """
        Extract view count from YouTube page HTML
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            html = response.text
            
            # Try multiple patterns to find view count
            patterns = [
                r'"viewCount":"(\d+)"',
                r'"viewCountText":{"simpleText":"([\d,]+) views"}',
                r'"viewCountText":{"runs":\[{"text":"([\d,]+)"}',
                r'(\d+(?:,\d{3})*)\s+views',
                r'"viewCount":{"videoViewCountRenderer":{"viewCount":{"simpleText":"([\d,]+)"'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html)
                if match:
                    view_count_str = match.group(1)
                    # Remove commas and convert to int
                    view_count = int(view_count_str.replace(',', ''))
                    logging.debug(f"Found view count using pattern: {view_count}")
                    return view_count
            
            return None
            
        except Exception as e:
            logging.debug(f"Failed to get views from page for {video_id}: {e}")
            return None
    
    def _get_views_alternative(self, video_id):
        """
        Alternative method to get view count using oEmbed or other APIs
        """
        try:
            # Try YouTube oEmbed API
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = self.session.get(oembed_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # oEmbed doesn't provide view count, but confirms video exists
                logging.debug(f"Video exists: {data.get('title', 'Unknown')}")
            
            # For now, return None as we need the HTML method
            return None
            
        except Exception as e:
            logging.debug(f"Alternative method failed for {video_id}: {e}")
            return None
    
    def monitor_view_count_changes(self, youtube_url, initial_count=None, check_interval=300):
        """
        Monitor view count changes over time
        Returns a generator that yields (timestamp, view_count, change) tuples
        """
        if initial_count is None:
            initial_count = self.get_current_view_count(youtube_url)
            if initial_count is None:
                logging.error("Could not get initial view count")
                return
        
        last_count = initial_count
        logging.info(f"Starting view count monitoring. Initial count: {initial_count:,}")
        
        while True:
            time.sleep(check_interval)
            
            current_count = self.get_current_view_count(youtube_url)
            if current_count is not None:
                change = current_count - last_count
                timestamp = time.time()
                
                yield timestamp, current_count, change
                
                if change > 0:
                    logging.info(f"View count increased by {change:,} (now {current_count:,})")
                else:
                    logging.debug(f"View count unchanged: {current_count:,}")
                
                last_count = current_count
            else:
                logging.warning("Failed to get current view count")
    
    def verify_views_are_counting(self, youtube_url, expected_increase=1, timeout_minutes=30):
        """
        Verify that views are actually being counted by YouTube
        Returns True if views increased, False otherwise
        """
        initial_count = self.get_current_view_count(youtube_url)
        if initial_count is None:
            logging.error("Cannot verify view counting - unable to get initial count")
            return False
        
        logging.info(f"Initial view count: {initial_count:,}")
        logging.info(f"Waiting up to {timeout_minutes} minutes for {expected_increase} view increase...")
        
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        check_interval = 60  # Check every minute
        
        while time.time() - start_time < timeout_seconds:
            time.sleep(check_interval)
            
            current_count = self.get_current_view_count(youtube_url)
            if current_count is not None:
                increase = current_count - initial_count
                
                if increase >= expected_increase:
                    logging.info(f"✅ Views are being counted! Increased by {increase:,} (from {initial_count:,} to {current_count:,})")
                    return True
                else:
                    elapsed_minutes = (time.time() - start_time) / 60
                    logging.info(f"Checking... {elapsed_minutes:.1f}min elapsed, increase so far: {increase:,}")
            else:
                logging.warning("Failed to check current view count")
        
        logging.warning(f"❌ Views may not be counting properly. No significant increase detected in {timeout_minutes} minutes.")
        return False
