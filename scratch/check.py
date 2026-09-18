import os
import re
from urllib.parse import urlparse

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

# Find malformed urls
for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'needdroptaxi.com/needdroptaxi.com' in content:
                print(f"Malformed url in {filepath}")
            if '../trip-fare-calculator' in content:
                print(f"Malformed relative url in {filepath}")
