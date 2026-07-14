import re

with open('/tmp/gids.html', 'r', errors='ignore') as f:
    content = f.read()

# Find all company listing blocks
# Look for pt-company-listing blocks
companies = []
# Find all company links
links = re.findall(r'href="(https?://[^\"]+)"[^>]*class=\"[^\"]*pt-company-listing__link[^\"]*"[^>]*>([^<]+)', content)
print(f"Found {len(links)} company links")
for link, name in links:
    print(f"  {name.strip()}: {link}")

# Also look for company names in a different pattern
names = re.findall(r'class=\"pt-company-listing__link[^\"]*\"[^>]*href=\"([^\"]+)\"[^>]*>\s*([^<]+)', content)
print(f"\nFound {len(names)} named companies")
for link, name in names:
    print(f"  {name.strip()}: {link}")

# Try another pattern - look for the listing blocks
blocks = re.findall(r'class=\"pt-company-listing rounded"[^>]*>(.*?)class=\"pt-company-listing__actions', content, re.DOTALL)
print(f"\nFound {len(blocks)} company blocks")
for block in blocks[:5]:
    # Extract name
    name_m = re.search(r'class=\"pt-company-listing__link[^\"]*\"[^>]*>\s*([^<]+)', block)
    link_m = re.search(r'href=\"([^\"]+)\"', block)
    if name_m and link_m:
        print(f"  {name_m.group(1).strip()}: {link_m.group(1)}")
