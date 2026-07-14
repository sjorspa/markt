#!/usr/bin/env python3
"""Search for new competitors in Amsterdam region using DuckDuckGo and Bing."""

import urllib.request
import urllib.parse
import json
import time
import re
import sys

def load_existing_domains():
    """Load existing domains from CSV."""
    existing = set()
    with open('concurrentie_onderzoek.csv') as f:
        for line in f:
            if line.startswith('bedrijfsnaam'):
                continue
            parts = line.strip().split(';')
            if len(parts) >= 2 and parts[1]:
                existing.add(parts[1].strip())
    return existing

def search_ddg(query, max_results=30):
    """Search DuckDuckGo for a query."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        response = urllib.request.urlopen(req, timeout=15)
        html = response.read().decode('utf-8')
        
        # Extract results
        results = []
        pattern = r'<a class="result__a" href="([^"]+)"[^>]*>(.*?)</a>'
        links = re.findall(pattern, html, re.DOTALL)
        
        snippet_pattern = r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>'
        snippets = re.findall(snippet_pattern, html, re.DOTALL)
        
        for (link, title), snippet in zip(links, snippets):
            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            if title and link:
                results.append({'title': title, 'url': link, 'snippet': snippet})
        
        return results[:max_results]
    except Exception as e:
        print(f"  DuckDuckGo error for '{query}': {e}", file=sys.stderr)
        return []

def search_bing(query, max_results=30):
    """Search Bing for a query."""
    try:
        url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        response = urllib.request.urlopen(req, timeout=15)
        html = response.read().decode('utf-8')
        
        results = []
        pattern = r'<h2><a href="([^"]+)"[^>]*>.*?</a></h2>.*?<p class="b_algo">(.*?)</p>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        for link, snippet in matches:
            title = re.sub(r'<[^>]+>', '', link.split('/')[-1] if '/' in link else 'result').strip()
            snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            if link and not link.startswith('#') and not link.startswith('javascript:'):
                results.append({'title': title, 'url': link, 'snippet': snippet})
        
        return results[:max_results]
    except Exception as e:
        print(f"  Bing error for '{query}': {e}", file=sys.stderr)
        return []

def extract_domain(url):
    """Extract domain from URL."""
    url = url.replace('https://', '').replace('http://', '')
    domain = url.split('/')[0]
    return domain.lower()

def main():
    existing = load_existing_domains()
    print(f"Loaded {len(existing)} existing domains")
    
    search_terms = [
        'dakdekker Amsterdam',
        'dakdekker Amstelveen',
        'dakdekker Haarlem',
        'dakdekker Almere',
        'dakdekker Diemen',
        'dakdekker Hilversum',
        'zinkwerker Amsterdam',
        'zinkwerk specialist',
        'dakrenovatie Amsterdam',
        'daklekkage reparatie Amsterdam',
        'dakgoten specialist Amsterdam',
        'EPDM dakbedekking Amsterdam',
        'bitumen dak Amsterdam',
        'loodgieter dakbedekking Amsterdam',
        'leien dak Amsterdam',
        'platte daken Amsterdam',
        'dakdekker Velsen',
        'dakdekker Beverwijk',
        'dakdekker Purmerend',
        'dakdekker Alkmaar',
        'dakdekker Weesp',
        'dakdekker Huizen',
        'dakdekker Bussum',
        'dakdekker Naarden',
        'dakdekker Laren',
        'dakdekker Blarum',
        'dakdekker Muiden',
        'dakdekker Castricum',
        'dakdekker Heemstede',
        'dakdekker Bloemendaal',
        'dakdekker Zandvoort',
        'dakdekker Uithoorn',
        'dakdekker Mijdrecht',
        'dakdekker Edam',
        'dakdekker Wormerland',
        'dakdekker Waterland',
        'dakdekker Amsterdam Oost',
        'dakdekker Amsterdam West',
        'dakdekker Amsterdam Noord',
        'dakdekker Amsterdam Zuid',
        'dakdekker Amsterdam Zuidoost',
        'dakdekker Amsterdam Nieuw-West',
    ]
    
    all_results = []
    for i, term in enumerate(search_terms):
        print(f"Searching ({i+1}/{len(search_terms)}): {term}...", flush=True)
        results = search_ddg(term)
        if not results:
            results = search_bing(term)
        all_results.extend(results)
        time.sleep(0.5)
    
    # Extract unique domains
    candidates = {}
    for r in all_results:
        domain = extract_domain(r['url'])
        if domain and domain not in existing:
            candidates[domain] = r
    
    print(f"\nFound {len(candidates)} potential new competitors:")
    for domain, r in sorted(candidates.items()):
        print(f"  {domain} - {r['title']}")
    
    # Save candidates
    with open('FINDINGS/new_candidates.txt', 'w') as f:
        for domain, r in sorted(candidates.items()):
            f.write(f"{domain}|{r['title']}|{r['url']}\n")
    
    print(f"\nCandidates saved to FINDINGS/new_candidates.txt")
    return candidates

if __name__ == '__main__':
    main()
