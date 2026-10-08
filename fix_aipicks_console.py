import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/AIPicks.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Remove console.error
code = re.sub(r'console\.error\(err\);', '', code)
code = re.sub(r'console\.error\(.*?\);', '', code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated AIPicks.js")
