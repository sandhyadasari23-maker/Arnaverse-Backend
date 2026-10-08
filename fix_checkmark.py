import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/OrderTracking.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace any mangled checkmarks we can find
# Just use a regex to replace the icon assignment line directly!
import re
target = r'const icon = index <= currentIndex \? ".*?" : \(index \+ 1\);'
replacement = 'const icon = index <= currentIndex ? "✔" : (index + 1);'
code = re.sub(target, replacement, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed OrderTracking.js")
