import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Customers.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove Edit Customer button
code = re.sub(r'<button class="btn btn-secondary edit-customer-btn" style="margin-top: 15px; width: 100%; padding: 8px;">Edit Customer</button>', '', code)

# 2. Remove the edit-mode div
edit_mode_regex = r'<div class="edit-mode" style="display: none;.*?</div>\s*</div>\s*</div>'
code = re.sub(edit_mode_regex, '</div>', code, flags=re.DOTALL)

# 3. Remove event listeners for editing
listeners_regex = r'// Bind edit toggle events.*?}\);'
code = re.sub(listeners_regex, '', code, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Removed Edit Customer functionality")
