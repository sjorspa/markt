import re
from urllib.parse import unquote

with open('/tmp/whatsapp_search.html', 'r', errors='ignore') as f:
    content = f.read()

# Find all Yahoo search result links
links = re.findall(r'href="(https?://r\.search\.yahoo\.com/rd\.lk[^"]+)"', content)
print(f'Found {len(links)} Yahoo redirect links')

# Try to extract the actual destination URLs
seen_urls = set()
for link in links:
    decoded = unquote(link)
    # Find the actual URL in the redirect chain
    url_match = re.search(r'RU=(https?://[^&]+)', decoded)
    if url_match:
        actual_url = unquote(url_match.group(1))
        # Skip Yahoo's own domains
        if any(domain in actual_url for domain in ['yahoo.com', 'bing.com', 'microsoft.com']):
            continue
        seen_urls.add(actual_url)

print(f'\nUnique non-ad URLs found:')
for url in sorted(seen_urls):
    print(f'  {url}')
