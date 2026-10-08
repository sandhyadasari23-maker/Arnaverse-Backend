import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Remove Add Bouquet button
code = code.replace('<a href="#/admin-add-bouquet" class="btn">+ Add New Bouquet</a>', '')

# Sort bouquets in JS before rendering
target = 'const renderData = (bouquets) => {'
replacement = '''const renderData = (bouquets) => {
        bouquets.sort((a, b) => {
            const numA = parseInt(a.id.replace(/\D/g, '')) || 0;
            const numB = parseInt(b.id.replace(/\D/g, '')) || 0;
            return numA - numB;
        });'''
code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated successfully")
