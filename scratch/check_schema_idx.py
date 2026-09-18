from bs4 import BeautifulSoup
import json

root = r'c:\Users\Pathi\Documents\needdroptaxi.com'

with open(root + r'\index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for script in soup.find_all('script', type='application/ld+json'):
    try:
        data = json.loads(script.string)
        if data.get('@type') == 'LocalBusiness':
            print("LocalBusiness Pricing:", data.get('hasOfferCatalog', {}).get('itemListElement', []))
    except Exception as e:
        print("Error parsing JSON:", e)
