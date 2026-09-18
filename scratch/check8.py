from bs4 import BeautifulSoup
import json

with open(r'outstation-taxi-service\index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')
    
    print("--- VISIBLE TEXT ---")
    for row in soup.find_all('tr'):
        print(row.get_text(separator=' | ', strip=True))

    print("\n--- SCHEMA ---")
    for s in soup.find_all('script', type='application/ld+json'):
        print(s.string)
