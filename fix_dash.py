import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Dashboard.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''    const renderDashboard = (orders) => {

        const totalSales = orders.reduce((sum, order) => sum + Number(order.total || 0), 0);'''

replacement = '''    const renderDashboard = (orders) => {
        // Safety check: ensure user hasn't navigated away during the fetch
        const totalOrdersEl = document.getElementById("totalOrders");
        if (!totalOrdersEl) return; // Abort if dashboard HTML is no longer in the DOM

        const totalSales = orders.reduce((sum, order) => sum + Number(order.total || 0), 0);'''

code = code.replace(target, replacement)

target2 = '''        document.getElementById("totalOrders").textContent = orders.length;

        document.getElementById("totalSales").textContent = `â‚¹${totalSales}`;'''

replacement2 = '''        totalOrdersEl.textContent = orders.length;
        document.getElementById("totalSales").textContent = `₹${totalSales}`;'''

code = code.replace(target2, replacement2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Dashboard.js safely")
