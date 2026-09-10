import os
import glob
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

external_domains = [
    'jsdelivr', 'jquery', 'googletagmanager', 'google-analytics',
    'clarity.ms', 'cloudflareinsights', 'facebook', 'instagram', 'linkedin', 'twitter'
]

results = []
for p in sorted(html_files):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    # Find any src or href or j.src or url() that references external domains relatively
    # e.g. ../ or /cdn. or ./ or starting without https:// or http:// or //
    for dom in external_domains:
        # check for quotes surrounding dom
        matches = re.findall(r'([\'"][^\'"]*' + dom + r'[^\'"]*[\'"])', content)
        for m in matches:
            val = m.strip('\'"')
            if not val.startswith('https://') and not val.startswith('http://') and not val.startswith('//') and not val.startswith('mailto:') and not val.startswith('tel:'):
                results.append((p, val))

print(f"Total malformed/relative external URLs: {len(results)}")
for p, val in results:
    print(f"  {p} -> {val}")
