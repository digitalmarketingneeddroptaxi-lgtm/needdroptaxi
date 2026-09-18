from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("--- ANCHORS WITH BOOK OR CALCULATOR ---")
for a in soup.find_all('a'):
    text = a.get_text(strip=True).lower()
    if 'book' in text or 'calculator' in text:
        print(f"Text: {text} | Href: {a.get('href')}")

print("\n--- BUTTONS WITH BOOK OR CALCULATOR ---")
for b in soup.find_all('button'):
    text = b.get_text(strip=True).lower()
    if 'book' in text or 'calculator' in text:
        print(f"Text: {text} | Attributes: {b.attrs}")
