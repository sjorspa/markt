#!/usr/bin/env python3
"""Analyze a candidate website for competitive research."""
import re, sys

html = open('/tmp/candidate_main.html').read()

# Title
title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
title = title_match.group(1).strip() if title_match else 'GEEN'

# Meta description
meta_match = re.search(r'<meta[^>]*name=["\x27]description["\x27][^>]*content=["\x27](.+?)["\x27]', html, re.IGNORECASE)
meta_desc = meta_match.group(1).strip() if meta_match else 'GEEN'

# H1 tags
h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
h1_text = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s if re.sub(r'<[^>]+>', '', h).strip()]

# H2 tags
h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
h2_count = len([h for h in h2s if re.sub(r'<[^>]+>', '', h).strip()])

# Schema.org
has_schema = 'schema.org' in html or 'ld+json' in html.lower()

# Mobile viewport
viewport = re.search(r'<meta[^>]*name=["\x27]viewport["\x27][^>]*content=["\x27](.+?)["\x27]', html, re.IGNORECASE)

# Phone numbers
phones = re.findall(r'0[0-9\s\-\+]{8,14}', html)
phones = set(p.strip() for p in phones if len(p.strip()) >= 10)

# Email
emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html))

# KvK
kkr_matches = set(re.findall(r'KvK[:\s]*([0-9]{8})', html, re.IGNORECASE))

# Address patterns
addr_matches = set(re.findall(r'[A-Z][a-z]+ [0-9]+[, ]*[A-Z]{2}\s?[0-9]{4}', html))

# CMS detection
cms = []
if 'wordpress' in html.lower(): cms.append('WordPress')
if 'elementor' in html.lower(): cms.append('Elementor')
if 'yoast' in html.lower(): cms.append('Yoast SEO')
if 'rank math' in html.lower(): cms.append('Rank Math SEO')
if 'wix' in html.lower(): cms.append('Wix')
if 'shopify' in html.lower(): cms.append('Shopify')

# sitemap.xml link
has_sitemap = 'sitemap.xml' in html

# robots.txt link
has_robots = 'robots.txt' in html

# GBP (Google Business Profile)
has_gbp = 'google.com/maps' in html or 'business.google.com' in html

print(f"Titel: {title}")
print(f"Meta beschrijving: {meta_desc[:80] if meta_desc != 'GEEN' else 'GEEN'}")
print(f"H1 tags ({len(h1_text)}): {h1_text[:3]}")
print(f"H2 count: {h2_count}")
print(f"schema.org JSON-LD: {'JA' if has_schema else 'GEEN'}")
print(f"sitemap.xml link: {'JA' if has_sitemap else 'GEEN'}")
print(f"robots.txt link: {'JA' if has_robots else 'GEEN'}")
print(f"Mobielvriendelijk: {'JA' if viewport else 'GEEN'}")
print(f"Google Business Profile: {'JA' if has_gbp else 'GEEN'}")
print(f"Telefoon: {phones}")
print(f"Email: {emails}")
print(f"KvK: {kkr_matches}")
print(f"Adres patronen: {addr_matches}")
print(f"CMS: {', '.join(cms) if cms else 'Niet gevonden'}")
