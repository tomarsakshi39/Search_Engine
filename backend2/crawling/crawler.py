# crawling/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import os

def extract_text(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup.get_text(separator=' ')

def get_links(soup, base_url):
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not urlparse(href).netloc:
            href = urljoin(base_url, href)
        if urlparse(base_url).netloc in urlparse(href).netloc:
            links.add(href)
    return links

def crawl(url, max_depth=1):
    visited = set()
    to_visit = [(url, 0)]
    crawled_data = []

    while to_visit:
        current_url, depth = to_visit.pop(0)
        if current_url not in visited and depth <= max_depth:
            print(f"Crawling: {current_url} (Depth: {depth})")
            try:
                response = requests.get(current_url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                text = extract_text(soup)
                crawled_data.append((current_url, text))
                visited.add(current_url)

                if depth < max_depth:
                    links = get_links(soup, current_url)
                    to_visit.extend((link, depth + 1) for link in links if link not in visited)
            except requests.RequestException as e:
                print(f"Failed to crawl: {current_url}, due to {e}")

            time.sleep(1)

    return crawled_data

def save_crawled_data(crawled_data, filename="crawled_data.json"):
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(crawled_data, file, ensure_ascii=False, indent=4)
