import re

print('Fixing PDF blank bug with regex')
with open('static/js/reports_and_settings.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Remove containerDiv creation
p1 = r"const containerDiv = document\.createElement\('div'\);[\s\S]*?document\.body\.appendChild\(containerDiv\);"
js = re.sub(p1, '', js)

# 2. Fix the html2pdf input
p2 = r"containerDiv\.innerHTML = contentBody;"
js = re.sub(p2, '', js)

p3 = r"\.from\(containerDiv\)\.save\(\);[\s\S]*?document\.body\.removeChild\(containerDiv\);"
js = re.sub(p3, '.from(contentBody).save();', js)

with open('static/js/reports_and_settings.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('Successfully patched reports_and_settings.js')
