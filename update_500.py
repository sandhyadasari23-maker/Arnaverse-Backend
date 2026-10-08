import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('"error": str(error)', '"message": "Server Error: " + str(error), "error": str(error)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated 500 error messages")
