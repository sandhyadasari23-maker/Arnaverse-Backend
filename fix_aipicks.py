import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/AIPicks.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'Server error. Please check if the backend is running.'
replacement = 'Cannot connect to server. Please make sure the backend server is running.'
code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated AIPicks.js")
