import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add safety check at the top of renderData
target1 = r'(const renderData = \(bouquets\) => \{)'
replacement1 = r'\1\n        // Safety check: ensure user hasn\'t navigated away during fetch\n        const tableBodyEl = document.getElementById("inventoryTableBody");\n        if (!tableBodyEl) return;\n'

import re
code = re.sub(target1, replacement1, code)

# 2. Add safety check in loadInventory fetch callbacks
target2 = r'(if \(!cachedInventory\) \{[\s\n]*tableBody\.innerHTML = `<tr><td colspan="7".*?Failed to load inventory\.</td></tr>`;[\s\n]*\})'
replacement2 = r'if (!cachedInventory) {\n                    const tBody = document.getElementById("inventoryTableBody");\n                    if (tBody) tBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:red;">Failed to load inventory.</td></tr>`;\n                }'

code = re.sub(target2, replacement2, code, count=1)

target3 = r'(if \(!cachedInventory\) \{[\s\n]*tableBody\.innerHTML = `<tr><td colspan="7".*?Error connecting to server\.</td></tr>`;[\s\n]*\})'
replacement3 = r'if (!cachedInventory) {\n                    const tBody = document.getElementById("inventoryTableBody");\n                    if (tBody) tBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:red;">Error connecting to server.</td></tr>`;\n                }'
code = re.sub(target3, replacement3, code, count=1)

target4 = r'(else if \(!cachedInventory\) \{[\s\n]*tableBody\.innerHTML = `<tr><td colspan="7".*?Loading inventory\.\.\.</td></tr>`;[\s\n]*\})'
replacement4 = r'else if (!cachedInventory) {\n            const tBody = document.getElementById("inventoryTableBody");\n            if (tBody) tBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px;">Loading inventory...</td></tr>`;\n        }'
code = re.sub(target4, replacement4, code, count=1)

# Ensure no weird â‚¹ chars
code = code.replace('â‚¹', '₹')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Applied SPA race condition fix to Inventory.js")
