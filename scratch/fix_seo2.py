import os
from bs4 import BeautifulSoup

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

# 1. Homepage SEO Fixes
idx_path = os.path.join(root, 'index.html')
with open(idx_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')
    
if soup.title:
    soup.title.string = "Taxi Service in Chennai | Outstation, Airport & Local Cabs"
meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc:
    meta_desc['content'] = "Book reliable and affordable taxi services in Chennai. Specializing in outstation rides, airport transfers, and local rentals. Enjoy comfortable travel today."
    
# Missing image ALT
img = soup.find('img', src=lambda s: s and 'Df4vqIEQ.webp' in s)
if img and not img.get('alt'):
    img['alt'] = "Need Drop Taxi - Comfortable Outstation Travel"

# Also update OG title and twitter title
og_title = soup.find('meta', attrs={'property': 'og:title'})
if og_title: og_title['content'] = soup.title.string
og_desc = soup.find('meta', attrs={'property': 'og:description'})
if og_desc: og_desc['content'] = meta_desc['content']

with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

# 2. Outstation SEO Fixes
out_path = os.path.join(root, r'outstation-taxi-service\index.html')
with open(out_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

if soup.title:
    soup.title.string = "Outstation Taxi Service from Chennai | Need Drop Taxi"
meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc:
    meta_desc['content'] = "Reliable outstation taxi service from Chennai. Transparent pricing starting at Rs.14/km. Book one-way or round-trip cabs with professional drivers."

og_title = soup.find('meta', attrs={'property': 'og:title'})
if og_title: og_title['content'] = soup.title.string
og_desc = soup.find('meta', attrs={'property': 'og:description'})
if og_desc: og_desc['content'] = meta_desc['content']

# Find and fix the 2 broken links: 
# Wait, I didn't identify them perfectly. Let me just replace any broken blog links.
# They were in the blog directory, not Outstation page? But SEOQuake said Outstation page has 2 broken links.
# Let me look for '/drop-taxi/' links or '#' links. 
# Oh! The broken links might be anchors to non-existent IDs. "Missing: /outstation-taxi-service/#tariffs"
# Is there a section with id="tariffs" in Outstation?
if not soup.find(id='tariffs'):
    # let's change #tariffs links to something else, or add id="tariffs" to the tariffs section!
    # Let's add id="tariffs" to the "Outstation Rides Tariff" heading.
    tariff_h2 = soup.find(lambda tag: tag.name in ['h2', 'h3'] and 'Tariff' in tag.get_text())
    if tariff_h2 and not tariff_h2.get('id'):
        tariff_h2['id'] = 'tariffs'

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
    
# Do the same for homepage missing anchors
with open(idx_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')
    
# If homepage has a link to /#tariffs, it's broken. The link is probably /outstation-taxi-service/#tariffs
# I added it to Outstation. What about /local-rental-taxi-service/#tariffs and /airport-transfer-taxi-service/#tariffs?
for p in ['local-rental-taxi-service', 'airport-transfer-taxi-service']:
    pp = os.path.join(root, p, 'index.html')
    if os.path.exists(pp):
        with open(pp, 'r', encoding='utf-8') as f:
            psoup = BeautifulSoup(f, 'html.parser')
        th = psoup.find(lambda tag: tag.name in ['h2', 'h3'] and 'Tariff' in tag.get_text())
        if th and not th.get('id'):
            th['id'] = 'tariffs'
            with open(pp, 'w', encoding='utf-8') as f:
                f.write(str(psoup))

