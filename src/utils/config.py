import os

class Config:
    BASE_URL = "https://example.com/docs"
    CACHE_DIR = os.path.join(os.getcwd(), "cache")
    DATABASE_URL = "sqlite:///local_cache.db"
    USER_AGENT = "MCP Doc Scraper/1.0"
    TIMEOUT = 10  # seconds
    MAX_RETRIES = 3

    @staticmethod
    def get_cache_file_path(doc_id):
        return os.path.join(Config.CACHE_DIR, f"{doc_id}.json")