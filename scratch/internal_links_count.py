import os
import glob
import re
from urllib.parse import urlparse
from collections import defaultdict

html_files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

# Map file to canonical URL
canonical_map = {}
for p in html_files:
    # compute URL from path:
    # ./index.html -> /
    # ./about/index.html -> /about/
    # ./drop-taxi/chennai-to-bangalore/index.html -> /drop-taxi/chennai-to-bangalore/
    clean_p = p.lstrip('./')
    if clean_p == 'index.html':
        url = '/'
    elif clean_p.endswith('/index.html'):
        url = '/' + clean_p[:-10]
    elif clean_p.endswith('.html'):
        url = '/' + clean_p
    else:
        url = '/' + clean_p
    canonical_map[p] = url

url_to_file = {v: k for k, v in canonical_map.items()}

# Count incoming links
incoming_links = defaultdict(set) # target_url -> set of source_files

for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    hrefs = re.findall(r'<a\b[^>]*\bhref=[\'"]([^\'"]*)[\'"][^>]*>', c, re.IGNORECASE)
    for h in hrefs:
        # ignore non-internal
        if h.startswith('tel:') or h.startswith('mailto:') or h.startswith('javascript:') or h.startswith('#'):
            continue
        # normalize
        if h.startswith('http://') or h.startswith('https://'):
            if 'needdroptaxi.com' in h:
                h = urlparse(h).path
            else:
                continue
        # clean query / fragment
        clean_h = h.split('?')[0].split('#')[0]
        if clean_h.startswith('/../'):
            clean_h = clean_h[3:]
        elif clean_h.startswith('../'):
            continue
        if not clean_h.endswith('/') and not '.' in clean_h.split('/')[-1] and clean_h != '':
            clean_h += '/'
        incoming_links[clean_h].add(p)

print("=== INCOMING INTERNAL LINK COUNTS FOR ALL PAGES ===")
for url in sorted(canonical_map.values()):
    sources = incoming_links.get(url, set())
    print(f"{url:<55} : {len(sources)} incoming pages")
    if len(sources) <= 3:
        for s in sources:
            print(f"    <- {s}")
