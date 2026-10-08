import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('autocomplete="email"', 'autocomplete="off"')
code = code.replace('autocomplete="current-password"', 'autocomplete="new-password"')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Disabled autofill")
