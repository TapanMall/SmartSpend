import codecs

print('Fixing Dashboard budget calculation references')
with codecs.open('templates/Dashboard.html', 'r', 'utf-8') as f:
    dash = f.read()

# Replace if (t.type === 'debit') with the new block
dash = dash.replace(
    "if (t.type === 'debit') {",
    "const tType = (t.type || '').toLowerCase();\n                if (tType === 'debit' || tType === 'expense') {"
)

with codecs.open('templates/Dashboard.html', 'w', 'utf-8') as f:
    f.write(dash)
print('Dashboard.html updated successfully')
