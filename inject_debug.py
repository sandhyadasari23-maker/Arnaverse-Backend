import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        if request.method == "POST":
            order_data = request.get_json()
            response = execute_with_retry(supabase.table("orders").insert(order_data))'''

replacement = '''        if request.method == "POST":
            order_data = request.get_json()
            print("=== INCOMING POST /api/orders ===", flush=True)
            print("Payload:", order_data, flush=True)
            try:
                response = execute_with_retry(supabase.table("orders").insert(order_data))
                print("Supabase Insert Response:", getattr(response, 'data', 'No data attribute'), flush=True)
            except Exception as e:
                print("Supabase Insert Error:", str(e), flush=True)
                raise e'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Injected debug prints")
else:
    print("Could not find target to inject debug prints")
