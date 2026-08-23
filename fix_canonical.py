import os
import re

def fix_canonical_urls(directory):
    base_url = "https://needdroptaxi.com"
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                # Determine the relative path
                rel_path = os.path.relpath(filepath, directory)
                
                # Convert Windows path to web path
                web_path = rel_path.replace('\\', '/')
                
                # Build canonical URL
                if web_path == 'index.html':
                    canonical = f"{base_url}/"
                elif web_path.endswith('/index.html'):
                    canonical = f"{base_url}/{web_path[:-11]}/"
                elif web_path.endswith('index.html'):
                    canonical = f"{base_url}/{web_path[:-10]}"
                else:
                    canonical = f"{base_url}/{web_path}"
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace <link rel="canonical" href="...">
                new_content = re.sub(
                    r'<link rel="canonical" href="[^"]*">',
                    f'<link rel="canonical" href="{canonical}">',
                    content
                )
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed canonical for {web_path}")

if __name__ == "__main__":
    fix_canonical_urls('c:\\Users\\Pathi\\Documents\\needdroptaxi.com')
