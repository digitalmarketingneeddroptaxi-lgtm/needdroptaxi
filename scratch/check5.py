import codecs
with codecs.open('scan_results.txt', 'r', 'utf-16le') as f:
    lines = f.readlines()
    for line in lines:
        if 'index.html' in line or 'outstation-taxi-service' in line:
            print(line.strip())
        elif 'BROKEN' in line:
            print(line.strip())
