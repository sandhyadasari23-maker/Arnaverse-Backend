import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/main.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace /admin-login routing fallback
code = code.replace("window.location.hash = '#/admin-login';", "window.location.hash = '#/login';")
code = code.replace("path !== '/admin-login'", "path !== '/login'")

# Optionally remove the route itself, but it doesn't hurt if we leave it for backwards compat or delete it
code = re.sub(r"\s*'/admin-login':[^,]+,", "", code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated main.js routing")
