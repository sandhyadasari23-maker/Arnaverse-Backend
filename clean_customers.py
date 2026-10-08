import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Customers.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# I will find the whole renderData function and replace it.
start = code.find('const renderData = (customers) => {')
end = code.find('        if (cachedCustomers) {', start)

replacement = '''    const renderData = (customers) => {
        // Safety check: ensure user hasn't navigated away during fetch
        const customerCountEl = document.getElementById("customerCount");
        if (!customerCountEl) return;

        customerCountEl.textContent = customers.length;
        
        if (customers.length === 0) {
            container.innerHTML = `<p>No customers found.</p>`;
            return;
        }
        
        container.innerHTML = customers.map((c, index) => `
            <div class="card customer-card" data-index="${index}" style="padding: 25px; border-top: 4px solid var(--primary); position: relative;">
                <h3 style="margin: 0 0 8px; color: var(--text-dark);">${Utils.escapeHtml(c.name)}</h3>
                <p style="margin: 3px 0; color: var(--text-muted);"><i class="fa-solid fa-envelope" style="width:20px; color:var(--primary);"></i> ${Utils.escapeHtml(c.email)}</p>
                <p style="margin: 3px 0; color: var(--text-muted);"><i class="fa-solid fa-phone" style="width:20px; color:var(--primary);"></i> ${Utils.escapeHtml(c.phone || "N/A")}</p>
                <p style="margin: 3px 0; color: var(--text-muted);"><i class="fa-solid fa-location-dot" style="width:20px; color:var(--primary);"></i> ${Utils.escapeHtml(c.city || "N/A")}</p>
                <p style="margin: 15px 0 0; font-size: 12px; color: var(--text-muted);">Joined: ${Utils.formatDate(c.created_at)}</p>
            </div>
        `).join('');
    };

'''

code = code[:start] + replacement + code[end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Cleaned up renderData")
