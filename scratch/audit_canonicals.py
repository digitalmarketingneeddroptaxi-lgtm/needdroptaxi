import os, re

files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            files.append(os.path.join(root, f).replace('\\', '/'))

canonicals = []
for p in sorted(files):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    m = re.findall(r'<link\s+[^>]*rel=[\'"]canonical[\'"][^>]*>', c, re.IGNORECASE)
    if not m:
        canonicals.append((p, 'MISSING', len(m)))
    else:
        for tag in m:
            m_href = re.search(r'href=[\'"]([^\'"]*)[\'"]', tag)
            href = m_href.group(1) if m_href else 'NO_HREF'
            canonicals.append((p, href, len(m)))

print(f"Total files checked: {len(files)}")
for p, href, count in canonicals:
    print(f"{p:<55} (count: {count}) -> {href}")
