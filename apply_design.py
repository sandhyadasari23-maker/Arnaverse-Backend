import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update the HTML layout to match the design exactly
# Replace the table headers and add the "Inventory Items" title
html_target = r'<table style="width: 100%; border-collapse: collapse; text-align: left;">[\s\S]*?</thead>'
html_replacement = '''<h2 style="margin: 0 0 20px 0; color: #9b335a; font-size: 24px;">Inventory Items</h2>
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 2px solid #f9eef2; background: #fdf5f7;">
                            <th style="padding: 15px; color: #9b335a; font-weight: bold;">Product</th>
                            <th style="padding: 15px; color: #9b335a; font-weight: bold;">Type</th>
                            <th style="padding: 15px; color: #9b335a; font-weight: bold;">Price</th>
                            <th style="padding: 15px; color: #9b335a; font-weight: bold;">Stock</th>
                            <th style="padding: 15px; color: #9b335a; font-weight: bold;">Status</th>
                            <th style="padding: 15px; color: #9b335a; font-weight: bold;">Action</th>
                        </tr>
                    </thead>'''

code = re.sub(html_target, html_replacement, code)

# 2. Update the row mapping in JS
row_target = r'tableBody\.innerHTML = bouquets\.map\(b => `[\s\S]*?`\)\.join\(\'\'\);'
row_replacement = '''tableBody.innerHTML = bouquets.map(b => {
            let statusBadge = "";
            if (b.stock > 5) {
                statusBadge = `<span style="background: #e0f8e9; color: #1e7e34; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #4ade80, #166534); border-radius: 50%; box-shadow: 0 0 5px rgba(74, 222, 128, 0.5);"></span> In Stock</span>`;
            } else {
                statusBadge = `<span style="background: #fce4e4; color: #c82333; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-flex; align-items: center; gap: 8px;"><span style="width: 10px; height: 10px; background: linear-gradient(135deg, #f87171, #991b1b); border-radius: 50%; box-shadow: 0 0 5px rgba(248, 113, 113, 0.5);"></span> Low Stock</span>`;
            }
            
            let typeVal = b.flower || b.category || "Bouquet";
            if (typeVal.length > 15) typeVal = typeVal.split(' ')[0];
            
            return `
            <tr style="border-bottom: 1px solid #f3e8eb;">
                <td style="padding: 18px 15px; font-weight: bold; color: #333;">${Utils.escapeHtml(b.name)}</td>
                <td style="padding: 18px 15px; color: #999;">${Utils.escapeHtml(typeVal)}</td>
                <td style="padding: 18px 15px; color: #333;">₹${b.price}</td>
                <td style="padding: 18px 15px; font-weight: bold; color: #333;">${b.stock}</td>
                <td style="padding: 18px 15px;">
                    ${statusBadge}
                </td>
                <td style="padding: 18px 15px;">
                    <button class="update-stock-btn" data-id="${Utils.escapeHtml(b.id)}" data-stock="${b.stock}" data-name="${Utils.escapeHtml(b.name)}" style="background: #9b335a; color: white; border: none; padding: 10px 18px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; display:inline-flex; align-items:center; gap:8px;"><i class="fas fa-pencil-alt" style="font-size:12px; color: #fba9c4;"></i> Update Stock</button>
                </td>
            </tr>
            `;
        }).join('');'''

code = re.sub(row_target, row_replacement, code)

# 3. Replace the Update Listeners and Delete Listeners with just the new prompt-based Update Listeners
listeners_target = r'// Stock Update Listeners[\s\S]*?// Delete Listeners[\s\S]*?\}\);[\s\n]*\}\);'
listeners_replacement = '''// Stock Update Listeners
        document.querySelectorAll('.update-stock-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const btnEl = e.currentTarget;
                const id = btnEl.getAttribute('data-id');
                const name = btnEl.getAttribute('data-name');
                const currentStock = btnEl.getAttribute('data-stock');
                
                const newStockStr = prompt(`Enter new stock quantity for ${name}:`, currentStock);
                if (newStockStr === null) return;
                
                const newStock = parseInt(newStockStr, 10);
                if (isNaN(newStock) || newStock < 0) {
                    alert("Please enter a valid positive number.");
                    return;
                }
                
                const originalHTML = btnEl.innerHTML;
                btnEl.innerHTML = 'Saving...';
                btnEl.style.opacity = '0.7';

                fetch('http://127.0.0.1:5000/api/bouquets', { 
                    method: 'PUT', 
                    headers: getHeaders(true),
                    body: JSON.stringify({ id: id, stock: newStock })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        btnEl.innerHTML = 'Saved!';
                        btnEl.style.background = '#2e8b57';
                        btnEl.style.opacity = '1';
                        
                        const bouquet = cachedInventory.find(b => b.id === id);
                        if (bouquet) bouquet.stock = newStock;
                        
                        setTimeout(() => loadInventory(true), 800);
                    } else {
                        alert(data.message || "Failed to update stock.");
                        btnEl.innerHTML = originalHTML;
                        btnEl.style.opacity = '1';
                    }
                })
                .catch(err => {
                    console.error(err);
                    alert("Error updating stock.");
                    btnEl.innerHTML = originalHTML;
                    btnEl.style.opacity = '1';
                });
            });
        });'''

code = re.sub(listeners_target, listeners_replacement, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Applied design update to Inventory.js")
