import re
import glob

def fix_mega_menu():
    files = glob.glob(r"c:\Users\Pathi\Documents\needdroptaxi.com\**\*.html", recursive=True)
    count = 0
    for file in files:
        if ".git" in file: continue
        
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        # 1. Change position:relative to position:static on the li
        content = re.sub(
            r'<li x-on:mouseenter="taxiServicesOpen = true" x-on:mouseleave="taxiServicesOpen = false" style="position:relative;z-index:50;"',
            r'<li x-on:mouseenter="taxiServicesOpen = true" x-on:mouseleave="taxiServicesOpen = false" style="position:static;"',
            content
        )
        
        # 2. Update width on the dropdown and add top:100% just in case
        content = re.sub(
            r'style="display:none;position:absolute;left:50%;transform:translateX\(-50%\);padding-top:24px;width:1200px;z-index:100;"',
            r'style="display:none;position:absolute;left:50%;top:68px;transform:translateX(-50%);padding-top:24px;width:min(1200px, calc(100vw - 32px));z-index:100;"',
            content
        )
        
        if content != original:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
    print(f"Updated {count} files.")

if __name__ == "__main__":
    fix_mega_menu()
