import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scratch' in root or '.system_generated' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f).replace('\\', '/'))

print(f"Processing {len(html_files)} files for JavaScript and resource URL fixes...")

changes_count = 0

for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig = content
    
    # 1. Fix jQuery relative links
    content = re.sub(
        r'src=[\'"][^\'"]*code\.jquery\.com/jquery-3\.6\.0\.min\.js[\'"]',
        'src="https://code.jquery.com/jquery-3.6.0.min.js"',
        content
    )
    
    # 2. Fix Alpine.js relative links
    content = re.sub(
        r'src=[\'"][^\'"]*cdn\.jsdelivr\.net/npm/%40alpinejs/collapse%403\.x\.x/dist/cdn\.min\.js[\'"]',
        'src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"',
        content
    )
    content = re.sub(
        r'src=[\'"][^\'"]*cdn\.jsdelivr\.net/npm/alpinejs%403\.13\.3/dist/cdn\.min\.js[\'"]',
        'src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"',
        content
    )
    
    # 3. Fix Google Tag Manager Partytown relative snippet
    # e.g.: j.src = "../../www.googletagmanager.com/gtm5445.html?id=" + i + dl;
    content = re.sub(
        r'j\.src\s*=\s*[\'"][^\'"]*www\.googletagmanager\.com/gtm5445\.html\?id=[\'"]\s*\+\s*i\s*\+\s*dl;',
        'j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;',
        content
    )
    
    # 4. Fix relative cdn-cgi email-decode script
    # e.g.: src="../cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"
    content = re.sub(
        r'src=[\'"]\.\./+(?:cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode\.min\.js)[\'"]',
        'src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"',
        content
    )
    content = re.sub(
        r'src=[\'"]\.\./\.\./+(?:cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode\.min\.js)[\'"]',
        'src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"',
        content
    )
    content = re.sub(
        r'src=[\'"]\.\./\.\./\.\./+(?:cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode\.min\.js)[\'"]',
        'src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"',
        content
    )
    
    # 5. Fix trip-fare-calculator assets relative bundle path
    if 'trip-fare-calculator' in p:
        content = re.sub(
            r'src=[\'"]\.\./assets/index-2bcf8e26\.js[\'"]',
            'src="/assets/index-2bcf8e26.js"',
            content
        )
    
    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        changes_count += 1
        print(f"Updated JS resources in: {p}")

print(f"Total files updated for JS resources: {changes_count}")
