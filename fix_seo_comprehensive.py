import os
import re

BASE = "https://needdroptaxi.com"
ROOT = r"c:\Users\Pathi\Documents\needdroptaxi.com"

# Map from file path to canonical URL path
def get_canonical_path(filepath):
    """Derive the canonical URL path from the file's location."""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    # e.g. "about/index.html" -> "/about/"
    # e.g. "index.html" -> "/"
    # e.g. "drop-taxi/chennai-to-bangalore/index.html" -> "/drop-taxi/chennai-to-bangalore/"
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("/index.html")] + "/"
    # for non-index files like pathi.html
    return "/" + rel

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    canonical_path = get_canonical_path(filepath)
    canonical_url = BASE + canonical_path
    
    # ===== 1. Fix og:url and twitter:url to use absolute canonical URLs =====
    # og:url with relative "index.html" or "../../index.html" etc
    content = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        r'\g<1>' + canonical_url + r'\2',
        content
    )
    content = re.sub(
        r'(<meta\s+name="twitter:url"\s+content=")[^"]*(")',
        r'\g<1>' + canonical_url + r'\2',
        content
    )
    
    # ===== 2. Fix og:image and twitter:image with "[object Object]" =====
    content = content.replace(
        'content="[object Object]"',
        'content="' + BASE + '/images/book-a-taxi-og.jpg"'
    )
    
    # ===== 3. Fix og:image and twitter:image relative paths =====
    # Convert relative ../images/... or ../../images/... or images/... to absolute
    content = re.sub(
        r'(content=")\.\./images/',
        r'\g<1>' + BASE + '/images/',
        content
    )
    content = re.sub(
        r'(content=")\.\.\/\.\.\/images/',
        r'\g<1>' + BASE + '/images/',
        content
    )
    content = re.sub(
        r'(content=")images/',
        r'\g<1>' + BASE + '/images/',
        content
    )
    
    # ===== 4. Fix cdn-cgi/l/email-protection.html links =====
    # These are HTTrack artifacts. Replace with a mailto link or just remove.
    # The email is contact@needdroptaxi.com based on schema data
    content = re.sub(
        r'href="(?:\.\./)*cdn-cgi/l/email-protection\.html[^"]*"',
        'href="mailto:contact@needdroptaxi.com"',
        content
    )
    
    # ===== 5. Fix remaining relative nav/booking links with query strings =====
    # ../taxi-booking/index.html?ref=... -> /taxi-booking/?ref=...
    content = re.sub(
        r'href="(?:\.\./)*taxi-booking/index\.html\?([^"]*)"',
        r'href="/taxi-booking/?\1"',
        content
    )
    
    # ===== 6. Fix remaining deep relative links (../X/Y/index.html) =====
    # Pattern: ../../drop-taxi/chennai-to-bangalore/index.html -> /drop-taxi/chennai-to-bangalore/
    content = re.sub(
        r'href="(?:\.\./)+([a-z][a-z0-9-]+/[a-z][a-z0-9-]+)/index\.html"',
        r'href="/\1/"',
        content
    )
    
    # Pattern: ../../blog/author/pathi/index.html -> /blog/author/pathi/
    content = re.sub(
        r'href="(?:\.\./)+([a-z][a-z0-9-]+/[a-z][a-z0-9-]+/[a-z][a-z0-9-]+)/index\.html"',
        r'href="/\1/"',
        content
    )
    
    # Pattern: ../blog/index.html -> /blog/
    content = re.sub(
        r'href="(?:\.\./)+([a-z][a-z0-9-]+)/index\.html"',
        r'href="/\1/"',
        content
    )
    
    # ===== 7. Fix remaining relative asset paths (src, href for CSS/favicons) =====
    # Convert ../favicon.svg -> /favicon.svg etc for <link> tags
    content = re.sub(
        r'(href=")(?:\.\./)+(_astro/[^"]+)"',
        r'\g<1>/\2"',
        content
    )
    content = re.sub(
        r'(href=")(?:\.\./)+assets/([^"]+)"',
        r'\g<1>/assets/\2"',
        content
    )
    content = re.sub(
        r'(href=")(?:\.\./)+favicon([^"]+)"',
        r'\g<1>/favicon\2"',
        content
    )
    content = re.sub(
        r'(href=")(?:\.\./)+apple-touch-icon([^"]+)"',
        r'\g<1>/apple-touch-icon\2"',
        content
    )
    content = re.sub(
        r'(href=")(?:\.\./)+site\.webmanifest"',
        r'\g<1>/site.webmanifest"',
        content
    )
    content = re.sub(
        r'(href=")(?:\.\./)+safari-pinned-tab([^"]+)"',
        r'\g<1>/safari-pinned-tab\2"',
        content
    )
    
    # ===== 8. Fix relative src paths for images and SVGs =====
    content = re.sub(
        r'(src=")(?:\.\./)+(_astro/[^"]+)"',
        r'\g<1>/\2"',
        content
    )
    content = re.sub(
        r'(src=")(?:\.\./)+images/([^"]+)"',
        r'\g<1>/images/\2"',
        content
    )
    
    # ===== 9. Fix og:image pointing to profile-pics/pathi.html (wrong file) =====
    content = content.replace(
        'content="../../../images/profile-pics/pathi.html"',
        'content="' + BASE + '/images/book-a-taxi-og.jpg"'
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {filepath}")
    else:
        print(f"OK:    {filepath}")

# Process all HTML files
for root, dirs, files in os.walk(ROOT):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            fix_html_file(os.path.join(root, file))

print("\n✅ Comprehensive SEO fix complete!")
