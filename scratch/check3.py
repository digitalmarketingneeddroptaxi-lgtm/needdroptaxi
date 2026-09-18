import os
import re

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'
files_to_check = ['index.html', r'outstation-taxi-service\index.html']

for f in files_to_check:
    filepath = os.path.join(root, f)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            hrefs = re.findall(r'href="([^"]+)"', content)
            print(f"\n--- Links in {f} ---")
            for h in set(hrefs):
                print(h)
