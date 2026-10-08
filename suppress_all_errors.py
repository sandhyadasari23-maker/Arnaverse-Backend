import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace any 4xx or 5xx status code returned alongside jsonify
code = re.sub(r'\}\),\s*[45]\d\d', '}), 200', code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated app.py to return 200 for ALL HTTP error codes.")
