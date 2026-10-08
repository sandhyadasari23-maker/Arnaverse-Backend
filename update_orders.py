import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/ManageOrders.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = r'<div style="font-weight: 700; color: var\(--text-dark\);">\$\{Utils\.escapeHtml\(item\.name \|\| \'Bouquet\'\)\}</div>\s*<div style="color: var\(--text-muted\); font-size: 14px;">Qty: \$\{item\.quantity \|\| 1\}</div>'

replacement = '''<div style="font-weight: 700; color: var(--text-dark);">${Utils.escapeHtml(item.name || 'Bouquet')}</div>
                                ${item.customization ? `
                                <div style="font-size: 13px; color: var(--text-muted); margin: 6px 0;">
                                    <div><strong>Flower:</strong> ${Utils.escapeHtml(item.customization.flower || '')}</div>
                                    <div><strong>Size:</strong> ${Utils.escapeHtml(item.customization.size || '')}</div>
                                    <div><strong>Ribbon:</strong> ${Utils.escapeHtml(item.customization.ribbon || '')}</div>
                                    <div><strong>Add Card:</strong> ${Utils.escapeHtml(item.customization.card || '')}</div>
                                </div>
                                ` : ''}
                                <div style="color: var(--text-muted); font-size: 14px;">Qty: ${item.quantity || 1}</div>'''

if re.search(target, code):
    code = re.sub(target, replacement, code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated ManageOrders rendering")
else:
    print("Could not find target in ManageOrders.js")
