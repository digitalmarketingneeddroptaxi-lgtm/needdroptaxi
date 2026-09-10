import os
import re

links = set()
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            for m in re.findall(r'href=[\'"](/drop-taxi/?)[\'"]', c):
                links.add((p, m))
print(f"Links to /drop-taxi/ alone: {len(links)}")
for item in links:
    print(item)
