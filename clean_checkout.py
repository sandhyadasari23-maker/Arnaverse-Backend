import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''    document.querySelectorAll('input[name="payment"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            document.getElementById('upiBox').style.display = 'none'; // Handled by Razorpay popup
        });
    });'''
code = code.replace(target, '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print('Cleaned up event listeners')
