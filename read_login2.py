import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('<input type="email"')
print(code[idx:idx+200])

idx = code.find('<input type="password"')
print(code[idx:idx+200])

idx = code.find('admin@')
if idx != -1:
    print(code[idx-50:idx+150])
