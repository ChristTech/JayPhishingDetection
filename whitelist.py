import json
import os
from datetime import datetime, timedelta

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
            if url not in self.whitelist["safe_urls"]:
                self.whitelist["safe_urls"].append(url)
                self.save_whitelist()
                return True
        return False

    def is_whitelisted(self, url):
        # Check permanent whitelist
        if url in self.whitelist["safe_urls"]:
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