import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('if request.method == "POST":')
print(code[idx:idx+800])
