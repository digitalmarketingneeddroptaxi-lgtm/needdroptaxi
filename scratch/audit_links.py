import os
import re
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

internal_broken = []
external_broken = []
all_internal_links = set()
all_external_links = set()

print("Scanning for links...")

for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            rel_filepath = os.path.relpath(filepath, root)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a'):
                href = a.get('href')
                if not href: continue
                
                # Exclude anchors pointing to the same page, mailto, tel, javascript
                if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:'):
                    continue
                
                if href.startswith('http://') or href.startswith('https://'):
                    # External or absolute internal
                    if 'needdroptaxi.com' in href:
                        # Treat as internal for existence checking if it's pointing to the site
                        path = urlparse(href).path
                        all_internal_links.add((rel_filepath, path, href))
                    else:
                        all_external_links.add((rel_filepath, href))
                else:
                    # Internal relative
                    all_internal_links.add((rel_filepath, href, href))

print(f"Found {len(all_internal_links)} internal and {len(all_external_links)} external unique links.")

# Check Internal Links
print("Checking internal links...")
for source, target_path, original_href in all_internal_links:
    # Remove query params and fragments
    clean_path = target_path.split('?')[0].split('#')[0]
    
    if clean_path == '/':
        clean_path = '/index.html'
    
    # Handle absolute paths vs relative paths
    if clean_path.startswith('/'):
        # Absolute to root
        target_file = os.path.join(root, clean_path.lstrip('/'))
    else:
        # Relative to current file
        target_file = os.path.join(os.path.dirname(os.path.join(root, source)), clean_path)
        
    # Standardize paths
    target_file = os.path.normpath(target_file)
    
    # If the target is a directory, append index.html
    if not target_file.endswith('.html') and not target_file.endswith('.css') and not target_file.endswith('.js') and not target_file.endswith('.png') and not target_file.endswith('.jpg') and not target_file.endswith('.webp') and not target_file.endswith('.svg') and not target_file.endswith('.xml') and not target_file.endswith('.txt'):
        if os.path.isdir(target_file):
            target_file = os.path.join(target_file, 'index.html')
        else:
            # Maybe it maps to a file with .html?
            if not os.path.exists(target_file) and os.path.exists(target_file + '.html'):
                target_file = target_file + '.html'
            else:
                target_file = os.path.join(target_file, 'index.html') # default Astro assumption

    if not os.path.exists(target_file):
        internal_broken.append((source, original_href))

print("Checking external links...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
# Only check a subset or do it quickly to avoid timeouts
checked_urls = {}
for source, url in all_external_links:
    if url in checked_urls:
        if not checked_urls[url]:
            external_broken.append((source, url))
        continue
        
    try:
        req = urllib.request.Request(url, headers=headers)
        urllib.request.urlopen(req, timeout=5)
        checked_urls[url] = True
    except urllib.error.HTTPError as e:
        if e.code in [403, 401]: # Sometimes blocks bots, assume okay for now unless it's a 404
             checked_urls[url] = True
        else:
             checked_urls[url] = False
             external_broken.append((source, url))
    except Exception as e:
        checked_urls[url] = False
        external_broken.append((source, url))

# Save results
with open(os.path.join(root, 'scratch', 'broken_links.json'), 'w') as f:
    json.dump({'internal': internal_broken, 'external': external_broken}, f, indent=2)

print(f"Audit complete. {len(internal_broken)} broken internal, {len(external_broken)} broken external.")
