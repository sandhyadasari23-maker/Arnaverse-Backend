import os
import glob
import re

files = glob.glob('C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/**/*.js', recursive=True)
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'fetch(' not in content:
        continue
        
    print(f"\n--- {os.path.basename(filepath)} ---")
    
    # Simple regex to find catch blocks
    catches = re.findall(r'\.catch\([^)]*\)\s*=>?\s*\{[^}]*\}', content)
    for c in catches:
        print(c)
    
    catches2 = re.findall(r'catch\s*\([^)]*\)\s*\{[^}]*\}', content)
    for c in catches2:
        print(c)
