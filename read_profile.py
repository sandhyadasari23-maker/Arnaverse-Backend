import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Profile.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('msg.textContent = "Profile updated')
print(code[idx:idx+800])
