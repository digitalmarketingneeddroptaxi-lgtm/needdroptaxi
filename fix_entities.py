import os

files = [
    r"c:\Users\Pathi\Documents\needdroptaxi.com\terms-and-conditions\index.html",
    r"c:\Users\Pathi\Documents\needdroptaxi.com\privacy-policy\index.html"
]

for file in files:
    with open(file, 'rb') as f:
        content = f.read()

    # Replace UTF-8 characters with HTML entities safely
    
    # Quotes and punctuation
    content = content.replace(b'\xe2\x80\x98', b'&lsquo;') # left single quote
    content = content.replace(b'\xe2\x80\x99', b'&rsquo;') # right single quote (apostrophe)
    content = content.replace(b'\xe2\x80\x9c', b'&ldquo;') # left double quote
    content = content.replace(b'\xe2\x80\x9d', b'&rdquo;') # right double quote
    content = content.replace(b'\xe2\x80\x93', b'&ndash;') # en dash
    content = content.replace(b'\xe2\x80\x94', b'&mdash;') # em dash
    
    # Symbols
    content = content.replace(b'\xe2\x82\xb9', b'&#8377;') # Indian Rupee
    content = content.replace(b'\xc2\xa9', b'&copy;')      # Copyright
    content = content.replace(b'\xf0\x9f\x9a\x97', b'&#128663;') # Car emoji
    
    # Also replace any Replacement Character \ufffd just in case
    content = content.replace(b'\xef\xbf\xbd', b'')

    with open(file, 'wb') as f:
        f.write(content)
        
    print(f"Fixed {file}")
