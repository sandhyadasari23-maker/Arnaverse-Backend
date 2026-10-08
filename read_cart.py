import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/cart.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('<div class="cart-item-category"')
print(code[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
