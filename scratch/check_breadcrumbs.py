import os
import re

with open('drop-taxi/chennai-to-bangalore/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# find breadcrumb HTML
m = re.findall(r'<nav[^>]*aria-label=[\'"]Breadcrumb[\'"][^>]*>.*?</nav>', content, re.DOTALL | re.IGNORECASE)
if not m:
    m = re.findall(r'<ol[^>]*>.*?</ol>', content, re.DOTALL)
print("Breadcrumbs found:")
for b in m:
    print(b)
