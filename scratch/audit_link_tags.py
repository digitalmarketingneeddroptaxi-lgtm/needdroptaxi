import os, re

files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            files.append(os.path.join(root, f).replace('\\', '/'))

link_hrefs = set()
for p in files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    links = re.findall(r'<link\b[^>]*\bhref=[\'"]([^\'"]*)[\'"]', c, re.IGNORECASE)
    for l in links:
        if 'cdn.' in l or 'jquery' in l or '..' in l:
            link_hrefs.add((p, l))

print(f"Suspicious link hrefs: {len(link_hrefs)}")
for p, l in link_hrefs:
    print(p, l)
