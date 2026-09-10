import os, re

files = []
for root, dirs, files_list in os.walk('.'):
    if '.git' in root or 'scratch' in root: continue
    for f in files_list:
        if f.endswith('.html'):
            files.append(os.path.join(root, f).replace('\\', '/'))

all_script_srcs = set()
for p in files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    srcs = re.findall(r'<script\b[^>]*\bsrc=[\'"]([^\'"]*)[\'"]', c, re.IGNORECASE)
    for s in srcs:
        all_script_srcs.add(s)

print(f"Total unique script src attributes: {len(all_script_srcs)}")
for s in sorted(all_script_srcs):
    print("  ", s)
