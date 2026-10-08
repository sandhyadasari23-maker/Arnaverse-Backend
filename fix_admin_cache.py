import os
import re

def update_file(filename, cache_key, var_name):
    path = f'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/{filename}'
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Replace module-level cache init
    code = re.sub(
        fr'let\s+{var_name}\s*=\s*null;', 
        f'let {var_name} = JSON.parse(localStorage.getItem("{cache_key}")) || null;', 
        code
    )
    
    # Replace the fetch assignment
    fetch_success_regex = fr'({var_name}\s*=\s*data\.\w+\s*\|\|\s*\[\];)'
    replacement = f'\\1\n                    localStorage.setItem("{cache_key}", JSON.stringify({var_name}));'
    code = re.sub(fetch_success_regex, replacement, code)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)

update_file('ManageOrders.js', 'arnaverse_admin_orders', 'cachedManageOrders')
update_file('ManageBouquets.js', 'arnaverse_admin_bouquets', 'cachedBouquets')
update_file('Customers.js', 'arnaverse_admin_customers', 'cachedCustomers')
update_file('Inventory.js', 'arnaverse_admin_inventory', 'cachedInventory')

print("Applied localStorage SWR to all admin pages")
