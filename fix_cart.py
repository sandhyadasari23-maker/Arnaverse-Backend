import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/cart.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the mangled cart icon with the actual shopping cart emoji
target = r'<div class="empty-icon".*?>.*?</div>'
replacement = '<div class="empty-icon" style="font-size:45px; margin-bottom:15px;">🛒</div>'

code = re.sub(target, replacement, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed cart icon")
