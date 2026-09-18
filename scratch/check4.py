import os
import re

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

with open(os.path.join(root, 'index.html'), 'r', encoding='utf-8') as file:
    content = file.read()
    hrefs = re.findall(r'href="([^"]+)"', content)
    for h in set(hrefs):
        if h.startswith('/') and not h.startswith('/_astro'):
            # check if file exists
            if h.endswith('/'):
                p = os.path.join(root, h.strip('/') + '/index.html')
            else:
                p = os.path.join(root, h.strip('/'))
            if not os.path.exists(p) and not os.path.exists(os.path.join(root, h.strip('/') + '.html')):
                print(f"Missing: {h}")
