import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'message.textContent = "Server error. Please try again later.";'
replacement = 'message.textContent = "Cannot connect to server. Please make sure the backend server is running.";'
code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated login.js")
