with open('templates/Dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

if '<script src="/static/js/custom_features.js"></script>' not in text:
    text = text.replace('</body>', '    <script src="/static/js/custom_features.js"></script>\n</body>')
    with open('templates/Dashboard.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Injected custom_features.js')
else:
    print('Already injected')
