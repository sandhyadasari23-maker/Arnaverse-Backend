import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">'
replacement = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">'

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated index.html")
