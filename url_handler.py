# url_handler.py

import webbrowser
import re
from config import REJECT_URLS

def filter_urls(content):
    """ Extract and filter URLs from the email content based on the REJECT_URLS list. """
    urls = set()
    # Regex pattern to find URLs
    pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    matches = re.findall(pattern, content)
    for url in matches:
        if url not in REJECT_URLS:
            urls.add(url)
    return list(urls)

def open_url(url):
    """ Open a URL in the default web browser. """
    try:
        webbrowser.open(url, new=2)  # Open in a new tab, if possible
        return True
    except Exception as e:
        print(f"Failed to open URL: {url}. Error: {e}")
        return False

if __name__ == "__main__":
    # Example content with URL for testing
    test_content = "Check out the project at https://github.com/example/project. Do not visit http://malicious-site.com."
    filtered_urls = filter_urls(test_content)
    print("Filtered URLs:", filtered_urls)
    if filtered_urls:
        open_url(filtered_urls[0])  # Open the first valid URL
