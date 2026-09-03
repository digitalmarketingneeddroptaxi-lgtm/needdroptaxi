import os
import re

def fix_links_in_html(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_astro' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Replace HTTrack strange index files in links
                content = re.sub(r'href=[\'\"](?:(?:\.\./)*)?index[a-z0-9]*\.html\?[^\'\"]*[\'\"]', 'href="/taxi-booking/"', content)
                
                # Replace relative paths to index.html
                # e.g. href="../about/index.html" -> href="/about/"
                content = re.sub(r'href=[\'\"](?:\.\./)+([^/]+)/index\.html[\'\"]', r'href="/\1/"', content)
                
                # e.g. href="../index.html" -> href="/"
                content = re.sub(r'href=[\'\"](?:\.\./)+index\.html[\'\"]', 'href="/"', content)
                
                # e.g. href="index.html" -> href="/"
                content = re.sub(r'href=[\'\"]index\.html[\'\"]', 'href="/"', content)
                
                # Ensure self-referencing canonicals are absolute
                # (Assuming they might be already absolute, but checking if they are not)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {filepath}")

fix_links_in_html(r'c:\Users\Pathi\Documents\needdroptaxi.com')
