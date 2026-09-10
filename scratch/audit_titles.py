import os, re

html_files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

for p in sorted(html_files):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    m = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE | re.DOTALL)
    t = m.group(1).strip() if m else "NO TITLE"
    print(f"{p:<55} | Len: {len(t):<3} | {t}")
