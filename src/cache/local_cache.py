import json
import os
from typing import Dict, Any, Optional

class LocalCache:
    def __init__(self, cache_file='cache/local_cache.json'):
        # Ensure cache directory exists
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def cache_document(self, doc_id: str, data: Dict[str, Any]):
        """Cache a document"""
        self.cache[doc_id] = data
        self.save_cache()

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a cached document"""
        return self.cache.get(doc_id)
    
    def get_cached_document(self, url: str) -> Optional[Dict[str, Any]]:
        """Get a cached document by URL (alias for get_document)"""
        return self.get_document(url)

    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def clear_cache(self):
        """Clear all cached documents"""
        self.cache = {}
        self.save_cache()
    
    def is_healthy(self) -> bool:
        """Check if the cache is healthy"""
        try:
            return os.path.exists(os.path.dirname(self.cache_file))
        except:
            return False