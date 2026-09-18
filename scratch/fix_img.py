import os
from PIL import Image
from bs4 import BeautifulSoup

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'
img_path = os.path.join(root, 'images', 'trip_fare_estimator_mockup.png')
out_path = os.path.join(root, 'images', 'trip_fare_estimator_mockup.webp')

if os.path.exists(img_path):
    with Image.open(img_path) as img:
        img.save(out_path, 'WEBP', quality=80)
    print("Saved WebP")
    
    # Update references in all html
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'trip_fare_estimator_mockup.png' in content:
                    content = content.replace('trip_fare_estimator_mockup.png', 'trip_fare_estimator_mockup.webp')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
