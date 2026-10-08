import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(r'from dotenv import load_dotenv\nload_dotenv()\n', '')

if 'from dotenv import load_dotenv' not in code:
    code = 'from dotenv import load_dotenv\nload_dotenv()\n' + code

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed app.py properly")
