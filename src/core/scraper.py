"""
Web Scraper Utility

Helper functions to detect URLs in text and scrape the main content
from them to provide as context to the LLM.
"""

import re
import requests
from bs4 import BeautifulSoup

def extract_urls(text: str) -> list[str]:
    """Find all URLs in a given text using regex."""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.findall(text)

def fetch_and_extract_text(url: str) -> str:
    """Fetch a URL and extract text from paragraphs."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # Extract text from p tags as they usually contain the main article body
        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text() for p in paragraphs)

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Truncate string if too long to save tokens (e.g. 5000 chars)
        max_chars = 5000
        if len(text) > max_chars:
            text = text[:max_chars] + "...\n[Content Truncated]"

        return text

    except Exception as e:
        print(f"  ⚠️ Warning: Failed to scrape {url}. Error: {e}")
        return ""

def get_scraped_context(text: str) -> str:
    """Extracts URLs from text, scrapes them, and combines the text."""
    urls = extract_urls(text)
    if not urls:
        return ""

    context = ""
    for url in urls:
        print(f"  🕸️ Scraping context from: {url}")
        article_text = fetch_and_extract_text(url)
        if article_text:
             context += f"\n--- Content from {url} ---\n{article_text}\n"

    return context
