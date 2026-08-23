import os
file_path = r"c:\Users\Pathi\Documents\needdroptaxi.com\drop-taxi\chennai-to-tirupati\index.html"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Look for logo
idx = content.find("Need Drop Taxi Logo")
if idx != -1:
    print("Logo area:", content[max(0, idx-100):min(len(content), idx+100)])

# Look for 2,410
idx2 = content.find("2,410")
if idx2 != -1:
    print("Price area:", content[max(0, idx2-50):min(len(content), idx2+50)])
