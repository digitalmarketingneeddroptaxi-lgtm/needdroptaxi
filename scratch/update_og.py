import os
import re
from bs4 import BeautifulSoup
import json

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'
new_og_image = 'https://needdroptaxi.com/images/need-drop-taxi-og.jpg'

for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            changed = False
            
            # Update meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name', '').lower()
                prop = meta.get('property', '').lower()
                if name == 'twitter:image' or prop == 'og:image' or name == 'og:image':
                    if meta.get('content') != new_og_image:
                        meta['content'] = new_og_image
                        changed = True

            # Also update Schema JSON-LD if it references an old image
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    script_changed = False
                    
                    if isinstance(data, dict):
                        if data.get('image') and isinstance(data.get('image'), str) and data['image'].endswith('.jpg') and 'og' in data['image']:
                            data['image'] = new_og_image
                            script_changed = True
                            
                    if script_changed:
                        script.string = json.dumps(data, separators=(',', ':'))
                        changed = True
                except:
                    pass

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
