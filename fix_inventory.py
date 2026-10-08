import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'Error connecting to server.'
replacement = 'Cannot connect to server. Please make sure the backend server is running.'
code = code.replace(target, replacement)

target2 = 'Error updating stock.'
replacement2 = 'Cannot connect to server. Please make sure the backend server is running.'
code = code.replace(target2, replacement2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Inventory.js")
