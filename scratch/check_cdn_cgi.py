import os, re

files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            files.append(os.path.join(root, f).replace('\\', '/'))

cdn_cgi_refs = []
for p in files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    matches = re.findall(r'src=[\'"]([^\'"]*cdn-cgi[^\'"]*)[\'"]', c)
    for m in matches:
        cdn_cgi_refs.append((p, m))

print(f"Total cdn-cgi script refs: {len(cdn_cgi_refs)}")
for p, m in set(cdn_cgi_refs):
    print(p, m)
