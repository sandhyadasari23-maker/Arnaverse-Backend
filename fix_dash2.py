import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Dashboard.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add safety check at the top of renderDashboard
target1 = r'(const renderDashboard = \(orders\) => \{)'
replacement1 = r'\1\n        const totalOrdersEl = document.getElementById("totalOrders");\n        if (!totalOrdersEl) return;\n'
code = re.sub(target1, replacement1, code)

# 2. Fix the usage of totalOrders
target2 = r'document\.getElementById\("totalOrders"\)\.textContent = orders\.length;'
replacement2 = r'totalOrdersEl.textContent = orders.length;'
code = re.sub(target2, replacement2, code)

# 3. Clean up the mangled rupee symbol if it's there
code = code.replace('â‚¹', '₹')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Dashboard.js safely via regex")
