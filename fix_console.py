import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/ManageBouquets.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'console.error("Image upload skipped/failed:", err);'
replacement = 'console.warn("Image upload skipped/failed (Bucket missing). Using fallback image.");'

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed console log")
