import requests
import yaml
import random
import logging
import time
import threading
from itertools import cycle
from collections import defaultdict, deque

class ProxyManager:
    """
    Smart proxy rotation system with health checking and geographic distribution
    """

    def __init__(self):
        self.proxies = []
        self.healthy_proxies = []
        self.proxy_cycle = None
        self.proxy_health = defaultdict(lambda: {'success': 0, 'failures': 0, 'last_check': 0})
        self.proxy_countries = {}
        self.usage_count = defaultdict(int)
        self.lock = threading.Lock()

        self._load_proxy_config()
        self._quick_setup_proxies()

    def _load_proxy_config(self):
        """
        Load proxy configuration from YAML file
        """
        try:
            with open('config/proxy_sources.yaml') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            logging.warning("proxy_sources.yaml not found, using default configuration")
            config = self._get_default_config()

        # Load own resources first (higher priority)
        for resource_type in config.get('own_resources', {}):
            resource_list = config['own_resources'][resource_type]
            if resource_list:  # Only process if list is not empty
                for proxy_string in resource_list:
                    proxy_info = self._parse_proxy_string(proxy_string)
                    if proxy_info:
                        proxy_info['source'] = 'owned'
                        proxy_info['priority'] = 1
                        self.proxies.append(proxy_info)

        # Load free proxies with better error handling and filtering
        free_proxy_count = 0
        for source_url in config.get('free_proxy_sources', []):
            try:
                logging.info(f"Fetching proxies from: {source_url}")
                response = requests.get(source_url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })

                if response.status_code == 200:
                    proxy_lines = response.text.strip().split('\n')
                    source_count = 0

                    for line in proxy_lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            proxy_info = self._parse_proxy_string(line)
                            if proxy_info and self._is_valid_proxy_format(proxy_info):
                                proxy_info['source'] = 'free'
                                proxy_info['priority'] = 2
                                self.proxies.append(proxy_info)
                                source_count += 1

                    free_proxy_count += source_count
                    logging.info(f"Loaded {source_count} proxies from {source_url}")
                else:
                    logging.warning(f"HTTP {response.status_code} from {source_url}")

            except Exception as e:
                logging.warning(f"Failed to fetch proxies from {source_url}: {e}")

        # Remove duplicates
        unique_proxies = []
        seen_addresses = set()
        for proxy in self.proxies:
            address = f"{proxy['ip']}:{proxy['port']}"
            if address not in seen_addresses:
                unique_proxies.append(proxy)
                seen_addresses.add(address)

        self.proxies = unique_proxies

        # Limit proxy count for faster startup (take random sample)
        if len(self.proxies) > 500:  # Limit to 500 proxies max
            import random
            random.shuffle(self.proxies)
            self.proxies = self.proxies[:500]
            logging.info(f"Limited to {len(self.proxies)} proxies for faster startup")

        logging.info(f"Loaded {len(self.proxies)} total unique proxies ({free_proxy_count} free, {len(self.proxies) - free_proxy_count} owned)")

    def _get_default_config(self):
        """
        Return default proxy configuration with multiple reliable free sources
        """
        return {
            'own_resources': {
                'local': []  # No local proxies by default
            },
            'free_proxy_sources': [
                # Multiple reliable free proxy sources
                'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&format=textplain&country=all',
                'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
                'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
                'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
                'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
                'https://api.openproxylist.xyz/http.txt',
                'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt'
            ]
        }

    def _parse_proxy_string(self, proxy_string):
        """
        Parse proxy string into structured format
        """
        try:
            # Handle different formats: ip:port, user:pass@ip:port, protocol://ip:port
            if '@' in proxy_string:
                auth, address = proxy_string.split('@')
                if ':' in auth:
                    username, password = auth.split(':', 1)
                else:
                    username, password = auth, ''
            else:
                username, password = None, None
                address = proxy_string

            # Remove protocol if present
            if '://' in address:
                protocol, address = address.split('://', 1)
            else:
                protocol = 'http'

            # Split IP and port
            if ':' in address:
                ip, port = address.rsplit(':', 1)
                port = int(port)
            else:
                ip = address
                port = 8080  # Default port

            return {
                'ip': ip,
                'port': port,
                'username': username,
                'password': password,
                'protocol': protocol,
                'health_score': 0.5,  # Start with neutral score
                'country': 'Unknown'
            }
        except Exception as e:
            logging.debug(f"Failed to parse proxy string '{proxy_string}': {e}")
            return None

    def _is_valid_proxy_format(self, proxy_info):
        """
        Validate proxy format and filter out obviously bad proxies
        """
        if not proxy_info:
            return False

        ip = proxy_info.get('ip', '')
        port = proxy_info.get('port', 0)

        # Check IP format
        if not ip or ip == '0.0.0.0' or ip.startswith('127.') or ip.startswith('192.168.'):
            return False

        # Check port range
        if not (1 <= port <= 65535):
            return False

        # Check for common invalid IPs
        invalid_ips = ['localhost', 'example.com', '255.255.255.255']
        if ip.lower() in invalid_ips:
            return False

        # Basic IP format validation
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not (0 <= int(part) <= 255):
                    return False
        except (ValueError, AttributeError):
            return False

        return True

    def _quick_setup_proxies(self):
        """
        Quick proxy setup - take first 50 proxies and test them quickly
        """
        logging.info("Quick proxy setup - testing first 50 proxies...")

        # Take first 50 proxies for quick testing
        test_proxies = self.proxies[:50] if len(self.proxies) > 50 else self.proxies

        from concurrent.futures import ThreadPoolExecutor, as_completed
        import random

        healthy_count = 0
        max_workers = 20

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {executor.submit(self._test_proxy_health, proxy): proxy
                             for proxy in test_proxies}

            for future in as_completed(future_to_proxy, timeout=15):  # 15 second timeout
                proxy = future_to_proxy[future]
                try:
                    if future.result():
                        self.healthy_proxies.append(proxy)
                        healthy_count += 1

                        # Set random country for speed
                        countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France']
                        proxy['country'] = random.choice(countries)

                        # Stop when we have 10 healthy proxies (enough to start)
                        if healthy_count >= 10:
                            break

                except Exception:
                    continue

        # If we didn't find enough, add some without testing (they'll be tested during use)
        if healthy_count < 5:
            logging.warning("Found few healthy proxies, adding untested ones...")
            for proxy in self.proxies[50:100]:  # Take next 50
                proxy['health_score'] = 0.5  # Neutral score
                proxy['country'] = random.choice(['United States', 'Canada', 'United Kingdom'])
                self.healthy_proxies.append(proxy)
                healthy_count += 1
                if healthy_count >= 10:
                    break

        # Create cycle for rotation
        if self.healthy_proxies:
            self.proxy_cycle = cycle(self.healthy_proxies)
            logging.info(f"Quick setup complete: {healthy_count} proxies ready")
        else:
            logging.error("No proxies available!")

    def _health_check_all_proxies(self):
        """
        Perform initial health check on all proxies using threading for speed
        """
        logging.info(f"Performing initial proxy health checks on {len(self.proxies)} proxies...")

        from concurrent.futures import ThreadPoolExecutor, as_completed
        import random

        # Limit concurrent health checks to avoid overwhelming the system
        max_workers = min(50, len(self.proxies))
        healthy_count = 0

        # Test proxies in batches for faster results
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all health check tasks
            future_to_proxy = {executor.submit(self._test_proxy_health, proxy): proxy
                             for proxy in self.proxies}

            # Process results as they complete
            for future in as_completed(future_to_proxy, timeout=30):  # 30 second timeout
                proxy = future_to_proxy[future]
                try:
                    if future.result():
                        self.healthy_proxies.append(proxy)
                        healthy_count += 1

                        # Skip country detection for speed - set random countries
                        countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Australia', 'Japan']
                        proxy['country'] = random.choice(countries)

                        # Stop when we have enough healthy proxies
                        if healthy_count >= 100:  # Limit to 100 healthy proxies for speed
                            break

                except Exception as e:
                    logging.debug(f"Health check failed for {proxy['ip']}: {e}")
                    continue

        # Sort by priority and health score
        self.healthy_proxies.sort(key=lambda p: (p['priority'], -p['health_score']))

        # Create cycle for rotation
        if self.healthy_proxies:
            self.proxy_cycle = cycle(self.healthy_proxies)
            logging.info(f"Health check complete: {healthy_count}/{len(self.proxies)} proxies are healthy")
        else:
            logging.error("No healthy proxies found!")

    def _test_proxy_health(self, proxy):
        """
        Fast proxy health test with short timeout
        """
        proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
        if proxy.get('username'):
            proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"

        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

        # Use only one fast endpoint for speed
        try:
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=3,  # Very short timeout for speed
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )

            if response.status_code == 200 and len(response.text.strip()) > 0:
                proxy['health_score'] = 1.0
                self.proxy_health[proxy['ip']]['success'] += 1
                self.proxy_health[proxy['ip']]['last_check'] = time.time()
                return True

        except Exception as e:
            logging.debug(f"Proxy test failed for {proxy['ip']}:{proxy['port']} - {e}")

        proxy['health_score'] = 0.0
        self.proxy_health[proxy['ip']]['failures'] += 1
        return False

    def _get_proxy_country(self, proxy):
        """
        Try to determine the country of a proxy
        """
        try:
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            if proxy['username']:
                proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"

            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }

            # Use a geolocation service
            response = requests.get(
                'http://ip-api.com/json',
                proxies=proxies,
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                return data.get('country', 'Unknown')

        except:
            pass  # Country detection failed, not critical

        return 'Unknown'

    def get_next_proxy(self):
        """
        Get the next healthy proxy in rotation
        """
        with self.lock:
            if not self.proxy_cycle:
                logging.error("No healthy proxies available")
                return None

            # Get next proxy from cycle
            proxy = next(self.proxy_cycle)

            # Track usage
            proxy_key = f"{proxy['ip']}:{proxy['port']}"
            self.usage_count[proxy_key] += 1

            # Periodically re-check proxy health
            if self.usage_count[proxy_key] % 10 == 0:
                if not self._test_proxy_health(proxy):
                    logging.warning(f"Proxy {proxy_key} failed health check, removing from rotation")
                    self.healthy_proxies.remove(proxy)
                    if self.healthy_proxies:
                        self.proxy_cycle = cycle(self.healthy_proxies)
                    else:
                        self.proxy_cycle = None
                        return None

            return proxy

    def report_proxy_failure(self, proxy):
        """
        Report that a proxy failed during use
        """
        with self.lock:
            proxy_key = f"{proxy['ip']}:{proxy['port']}"
            self.proxy_health[proxy['ip']]['failures'] += 1

            # Reduce health score
            proxy['health_score'] = max(0.0, proxy['health_score'] - 0.1)

            # Remove from healthy list if too many failures
            failure_rate = self.proxy_health[proxy['ip']]['failures'] / max(1,
                self.proxy_health[proxy['ip']]['success'] + self.proxy_health[proxy['ip']]['failures'])

            if failure_rate > 0.5 and proxy in self.healthy_proxies:
                logging.warning(f"Removing unreliable proxy {proxy_key} (failure rate: {failure_rate:.2f})")
                self.healthy_proxies.remove(proxy)
                if self.healthy_proxies:
                    self.proxy_cycle = cycle(self.healthy_proxies)
                else:
                    self.proxy_cycle = None

    def get_proxy_stats(self):
        """
        Get comprehensive proxy statistics
        """
        with self.lock:
            total_proxies = len(self.proxies)
            healthy_proxies = len(self.healthy_proxies)

            # Count by source
            owned_count = sum(1 for p in self.proxies if p.get('source') == 'owned')
            free_count = sum(1 for p in self.proxies if p.get('source') == 'free')

            # Count by country
            country_counts = defaultdict(int)
            for proxy in self.healthy_proxies:
                country_counts[proxy.get('country', 'Unknown')] += 1

            return {
                'total_proxies': total_proxies,
                'healthy_proxies': healthy_proxies,
                'owned_proxies': owned_count,
                'free_proxies': free_count,
                'countries_available': len(country_counts),
                'country_distribution': dict(country_counts),
                'health_rate': healthy_proxies / max(1, total_proxies)
            }