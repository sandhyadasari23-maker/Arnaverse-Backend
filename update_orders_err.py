import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/orders.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''            .catch(err => {
                console.error(err);
                if (!cachedOrders) {
                    container.innerHTML = `<p style="text-align:center; color:red;">Error loading orders.</p>`;
                }
            });'''

replacement = '''            .catch(err => {
                console.error(err);
                if (!cachedOrders) {
                    container.innerHTML = `<p style="text-align:center; color:#d9534f; padding: 40px;">Cannot connect to server. The backend might be offline.</p>`;
                }
            });'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated orders.js error message")
else:
    print("Target not found in orders.js")
