import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Remove silent cloud sync log
    code = code.replace('.catch(err => console.log("Silent cloud sync failed:", err));', '.catch(() => {});')
    
    # Remove console.error(err) inside catches
    code = re.sub(r'console\.error\(err\);', '', code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

files = [
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/main.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Customers.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/ManageOrders.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/ManageBouquets.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Inventory.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/admin/Dashboard.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/orders.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Profile.js',
    'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Register.js'
]

for f in files:
    if os.path.exists(f):
        process_file(f)
print("Suppressed console.error in all files.")
