import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        .catch(err => {
            console.error(err);
            msg.textContent = "Error placing order. Try again later.";
            msg.style.color = "#d9534f";
        });'''

replacement = '''        .catch(err => {
            console.error("Network Error:", err);
            msg.textContent = "Cannot connect to server. The backend might be offline.";
            msg.style.color = "#d9534f";
        });'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated Checkout.js network error handling")
else:
    print("Target not found in Checkout.js")
