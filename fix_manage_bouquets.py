import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/ManageBouquets.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'Server error.'
replacement = 'Cannot connect to server. Please make sure the backend server is running.'
code = code.replace(target, replacement)

target2 = 'Failed to delete.'
replacement2 = 'Cannot connect to server. Please make sure the backend server is running.'
code = code.replace(target2, replacement2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated ManageBouquets.js")
