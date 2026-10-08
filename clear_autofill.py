import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = 'export function init() {'
replacement = '''export function init() {
    // Clear browser autofill if any
    setTimeout(() => {
        const emailEl = document.getElementById("email");
        const passEl = document.getElementById("password");
        if (emailEl) emailEl.value = '';
        if (passEl) passEl.value = '';
    }, 50);
'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Added autofill clearing logic")
else:
    print("Target not found")
