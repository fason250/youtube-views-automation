import time
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta

class SafetyController:
    """
    Intelligent safety system that automatically adjusts timing and distribution
    to avoid detection while maximizing efficiency.
    """
    
    def __init__(self):
        # Safety limits
        self.MAX_VIEWS_PER_IP = 3
        self.MIN_SECONDS_BETWEEN_VIEWS = 90  # 1.5 minutes minimum
        self.MAX_VIEWS_PER_HOUR = 2000  # Conservative hourly limit
        self.MIN_GEO_DIVERSITY = 0.7  # 70% geographic diversity
        
        # Tracking
        self.ip_usage = defaultdict(int)
        self.ip_last_used = defaultdict(float)
        self.hourly_views = deque()  # Track views per hour
        self.country_distribution = defaultdict(int)
        self.total_views_attempted = 0
        
    def calculate_safe_timing(self, target_views):
        """
        Calculate optimal timing and concurrency for the given view count
        """
        # Base calculations
        min_time_needed = (target_views * self.MIN_SECONDS_BETWEEN_VIEWS) / 3600  # hours
        
        # Adjust for hourly limits
        hours_needed_for_rate = target_views / self.MAX_VIEWS_PER_HOUR
        
        # Take the longer of the two
        estimated_hours = max(min_time_needed, hours_needed_for_rate)
        
        # Calculate optimal concurrency
        # We want to spread views out but not too slowly
        if target_views <= 1000:
            max_concurrent = max(1, min(10, target_views // 10))  # Ensure at least 1
            delay_between_views = 2.0  # 2 seconds between submissions
        elif target_views <= 10000:
            max_concurrent = max(1, min(25, target_views // 20))  # Ensure at least 1
            delay_between_views = 1.5
        else:
            max_concurrent = max(1, min(50, target_views // 50))  # Ensure at least 1
            delay_between_views = 1.0

        # For very small view counts, use 1 thread
        if target_views < 10:
            max_concurrent = 1
        
        # Ensure we don't exceed hourly limits
        views_per_hour_planned = (3600 / delay_between_views) * max_concurrent
        if views_per_hour_planned > self.MAX_VIEWS_PER_HOUR:
            # Adjust delay to stay within limits
            delay_between_views = (3600 * max_concurrent) / self.MAX_VIEWS_PER_HOUR
        
        return {
            'estimated_hours': estimated_hours,
            'max_concurrent': max_concurrent,
            'delay_between_views': delay_between_views,
            'views_per_hour': min(views_per_hour_planned, self.MAX_VIEWS_PER_HOUR)
        }
    
    def is_view_safe(self, ip_address):
        """
        Check if it's safe to use this IP for a view right now
        """
        current_time = time.time()
        
        # Check IP usage limit
        if self.ip_usage[ip_address] >= self.MAX_VIEWS_PER_IP:
            return False
        
        # Check time since last use
        last_used = self.ip_last_used.get(ip_address, 0)
        if current_time - last_used < self.MIN_SECONDS_BETWEEN_VIEWS:
            return False
        
        # Check hourly rate limit
        if self._get_current_hourly_rate() >= self.MAX_VIEWS_PER_HOUR:
            return False
        
        return True
    
    def record_successful_view(self, ip_address, country):
        """
        Record a successful view for tracking and safety monitoring
        """
        current_time = time.time()
        
        # Update IP tracking
        self.ip_usage[ip_address] += 1
        self.ip_last_used[ip_address] = current_time
        
        # Update geographic distribution
        self.country_distribution[country] += 1
        
        # Update hourly tracking
        self.hourly_views.append(current_time)
        self._cleanup_old_hourly_data()
        
        self.total_views_attempted += 1
        
        # Log safety metrics periodically
        if self.total_views_attempted % 100 == 0:
            self._log_safety_metrics()
    
    def _get_current_hourly_rate(self):
        """
        Get the number of views in the last hour
        """
        self._cleanup_old_hourly_data()
        return len(self.hourly_views)
    
    def _cleanup_old_hourly_data(self):
        """
        Remove view records older than 1 hour
        """
        cutoff_time = time.time() - 3600  # 1 hour ago
        while self.hourly_views and self.hourly_views[0] < cutoff_time:
            self.hourly_views.popleft()
    
    def _log_safety_metrics(self):
        """
        Log current safety metrics for monitoring
        """
        geo_diversity = self._calculate_geo_diversity()
        hourly_rate = self._get_current_hourly_rate()
        unique_ips = len(self.ip_usage)
        
        logging.info(f"Safety Metrics - Views: {self.total_views_attempted}, "
                    f"Hourly Rate: {hourly_rate}, "
                    f"Unique IPs: {unique_ips}, "
                    f"Geo Diversity: {geo_diversity:.2f}")
        
        # Warn if approaching limits
        if hourly_rate > self.MAX_VIEWS_PER_HOUR * 0.8:
            logging.warning("Approaching hourly rate limit")
        
        if geo_diversity < self.MIN_GEO_DIVERSITY:
            logging.warning(f"Low geographic diversity: {geo_diversity:.2f}")
    
    def _calculate_geo_diversity(self):
        """
        Calculate geographic diversity score (0-1)
        """
        if not self.country_distribution:
            return 0.0
        
        total_views = sum(self.country_distribution.values())
        unique_countries = len(self.country_distribution)
        
        # Simple diversity metric: unique countries / total views
        # Higher is better, max is 1.0 (each view from different country)
        return min(1.0, unique_countries / total_views)
    
    def get_safety_report(self):
        """
        Get a comprehensive safety report
        """
        return {
            'total_views': self.total_views_attempted,
            'unique_ips_used': len(self.ip_usage),
            'current_hourly_rate': self._get_current_hourly_rate(),
            'geo_diversity': self._calculate_geo_diversity(),
            'countries_represented': len(self.country_distribution),
            'ip_usage_distribution': dict(self.ip_usage),
            'country_distribution': dict(self.country_distribution)
        }
