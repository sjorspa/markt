#!/usr/bin/env python3
"""Search Bing via HTTP (no SSL) and extract .nl domains."""
import http.client
import urllib.parse
import re

def search_bing(query, max_redirects=5):
    encoded = urllib.parse.quote(query, safe='')
    url = f'/search?q={encoded}'
    for i in range(max_redirects):
        conn = http.client.HTTPConnection('www.bing.com', timeout=10)
        conn.request('GET', url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'nl-NL,nl;q=0.9,en;q=0.7',
        })
        resp = conn.getresponse()
        status = resp.status
        if status in (301, 302, 303, 307, 308):
            location = resp.getheader('Location')
            if location:
                url = location
                continue
        html = resp.read().decode('utf-8', errors='replace')
        return html
    return None

# Load existing domains
existing = set()
with open('concurrentie_onderzoek.csv') as f:
    for line in f:
        if line.startswith('bedrijfsnaam'):
            continue
        parts = line.strip().split(';')
        if len(parts) >= 2 and parts[1]:
            existing.add(parts[1].strip().lower().replace('www.', ''))

search_terms = [
    'dakdekker Almere',
    'dakdekker Purmerend',
    'dakdekker Alkmaar',
    'dakdekker Hilversum',
    'dakdekker Weesp',
    'dakdekker Huizen',
    'dakdekker Bussum',
    'dakdekker Naarden',
    'dakdekker Laren',
    'dakdekker Muiden',
    'dakdekker Castricum',
    'dakdekker Heemstede',
    'dakdekker Bloemendaal',
    'dakdekker Zandvoort',
    'dakdekker Haarlemmermeer',
    'dakdekker Houten',
    'dakdekker Woerden',
    'dakdekker Nieuwkoop',
    'dakdekker Gouda',
    'dakdekker Katwijk',
    'dakdekker Leiden',
    'dakdekker Heemskerk',
    'dakdekker Uitgeest',
    'dakdekker Texel',
    'dakdekker Wijdemeren',
    'dakdekker Eemnes',
    'dakdekker Montfoort',
    'dakdekker Stichtse Vecht',
    'dakdekker De Ronde Venen',
    'dakdekker Krimpenerwaard',
    'dakdekker Amstelveen',
    'dakdekker Diemen',
    'dakdekker Beverwijk',
    'dakdekker Velsen',
    'dakdekker Wormerland',
    'dakdekker Waterland',
    'dakdekker Ouder-Amstel',
    'dakdekker Abcoude',
    'dakdekker Oostzaan',
    'dakdekker Oudewater',
    'dakdekker Kortenhoef',
    'dakdekker Maartensdijk',
    'dakdekker Bunnik',
    'dakdekker Renswoude',
    'dakdekker Lopikerwal',
    'dakdekker Bodegraven-Reeuwijk',
    'dakdekker Molenwaard',
    'dakdekker Vianen',
    'dakdekker Vijfheerenlanden',
    'dakdekker Teylingen',
    'dakdekker Noordwijkerhout',
    'dakdekker Rijnwoude',
]

candidates = {}
skip_domains = {
    'youtube.com', 'facebook.com', 'linkedin.com', 'instagram.com',
    'google.nl', 'google.com', 'bing.com', 'microsoft.com',
    'wordpress.org', 'wordpress.com', 'medium.com', 'github.com',
    'marktplaats.nl', 'werkspot.nl', 'trustpilot.com', 'klarna.com',
    'facebook.nl', 'twitter.com', 'pinterest.com', 'vk.com',
    'tumblr.com', 'blogspot.com', 'ebay.com', 'amazon.com',
}

for i, term in enumerate(search_terms):
    print(f'({i+1}/{len(search_terms)}) {term}...', flush=True)
    html = search_bing(term)
    if html:
        # Extract domains from result links
        pattern = r'href=["\x27](https?://[^"\x27/\s#?]+\.nl)[^"\x27]*["\x27]'
        found = re.findall(pattern, html)
        # Also try with single quotes
        pattern2 = r"href=['\"]([^'\"]+\.nl)[^'\"]*['\"]"
        found2 = re.findall(pattern2, html)
        found.extend(found2)
        
        new_found = 0
        for domain in found:
            domain = domain.lower()
            if domain in skip_domains:
                continue
            if domain not in existing and domain not in candidates:
                candidates[domain] = term
                new_found += 1
        if new_found > 0:
            print(f'  New: {new_found} (total: {len(candidates)})', flush=True)

print(f'\nTotal new candidates: {len(candidates)}')
for d in sorted(candidates.keys()):
    print(f'  {d} (from: {candidates[d]})')

with open('FINDINGS/new_candidates.txt', 'w') as f:
    for domain, term in sorted(candidates.items()):
        f.write(f'{domain}|{term}|bing\n')
print(f'Saved to FINDINGS/new_candidates.txt')
