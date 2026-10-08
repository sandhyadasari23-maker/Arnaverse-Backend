import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Register.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        .catch(err => {
            msg.textContent = "Server error. Please try again later.";
            msg.style.display = "block";
            msg.className = "alert alert-error";
        });'''

replacement = '''        .catch(err => {
            msg.textContent = "Cannot connect to server. The backend might be offline.";
            msg.style.display = "block";
            msg.className = "alert alert-error";
        });'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated Register.js network error msg")
else:
    print("Target not found in Register.js")
