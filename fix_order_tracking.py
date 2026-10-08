import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/OrderTracking.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'Error loading tracking details.'
replacement = 'Cannot connect to server. Please make sure the backend server is running.'
code = code.replace(target, replacement)

# Remove console.error
code = re.sub(r'console\.error\(err\);', '', code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated OrderTracking.js")
