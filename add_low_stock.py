import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# First clean up the weird newlines if any
code = code.replace('\n\n\n', '\n').replace('\n\n', '\n')

target_html = '''                <div class="card" style="text-align: center; padding: 25px;">
                    <h2 id="outStockItems" style="margin: 5px 0; color: var(--danger); font-size: 28px;">0</h2>
                    <p style="margin: 0; color: var(--text-muted);">Out of Stock</p>
                </div>'''
replacement_html = '''                <div class="card" style="text-align: center; padding: 25px;">
                    <h2 id="lowStockItems" style="margin: 5px 0; color: #f59e0b; font-size: 28px;">0</h2>
                    <p style="margin: 0; color: var(--text-muted);">Low Stock</p>
                </div>
                <div class="card" style="text-align: center; padding: 25px;">
                    <h2 id="outStockItems" style="margin: 5px 0; color: var(--danger); font-size: 28px;">0</h2>
                    <p style="margin: 0; color: var(--text-muted);">Out of Stock</p>
                </div>'''
code = code.replace(target_html, replacement_html)

# Update the JS logic
target_js = '''        document.getElementById('totalItems').textContent = bouquets.length;
        document.getElementById('inStockItems').textContent = bouquets.filter(b => b.stock > 0).length;
        document.getElementById('outStockItems').textContent = bouquets.filter(b => b.stock <= 0).length;'''
replacement_js = '''        document.getElementById('totalItems').textContent = bouquets.length;
        document.getElementById('inStockItems').textContent = bouquets.filter(b => b.stock > 5).length;
        document.getElementById('lowStockItems').textContent = bouquets.filter(b => b.stock > 0 && b.stock <= 5).length;
        document.getElementById('outStockItems').textContent = bouquets.filter(b => b.stock <= 0).length;'''
code = code.replace(target_js, replacement_js)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated')
