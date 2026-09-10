import os, re

files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            files.append(os.path.join(root, f).replace('\\', '/'))

gtm_bad = []
for p in files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'gtm5445.html' in c:
        gtm_bad.append(p)

print(f"Files with gtm5445.html: {len(gtm_bad)}")
