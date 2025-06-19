import unittest
from src.scraper.web_scraper import WebScraper
from src.scraper.content_parser import ContentParser

class TestWebScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraper()

    def test_scrape_article(self):
        url = "https://example.com/help/article"
        html_content = self.scraper.scrape_article(url)
        self.assertIn("<html>", html_content)  # Basic check for HTML content

class TestContentParser(unittest.TestCase):
    def setUp(self):
        self.parser = ContentParser()

    def test_parse_content(self):
        html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        parsed_data = self.parser.parse_content(html)
        self.assertEqual(parsed_data['title'], "Title")
        self.assertEqual(parsed_data['content'], "Content")

if __name__ == '__main__':
    unittest.main()