from bs4 import BeautifulSoup

with open(r'outstation-taxi-service\index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

for a in soup.find_all('a'):
    text = a.get_text(strip=True).lower()
    if 'book' in text or 'calculator' in text:
        print(f"--- Button: {text} ---")
        print(a.prettify())
