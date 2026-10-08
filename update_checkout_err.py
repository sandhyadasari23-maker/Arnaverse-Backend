import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''            .then(res => res.json())
            .then(data => {
                if (!data.success) throw new Error(data.message || "Failed to create payment");'''

replacement = '''            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    msg.textContent = data.message || "Failed to create payment";
                    msg.style.color = "#d9534f";
                    throw new Error(data.message || "Failed to create payment");
                }'''

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Checkout.js error handling")
