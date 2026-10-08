import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Register.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = r'showMessage\("Server error. Please try again later.", "error"\);'
replacement = 'showMessage("Cannot connect to server. The backend might be offline.", "error");'

code = re.sub(target, replacement, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Register.js UI error msg")
