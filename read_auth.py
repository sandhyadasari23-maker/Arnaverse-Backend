import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/main.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('const isAdmin = localStorage')
print(code[idx:idx+800])
