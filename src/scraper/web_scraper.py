import requests
from typing import Optional

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MCP Documentation Scraper/1.0'
        })

    def scrape_article(self, url: str) -> str:
        """Scrape an article from a URL"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"Failed to retrieve article from {url}, status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"Error scraping {url}: {str(e)}")