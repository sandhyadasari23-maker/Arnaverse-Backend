import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

if 'from dotenv import load_dotenv' not in code:
    code = code.replace('import os', 'import os\nfrom dotenv import load_dotenv\nload_dotenv()')

target = '''        if not key_id or not key_secret:
            return jsonify({"success": False, "message": "Razorpay keys not configured"}), 500'''

replacement = '''        if not key_id or not key_secret:
            return jsonify({"success": False, "message": "Razorpay keys not configured"}), 500
            
        if "YOUR_TEST_KEY" in key_id or "YOUR_TEST_KEY" in key_secret:
            return jsonify({"success": False, "message": "Please replace the placeholder Razorpay keys in your .env file with real test keys from your Razorpay Dashboard."}), 400'''

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated app.py with load_dotenv and dummy key check")
