import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''            let statusBadge = "";
            if (b.stock > 5) {
                statusBadge = `<span style="background: #e0f8e9; color: #1e7e34; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #4ade80, #166534); border-radius: 50%; box-shadow: 0 0 5px rgba(74, 222, 128, 0.5);"></span> In Stock</span>`;
            } else {
                statusBadge = `<span style="background: #fce4e4; color: #c82333; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #f87171, #991b1b); border-radius: 50%; box-shadow: 0 0 5px rgba(248, 113, 113, 0.5);"></span> Low Stock</span>`;
            }'''

replacement = '''            let statusBadge = "";
            if (b.stock > 5) {
                statusBadge = `<span style="background: #e0f8e9; color: #1e7e34; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #4ade80, #166534); border-radius: 50%; box-shadow: 0 0 5px rgba(74, 222, 128, 0.5);"></span> In Stock</span>`;
            } else if (b.stock > 0) {
                statusBadge = `<span style="background: #fdf2d0; color: #d39e00; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #fbbf24, #b45309); border-radius: 50%; box-shadow: 0 0 5px rgba(251, 191, 36, 0.5);"></span> Low Stock</span>`;
            } else {
                statusBadge = `<span style="background: #fce4e4; color: #c82333; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #f87171, #991b1b); border-radius: 50%; box-shadow: 0 0 5px rgba(248, 113, 113, 0.5);"></span> Out of Stock</span>`;
            }'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed status badge logic")
else:
    print("Could not find exact target string")
