class ContentParser:
    def parse_content(self, html, url=None):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])

        return {
            'title': title,
            'content': content,
            'url': url,
            'summary': content[:500] + '...' if len(content) > 500 else content
        }