#!/usr/bin/env python3
"""Extract clean readable text from a web article URL.

Examples:
    python 06_scrape_article.py --url https://example.com/article --output article.txt
"""
import argparse
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' is required.", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: 'beautifulsoup4' is required.", file=sys.stderr)
    sys.exit(1)

SKIP_TAGS = ["script", "style", "nav", "footer", "header", "aside"]

def fetch_text(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ArticleScraper/1.0)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(SKIP_TAGS):
        tag.decompose()
    title = soup.find("title")
    if title and title.get_text(strip=True):
        yield f"# {title.get_text(strip=True)}\n"
    article = soup.find("article") or soup.find("main") or soup
    for el in article.find_all(["h1", "h2", "h3", "p", "li"]):
        text = el.get_text(separator=" ", strip=True)
        if text:
            yield text

def main(url, output):
    try:
        lines = list(fetch_text(url))
    except requests.RequestException as exc:
        print(f"Error fetching URL: {exc}", file=sys.stderr)
        return 1
    content = "\n\n".join(lines)
    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"Article saved to {output} ({len(content)} chars).")
    else:
        print(content)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from web article.")
    parser.add_argument("--url", required=True, help="Article URL")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()
    sys.exit(main(args.url, args.output))
