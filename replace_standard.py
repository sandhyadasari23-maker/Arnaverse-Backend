import os
import glob

files = glob.glob('C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/**/*.js', recursive=True)
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    code = code.replace("Cannot connect to server. The backend might be offline.", "Cannot connect to server. Please make sure the backend server is running.")
    code = code.replace("Cannot connect to server. The backend might be offline", "Cannot connect to server. Please make sure the backend server is running.")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
        
print("Replaced standard error string.")
