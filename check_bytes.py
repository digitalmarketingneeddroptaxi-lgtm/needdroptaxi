import os

file = r"c:\Users\Pathi\Documents\needdroptaxi.com\privacy-policy\index.html"
with open(file, 'rb') as f:
    content = f.read()

idx = content.find(b"the Company")
print("Around Company:", content[idx-10:idx+30])

file2 = r"c:\Users\Pathi\Documents\needdroptaxi.com\terms-and-conditions\index.html"
with open(file2, 'rb') as f:
    content2 = f.read()
    
idx2 = content2.find(b"150")
if idx2 != -1:
    print("Around 150:", content2[idx2-10:idx2+20])
