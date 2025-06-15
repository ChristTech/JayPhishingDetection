import json
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse

class Whitelist:
    def __init__(self):
        self.whitelist_file = 'whitelist.json'
        self.temp_whitelist = {}  # Store temporary whitelisted URLs with expiry
        self.whitelist = self._load_whitelist()

    def _load_whitelist(self):
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                return json.load(f)
        return {"safe_urls": []}

    def save_whitelist(self):
        with open(self.whitelist_file, 'w') as f:
            json.dump(self.whitelist, f, indent=2)

    def add_url(self, url, temporary=False):
        if temporary:
            # Add to temporary whitelist with 24-hour expiry
            expiry_time = datetime.now() + timedelta(hours=24)
            self.temp_whitelist[url] = expiry_time.timestamp()
            return True
        else:
            # Add to permanent whitelist
            domain = self._get_domain(url)
            if not any(domain == self._get_domain(white_url) 
                      for white_url in self.whitelist["safe_urls"]):
                self.whitelist["safe_urls"].append(url)
                self.save_whitelist()
                return True
        return False

    def _get_domain(self, url):
        """Extract main domain from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        return domain.replace('www.', '')

    def is_whitelisted(self, url):
        domain = self._get_domain(url)
        for white_url in self.whitelist["safe_urls"]:
            white_domain = self._get_domain(white_url)
            if domain == white_domain:
                return True
        
        # Check temporary whitelist
        if url in self.temp_whitelist:
            expiry_time = self.temp_whitelist[url]
            if datetime.now().timestamp() < expiry_time:
                return True
            else:
                # Remove expired entry
                del self.temp_whitelist[url]
        return False

    def cleanup_temp_whitelist(self):
        # Remove expired temporary entries
        current_time = datetime.now().timestamp()
        expired_urls = [url for url, expiry in self.temp_whitelist.items() 
                       if current_time > expiry]
        for url in expired_urls:
            del self.temp_whitelist[url]