import os
import re

def find_relative_links(directory):
    pattern = re.compile(r'href=[\'\"]([^\'\"/h#m][^\'\"]*)[\'\"]')
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_astro' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for match in matches:
                        if not match.startswith('data:') and not match.startswith('javascript:') and not match.startswith('tel:'):
                            print(f'File: {filepath}, Relative link: {match}')

find_relative_links('c:/Users/Pathi/Documents/needdroptaxi.com')
