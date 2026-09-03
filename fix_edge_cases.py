import os
import re

ROOT = r"c:\Users\Pathi\Documents\needdroptaxi.com"

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Fix paths with query params: e.g. ../trip-fare-calculator/index.html?ref=... -> /trip-fare-calculator/?ref=...
    content = re.sub(
        r'href="(?:\.\./)*trip-fare-calculator/index\.html\?([^"]*)"',
        r'href="/trip-fare-calculator/?\1"',
        content
    )
    content = re.sub(
        r'href="trip-fare-calculator/index\.html\?([^"]*)"',
        r'href="/trip-fare-calculator/?\1"',
        content
    )
    
    # Fix paths with hash fragments: e.g. ../outstation-taxi-service/index.html#tariffs -> /outstation-taxi-service/#tariffs
    content = re.sub(
        r'href="(?:\.\./)*([a-z][a-z0-9-]+)/index\.html#([^"]*)"',
        r'href="/\1/#\2"',
        content
    )
    content = re.sub(
        r'href="([a-z][a-z0-9-]+)/index\.html#([^"]*)"',
        r'href="/\1/#\2"',
        content
    )

    # Fix blog links in blog/index.html
    # href="top-10-tourist-attractions.../index.html" -> "/blog/top-10-tourist-attractions.../"
    content = re.sub(
        r'href="([a-z][a-z0-9-]+)/index\.html"',
        r'href="/blog/\1/"',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {filepath}")

for root, dirs, files in os.walk(ROOT):
    if '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            fix_html_file(os.path.join(root, file))

print("Edge cases fixed.")
