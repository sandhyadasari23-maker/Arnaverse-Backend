import os
import re

path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Dashboard.js'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(
    r'let\s+cachedOrders\s*=\s*null;', 
    'let cachedOrders = JSON.parse(localStorage.getItem("arnaverse_admin_dashboard_orders")) || null;', 
    code
)

fetch_success_regex = r'(cachedOrders\s*=\s*data\.orders\s*\|\|\s*\[\];)'
replacement = r'\1\n                localStorage.setItem("arnaverse_admin_dashboard_orders", JSON.stringify(cachedOrders));'
code = re.sub(fetch_success_regex, replacement, code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('Applied to Dashboard.js')
