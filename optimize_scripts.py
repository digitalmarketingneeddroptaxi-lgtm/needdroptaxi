import os
import re

def optimize_scripts_and_a11y(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content

    # 1. Change Clarity script to partytown
    # We look for <script type="text/javascript"> right before clarity code
    new_content = re.sub(
        r'<script type="text/javascript">(\s*\(function\s*\(c,\s*l,\s*a,\s*r,\s*i,\s*t,\s*y\))',
        r'<script type="text/partytown">\1',
        new_content
    )

    # 2. Add loading="lazy" to iframes
    def iframe_replacer(match):
        iframe_tag = match.group(0)
        if 'loading=' not in iframe_tag:
            # add loading="lazy" before the closing bracket
            iframe_tag = iframe_tag[:-1] + ' loading="lazy">'
        return iframe_tag
    new_content = re.sub(r'<iframe\s+[^>]+>', iframe_replacer, new_content)

    # 3. Add aria-label to the mobile close button (a tag wrapping a specific svg)
    # The tag looks like: <a x-on:click.prevent="mobileNavOpen = !mobileNavOpen" href="#" class="focus:outline-none focus:ring-2 focus:ring-yellow-500 rounded-full p-1" data-astro-cid-pml5ybxm>
    close_btn_pattern = r'(<a x-on:click\.prevent="mobileNavOpen = !mobileNavOpen" href="#" class="focus:outline-none[^>]+>)'
    
    def close_btn_replacer(match):
        tag = match.group(1)
        if 'aria-label' not in tag:
            return tag[:-1] + ' aria-label="Close Mobile Menu">'
        return tag

    new_content = re.sub(close_btn_pattern, close_btn_replacer, new_content)

    # 4. Add defer to Alpine if missing, wait it's already there `<script src="..." defer></script>`
    # 5. Fix any empty links in the mobile menu list
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Optimized: {os.path.basename(filepath)}")

if __name__ == "__main__":
    optimize_scripts_and_a11y('c:\\Users\\Pathi\\Documents\\needdroptaxi.com')
