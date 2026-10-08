import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/orders.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = r'<div style="text-align:center; padding:40px; color:red;">Error loading orders.</div>'
replacement = '<div style="text-align:center; padding:40px; color:#d9534f;">Cannot connect to server. The backend might be offline.</div>'

code = re.sub(target, replacement, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated orders.js UI error msg")
