import os
import re
from PIL import Image

def optimize_html(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                process_html(os.path.join(root, file))

def process_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find images
    img_pattern = re.compile(r'<img([^>]+)>')
    
    def replacer(match):
        attrs_str = match.group(1)
        original_attrs = attrs_str
        
        has_width = 'width=' in attrs_str
        has_height = 'height=' in attrs_str
        has_alt = 'alt=' in attrs_str
        has_loading = 'loading=' in attrs_str
        has_fetchpriority = 'fetchpriority=' in attrs_str
        
        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs_str)
        if not src_match:
            return match.group(0)
            
        src = src_match.group(1)
        
        # Add alt if missing
        if not has_alt:
            attrs_str += ' alt=""'
            
        # Hero image check (e.g., taxi-p1)
        is_hero = 'taxi-p1' in src or 'hero' in src or 'taxi-booking-bg' in src
        
        if is_hero:
            if 'loading="lazy"' in attrs_str:
                attrs_str = attrs_str.replace('loading="lazy"', '')
            if not has_fetchpriority:
                attrs_str += ' fetchpriority="high"'
        else:
            if not has_loading:
                attrs_str += ' loading="lazy"'
                
        # Dimensions check
        if not has_width or not has_height:
            # Try to find the image size
            # Remove leading slash or handling relative paths
            img_path = src.lstrip('/')
            full_img_path = os.path.join('c:\\Users\\Pathi\\Documents\\needdroptaxi.com', img_path)
            
            try:
                with Image.open(full_img_path) as img:
                    width, height = img.size
                    if not has_width:
                        attrs_str += f' width="{width}"'
                    if not has_height:
                        attrs_str += f' height="{height}"'
            except Exception as e:
                pass # print(f"Could not read {full_img_path}: {e}")

        # Clean up multiple spaces
        attrs_str = re.sub(r'\s+', ' ', attrs_str).strip()
        
        new_tag = f'<img {attrs_str}>'
        if new_tag != match.group(0):
            print(f"Updated in {os.path.basename(filepath)}: {src}")
            
        return new_tag

    new_content = re.sub(img_pattern, replacer, content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == "__main__":
    optimize_html('c:\\Users\\Pathi\\Documents\\needdroptaxi.com')
    print("Done optimizing images.")
