import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js'

with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Inject the search and filter UI right before the table
html_target = '''            <section style="background: white; border-radius: 14px; padding: 20px; border: 1px solid #eadfe2; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">'''
html_replacement = '''            <section style="background: white; border-radius: 14px; padding: 20px; border: 1px solid #eadfe2; overflow-x: auto;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; gap: 15px; flex-wrap: wrap;">
                    <div style="flex:1; min-width: 250px;">
                        <input type="text" id="inventorySearch" placeholder="Search by ID or Name..." style="padding:12px 15px; width:100%; border-radius:8px; border:1px solid #ccc; font-size: 14px;">
                    </div>
                    <select id="inventoryFilter" style="padding:12px 15px; border-radius:8px; border:1px solid #ccc; font-size: 14px; cursor:pointer; min-width: 200px;">
                        <option value="all">All Items</option>
                        <option value="in_stock">In Stock</option>
                        <option value="low_stock">Low Stock</option>
                        <option value="out_stock">Out of Stock</option>
                    </select>
                </div>
                <table style="width: 100%; border-collapse: collapse; text-align: left;">'''

code = code.replace(html_target, html_replacement)

# 2. Add filtering logic to JS
js_target = '''    const renderData = (bouquets) => {'''
js_replacement = '''    const renderData = (bouquets) => {
        // Calculate counts
        const countAll = bouquets.length;
        const countInStock = bouquets.filter(b => b.stock > 5).length;
        const countLowStock = bouquets.filter(b => b.stock > 0 && b.stock <= 5).length;
        const countOutStock = bouquets.filter(b => b.stock <= 0).length;

        // Update top cards
        document.getElementById('totalItems').textContent = countAll;
        document.getElementById('inStockItems').textContent = countInStock;
        document.getElementById('lowStockItems').textContent = countLowStock;
        document.getElementById('outStockItems').textContent = countOutStock;

        // Update dropdown text with counts
        const filterSelect = document.getElementById('inventoryFilter');
        if (filterSelect) {
            filterSelect.options[0].text = `All Items (${countAll})`;
            filterSelect.options[1].text = `In Stock (${countInStock})`;
            filterSelect.options[2].text = `Low Stock (${countLowStock})`;
            filterSelect.options[3].text = `Out of Stock (${countOutStock})`;
        }

        // Apply filters
        const searchVal = (document.getElementById('inventorySearch')?.value || '').toLowerCase();
        const filterVal = document.getElementById('inventoryFilter')?.value || 'all';

        let filteredBouquets = bouquets.filter(b => {
            const matchesSearch = b.id.toLowerCase().includes(searchVal) || b.name.toLowerCase().includes(searchVal);
            if (!matchesSearch) return false;

            if (filterVal === 'in_stock') return b.stock > 5;
            if (filterVal === 'low_stock') return b.stock > 0 && b.stock <= 5;
            if (filterVal === 'out_stock') return b.stock <= 0;
            return true;
        });

        bouquets = filteredBouquets;
'''

code = code.replace(js_target, js_replacement)

# Remove the old count updating logic which is now merged into renderData
old_counts = '''        document.getElementById('totalItems').textContent = bouquets.length;
        document.getElementById('inStockItems').textContent = bouquets.filter(b => b.stock > 5).length;
        document.getElementById('lowStockItems').textContent = bouquets.filter(b => b.stock > 0 && b.stock <= 5).length;
        document.getElementById('outStockItems').textContent = bouquets.filter(b => b.stock <= 0).length;'''

code = code.replace(old_counts, '')

# Bind event listeners to re-render when typing/changing filters
init_bottom = '''    const loadInventory = (forceRender = false) => {'''
init_bottom_replacement = '''    const loadInventory = (forceRender = false) => {
        const searchInput = document.getElementById('inventorySearch');
        const filterSelect = document.getElementById('inventoryFilter');
        
        if (searchInput && !searchInput.dataset.bound) {
            searchInput.dataset.bound = "true";
            searchInput.addEventListener('input', () => { if(cachedInventory) renderData(cachedInventory); });
        }
        if (filterSelect && !filterSelect.dataset.bound) {
            filterSelect.dataset.bound = "true";
            filterSelect.addEventListener('change', () => { if(cachedInventory) renderData(cachedInventory); });
        }
'''
code = code.replace(init_bottom, init_bottom_replacement)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Filters added")
