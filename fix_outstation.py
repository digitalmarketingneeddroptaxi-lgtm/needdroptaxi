import os
import re
import glob

def fix_pages():
    files = glob.glob(r"c:\Users\Pathi\Documents\needdroptaxi.com\**\*.html", recursive=True)
    count_logo = 0
    count_rupee = 0
    
    for file in files:
        if ".git" in file: continue
        
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original = content
        
        # 1. Fix the logo classes
        # Remove invert, hue-rotate-180, contrast-125 (and their 'a' suffixed hacks)
        content = re.sub(r'\binvert[a]?\b', '', content)
        content = re.sub(r'\bhue-rotate-180[a]?\b', '', content)
        content = re.sub(r'\bcontrast-125[a]?\b', '', content)
        # Clean up multiple spaces in class
        content = re.sub(r'class=" +', 'class="', content)
        content = re.sub(r' +w-\[130px\]', ' w-[130px]', content)
        
        # 2. Fix the Rupee symbol replacing '?' before numbers
        # We want to replace ? followed by digits and commas, but ONLY if it's preceded by space, >, or some text,
        # to avoid replacing URL parameters like index.html?123 (though rare).
        # Typically the prices are like ">?2,410" or "at ?2,410" or "? 2,410"
        
        # Let's find all ? followed by number
        # Example: starting at ?2,410 -> starting at &#8377;2,410
        # Example: >?14/km -> >&#8377;14/km
        content = re.sub(r'(>|\s)\?([0-9][0-9,]*)\b', r'\1&#8377;\2', content)
        
        # What about "?150" or "? 150"? 
        content = re.sub(r'(>|\s)\?\s*([0-9][0-9,]*)\b', r'\1&#8377;\2', content)
        
        if content != original:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            count_logo += 1

    print(f"Fixed {count_logo} files.")

if __name__ == "__main__":
    fix_pages()
