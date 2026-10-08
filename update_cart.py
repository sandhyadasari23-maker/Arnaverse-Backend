import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/cart.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''<div class="cart-item-category" style="font-size:12px; color:var(--primary); font-weight:bold; text-transform:uppercase;">${Utils.escapeHtml(item.category || "Bouquet")}</div>
                        <h3 class="cart-item-name">${Utils.escapeHtml(item.name)}</h3>
                        <div class="cart-item-price" style="font-weight:bold; color:var(--text-dark);">&#8377;${price}</div>'''

replacement = '''<div class="cart-item-category" style="font-size:12px; color:var(--primary); font-weight:bold; text-transform:uppercase;">${Utils.escapeHtml(item.category || "Bouquet")}</div>
                        <h3 class="cart-item-name">${Utils.escapeHtml(item.name)}</h3>
                        ${item.customization ? `
                        <div style="font-size: 13px; color: var(--text-muted); margin: 6px 0;">
                            <div><strong>Flower:</strong> ${Utils.escapeHtml(item.customization.flower || '')}</div>
                            <div><strong>Size:</strong> ${Utils.escapeHtml(item.customization.size || '')}</div>
                            <div><strong>Ribbon:</strong> ${Utils.escapeHtml(item.customization.ribbon || '')}</div>
                            <div><strong>Add Card:</strong> ${Utils.escapeHtml(item.customization.card || '')}</div>
                        </div>
                        ` : ''}
                        <div class="cart-item-price" style="font-weight:bold; color:var(--text-dark);">&#8377;${price}</div>'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated cart rendering")
else:
    print("Could not find target in cart.js")
