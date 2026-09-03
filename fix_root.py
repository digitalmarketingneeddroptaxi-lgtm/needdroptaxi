import os
import re

ROOT = r"c:\Users\Pathi\Documents\needdroptaxi.com"

# Fix root index.html - it uses relative paths without ../
filepath = os.path.join(ROOT, "index.html")
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

original = content

# Fix href="about/index.html" -> href="/about/" (root-level relative without ../)
content = re.sub(r'href="([a-z][a-z0-9-]+)/index\.html"', r'href="/\1/"', content)

# Fix href="outstation-taxi-service/index.html" -> "/outstation-taxi-service/"
# Already handled above

# Fix src="_astro/..." -> src="/_astro/..."
content = re.sub(r'(src=")_astro/', r'\g<1>/_astro/', content)
content = re.sub(r'(src=")images/', r'\g<1>/images/', content)

# Fix href="_astro/..." -> href="/_astro/..."
content = re.sub(r'(href=")_astro/', r'\g<1>/_astro/', content)
content = re.sub(r'(href=")assets/', r'\g<1>/assets/', content)

# Fix href="favicon.svg" -> "/favicon.svg"
content = re.sub(r'(href=")favicon', r'\g<1>/favicon', content)
content = re.sub(r'(href=")apple-touch-icon', r'\g<1>/apple-touch-icon', content)
content = re.sub(r'(href=")site\.webmanifest', r'\g<1>/site.webmanifest', content)
content = re.sub(r'(href=")safari-pinned-tab', r'\g<1>/safari-pinned-tab', content)

# Fix deeper paths: drop-taxi/X/index.html -> /drop-taxi/X/
content = re.sub(r'href="([a-z][a-z0-9-]+/[a-z][a-z0-9-]+)/index\.html"', r'href="/\1/"', content)

# Fix blog paths
content = re.sub(r'href="(blog/[a-z][a-z0-9-]+/[a-z][a-z0-9-]+)/index\.html"', r'href="/\1/"', content)

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("FIXED: Root index.html")
else:
    print("OK: Root index.html already clean")
