import sys
sys.stdout.reconfigure(encoding='utf-8')

html = open('templates/Dashboard.html', encoding='utf-8').read()
custom_js = open('static/js/custom_features.js', encoding='utf-8').read()

checks = [
    ('Budget modal injection', 'MODAL HTML INJECTION' in custom_js and 'id="budgetModal"' in custom_js),
    ('Goal modal injection', 'id="goalModal"' in custom_js),
    ('Category icon map', 'catIconMap' in html and 'getCatIcon' in html),
    ('Analytics rounding', 'Math.round(data.expenses / 30)' in html),
    ('Budget overage colors', 'rawPct > 100' in custom_js),
    ('Old budget error removed', 'Budget modal not available' not in html),
    ('Old goal error removed', 'Goal modal not available' not in html),
]

for name, ok in checks:
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}] {name}')

print(f'\nAll checks passed!' if all(ok for _, ok in checks) else '\nSome checks FAILED!')
