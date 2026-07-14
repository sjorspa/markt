#!/usr/bin/env python3
"""Analyze dakdekkersamstelveen.nl website."""
import re
import json

with open('FINDINGS/dakdekkersamstelveen_main.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Title
title_m = re.search(r'<title>([^<]+)</title>', html)
title = title_m.group(1) if title_m else 'GEEN'

# Meta description
meta_m = re.search(r'<meta[^>]*content=["\x27]([^"\x27]*)["\x27][^>]*name=["\x27]description["\x27]', html, re.IGNORECASE)
if not meta_m:
    meta_m = re.search(r'<meta[^>]*name=["\x27]description["\x27][^>]*content=["\x27]([^"\x27]*)["\x27]', html, re.IGNORECASE)
meta_desc = meta_m.group(1) if meta_m else 'GEEN'

# H1/H2 tags
h1s = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
h2s = re.findall(r'<h2[^>]*>([^<]+)</h2>', html, re.IGNORECASE)

# Schema.org JSON-LD
schema_blocks = re.findall(r'<script[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>', html, re.DOTALL)

# robots.txt / sitemap
has_robots = bool(re.search(r'robots\.txt', html, re.IGNORECASE))
has_sitemap = bool(re.search(r'sitemap', html, re.IGNORECASE))

# Canonical
canonical_m = re.search(r'<link[^>]*rel=["\x27]canonical["\x27][^>]*href=["\x27]([^"\x27]*)["\x27]', html, re.IGNORECASE)

# Mobile
viewport_m = re.search(r'<meta[^>]*name=["\x27]viewport["\x27][^>]*content=["\x27]([^"\x27]*)["\x27]', html, re.IGNORECASE)

# Google Business
has_gbp = bool(re.search(r'business\.google\.com', html, re.IGNORECASE))

# Contact info
emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
phones = re.findall(r'0[0-9]{8,10}|0[0-9]{2}[- ]?[0-9]{6,8}', html)
kvks = re.findall(r'KvK[:\s]*[0-9]{8}', html, re.IGNORECASE)
if not kvks:
    kvks = re.findall(r'[0-9]{8}', html)

# Addresses
addresses = re.findall(r'[A-Z][A-Za-z\s,]+(?:straat|weg|dwarstraat|laan|plein|hof|steeg|gracht)[\s,]*[0-9]+', html)

# Social
fb_m = re.search(r'facebook\.com/([^"\x27\s]+)', html, re.IGNORECASE)
ig_m = re.search(r'instagram\.com/([^"\x27\s]+)', html, re.IGNORECASE)
yt_m = re.search(r'youtube\.com/([^"\x27\s]+)', html, re.IGNORECASE)

# CMS detection
is_wordpress = 'wp-content' in html
is_elementor = 'elementor' in html.lower()
is_yoast = 'yoast' in html.lower()

# Services in body text
body_m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
body_text = body_m.group(1) if body_m else ''

services = []
service_keywords = [
    'dakbedekking', 'dakrenovatie', 'dakreparatie', 'dakgoot', 'gootverversing',
    'zinkwerk', 'loodwerk', 'koper', 'plat dak', 'hellend dak', 'EPDM', 'PVC',
    'TPO', 'shingles', 'leien', 'dakisolatie', 'dakonderhoud', 'dakkapel',
    'schoorsteen', 'vogelwering', 'gevelbekleding', 'montage', 'nieuwbouw',
    'herstel', 'reparatie', 'renovatie', 'onderhoud'
]
for kw in service_keywords:
    if kw.lower() in body_text.lower():
        services.append(kw)

print(f'TITLE: {title}')
print(f'META DESC: {meta_desc}')
print(f'H1 count: {len(h1s)}')
for i, h1 in enumerate(h1s):
    print(f'  H1[{i}]: {h1.strip()}')
print(f'H2 count: {len(h2s)}')
for i, h2 in enumerate(h2s[:10]):
    print(f'  H2[{i}]: {h2.strip()[:80]}')
print(f'Schema.org: {len(schema_blocks)} blocks')
for i, s in enumerate(schema_blocks):
    try:
        data = json.loads(s.strip())
        addr = "N/A"
        if isinstance(data.get("address"), dict):
            addr = data["address"].get("streetAddress", "N/A")
        print(f'  Block {i}: type={data.get("@type", "unknown")}, name={data.get("name", "N/A")}, address={addr}')
    except:
        print(f'  Block {i}: (parse error) {s.strip()[:100]}')
print(f'robots.txt: {"JA" if has_robots else "GEEN"}')
print(f'sitemap.xml: {"JA" if has_sitemap else "GEEN"}')
print(f'canonical: {canonical_m.group(1) if canonical_m else "GEEN"}')
print(f'mobielvriendelijk: {"JA" if viewport_m else "GEEN"}')
print(f'Google Business Profile: {"JA" if has_gbp else "GEEN"}')
print(f'emails: {emails}')
print(f'phones: {[p for p in phones if len(p) >= 8][:5]}')
print(f'KvK: {kvks[:3]}')
print(f'addresses: {[a.strip() for a in addresses[:5]]}')
print(f'Facebook: {fb_m.group(1) if fb_m else "GEEN"}')
print(f'Instagram: {ig_m.group(1) if ig_m else "GEEN"}')
print(f'YouTube: {yt_m.group(1) if yt_m else "GEEN"}')
print(f'WordPress: {is_wordpress}, Elementor: {is_elementor}, Yoast: {is_yoast}')
print(f'Diensten: {", ".join(services[:15])}')
