#!/usr/bin/env python3
"""Search for new competitor candidates using available search result files."""
import csv
import re
import sys
import os

def load_existing():
    """Load all websites already in the CSV."""
    already = set()
    with open('concurrentie_onderzoek.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            site = row.get('website', '').strip().lower().replace('www.', '')
            if site:
                already.add(site)
    return already

def extract_urls_from_file(filepath):
    """Extract potential company URLs from search result HTML files."""
    urls = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r'href=["\']https?://([^"/\s#]+\.nl)[^"\']*["\']'
        found = re.findall(pattern, content)
        urls.extend(found)
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return urls

def main():
    already = load_existing()
    print(f"Companies already analyzed: {len(already)}")
    
    # Extract from search result files
    search_files = ['bing_results.txt', 'google_results.txt', 'duckduckgo_results.txt']
    candidate_urls = set()
    for sf in search_files:
        urls = extract_urls_from_file(sf)
        print(f"Found {len(urls)} .nl URLs in {sf}", file=sys.stderr)
        candidate_urls.update(urls)
    
    # Also try to find domains mentioned in FINDINGS markdown files
    findings_dir = 'FINDINGS'
    for fname in os.listdir(findings_dir):
        if fname.endswith('.md'):
            with open(os.path.join(findings_dir, fname), 'r', encoding='utf-8') as f:
                content = f.read()
            domains = re.findall(r'(\w+\.nl)', content)
            candidate_urls.update(domains)
    
    # Filter: remove already analyzed, remove known non-company domains
    skip_domains = {
        'robots.txt', 'sitemap.xml', 'google', 'wikipedia', 'linkedin',
        'facebook', 'twitter', 'youtube', 'instagram', 'pinterest',
        'vk.com', 'blogspot', 'wordpress', 'tumblr', 'medium.com',
        'github', 'stackoverflow', 'amazon', 'ebay', 'marktplaats',
        'werkspot', 'bouwbedrijvengids', 'klarna', 'trustpilot'
    }
    
    new_candidates = []
    for url in sorted(candidate_urls):
        if url not in already and url not in skip_domains:
            if re.match(r'^[a-z0-9][a-z0-9-]*\.nl$', url):
                new_candidates.append(url)
    
    print(f"\nNew candidates found (not yet analyzed): {len(new_candidates)}")
    for c in new_candidates:
        print(f"  - {c}")

if __name__ == '__main__':
    main()
