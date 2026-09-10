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
    m_desc = re.search(r'<meta\s+name=[\'"]description[\'"]\s+content=[\'"](.*?)[\'"]', c, re.IGNORECASE | re.DOTALL)
    if not m_desc:
        m_desc = re.search(r'<meta\s+content=[\'"](.*?)[\'"]\s+name=[\'"]description[\'"]', c, re.IGNORECASE | re.DOTALL)
    desc = m_desc.group(1).strip() if m_desc else "NO DESC"
    print(f"\n{p} (Len: {len(desc)}):")
    print(f"  {desc}")
